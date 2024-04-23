from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# uvicorn users:app --reload --> inicia el servidor 

# Entidad User, para evitar hacer a mano lo de abajo (@app.get("/usersjson"))

class User(BaseModel):
    id: int # para realizar el path
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Roman",surname="Danchuk",url="htpps://mouredev.com/python",age=33),
            User(id=2, name="Lila",surname="Danchuk Cherdemian",url="htpps://mouredev.com/python",age=3),
            User(id=3, name="Yasmin",surname="Cherdemian",url="htpps://mouredev.com/python",age=27)
            ]

@app.get("/usersjson")
async def usersjson():
    return [{"name":"Roman","surname":"Danchuk","url":"htpps://mouredev.com/python","age":33},
            {"name":"Lila","surname":"Danchuk Cherdemian","url":"htpps://mouredev.com/python","age":3},
            {"name":"Yasmin","surname":"Cherdemian","url":"htpps://mouredev.com/python","age":27}
            ]

@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")
async def user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    return list(users)