import pymongo
from typing import Any
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

# servidor do banco de dados
client = pymongo.MongoClient(r'mongodb://localhost:27017') 
# Nome do banco de dados
db: Database[dict[str, Any]] = client['ChamadosAPI']

# entidades
users: Collection[dict[str, Any]] = db['users']
calls: Collection[dict[str, Any]] = db['calls']

# mais entidades podem ser adicionadas posteriormente