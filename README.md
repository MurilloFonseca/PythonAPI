# API para gerenciamento de chamados

## Descrição
Uma API para gerenciar e manter um sistema de chamados, podendo adicionar, alterar, listar e excluir tanto entradas de chamados quanto de usuários

## Tecnologias utilizadas
- Python: Linguagem em que a API foi escrita
- Flask: Framework usado para gerar uma aplicação web em python
- MongoDB: banco de dados noSQL 

### Dependências
- Pymongo
- Flask
- Pyjwt

## EndPoints

### /login
- usado para autenticar o usuário
- somente pode ser usado com o método GET
- retorna um token jwt que deve ser enviado no header dos demais endpoints

### /user e /call
- permitem os métodos GET, POST, PUT e DELETE
- permite a query 'limit' para limitar o número de retornos
- precisam do parâmetro token no header, com um jwt autenticado, para funcionar
- os parâmetros para o post e put devem ser inseridos no body

## Instalação e uso
Para utilizar a API é necessário um servidor para o banco de dados e outro para a API.
se o MongoDB e as dependências já estiverem instaladas, basta executar o arquivo 'api.py' que a API já estará rodando em um servidor local.