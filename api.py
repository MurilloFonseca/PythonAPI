import db
import jwt 

from uuid import uuid4
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Literal
from functools import wraps

from flask import Flask, Response, abort, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures.auth import Authorization

app = Flask(__name__)
app.config['PW'] = '4qK5ku8ZNCpTjHqM9fbabgLvjwGgWbLoeP4EJFr8FAY' # senha do JWT
# a senha foi criada usando a função secrets.token_urlsafe() do python

# decorator para verificar se o usuário está autenticado
def authenticate(f) -> Callable[[Any], Response]:
    @wraps(f)
    def _(*args, **kwargs) -> Response:
        if 'token' in request.headers:
            token: str | None = request.headers['token']
        else:
            abort(401)
        
        try:
            data: dict[str, Any] = jwt.decode(token, app.config['PW'], algorithms=['HS256'])
            if data['exp'] < datetime.now(timezone.utc).timestamp():
                abort(401)
            return f(*args, **kwargs)
        
        except:
            abort(401)

    return _


# users
@app.route('/user', methods=['POST'])
@authenticate
def create_user() -> Response:
    data: dict[str, Any] = request.get_json()

    if 'user' in data and 'password' in data:
        pw: str = generate_password_hash(data['password'])
        id = str(uuid4())
        db.users.insert_one({'id': id, 'name': data['user'], 'password': pw})
        
        return jsonify(db.users.find_one({'id': id}, {'_id': 0}))
    
    else:
        abort(400) # bad request


@app.route('/user', methods=['GET'])
@authenticate
def get_all_users() -> Response:
    limit: str | None = request.args.get('limit')
    if limit is not None:
        return jsonify([i for i in db.users.find({}, {'_id': 0}).limit(int(limit))])
    else:
        return jsonify([i for i in db.users.find({}, {'_id': 0})])

@app.route('/user/<id>', methods=['GET'])
@authenticate
def get_user_by_id(id) -> Response:
    return jsonify(db.users.find_one({'id': id}, {'_id': 0}))

@app.route('/user/<id>', methods=['PUT'])
@authenticate
def promote(id) -> Response:
    data: dict[str, Any] = request.get_json()
    db.users.update_one({'id': id}, {'$set': data})
    return jsonify(db.users.find_one({'id': id}, {'_id': 0}))

@app.route('/user/<id>', methods=['DELETE'])
@authenticate
def delete_user(id) -> Response:
    db.users.delete_one({'id': id})
    return jsonify()

# login
@app.route('/login', methods=['GET'])
def login() -> Response:
    data: Authorization | None = request.authorization
    if data is not None:
        try:
            for user in db.users.find({'name': data['username']}):
                if check_password_hash(user['password'], data['password']): # type: ignore
                    payload: dict[str, Any] = {
                            'user': data['username'],
                            'password': data['password'],
                            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
                        }
                    return jsonify({'token': jwt.encode(payload, app.config['PW'], algorithm='HS256')})
            else:
                abort(401)
        except:
            abort(400)
    else:
        abort(400)


# chamados
@app.route('/call', methods=['POST'])
@authenticate
def create_call() -> Response:
    data:dict[str, Any] = request.get_json()

    id = str(uuid4())
    data.update({'id': id})
    db.calls.insert_one(data)
    
    return jsonify(db.calls.find_one({'id': id}, {'_id': 0}))


@app.route('/call', methods=['GET'])
@authenticate
def get_all_calls() -> Response:
    limit: str | None = request.args.get('limit')
    if limit is not None:
        return jsonify([i for i in db.calls.find({}, {'_id': 0}).limit(int(limit))])
    else:
        return jsonify([i for i in db.calls.find({}, {'_id': 0})])

@app.route('/call/<id>', methods=['GET'])
@authenticate
def get_call_by_id(id) -> Response:
    return jsonify(db.calls.find_one({'id': id}, {'_id': 0}))

@app.route('/call/<id>', methods=['PUT'])
@authenticate
def edit_call(id) -> Response:
    data: dict[str, Any] = request.get_json()
    db.calls.update_one({'id': id}, {'$set': data})
    return jsonify(db.calls.find_one({'id': id}, {'_id': 0}))

@app.route('/call/<id>', methods=['DELETE'])
@authenticate
def delete_call(id) -> Response:
    db.calls.delete_one({'id': id})
    return jsonify()


app.run(port=5000, host='localhost')

