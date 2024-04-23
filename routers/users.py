from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                    tags=["users"],
                    responses={404:{"message":"No encontrado."}})

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

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Roman","surname":"Danchuk","url":"htpps://mouredev.com/python","age":33},
            {"name":"Lila","surname":"Danchuk Cherdemian","url":"htpps://mouredev.com/python","age":3},
            {"name":"Yasmin","surname":"Cherdemian","url":"htpps://mouredev.com/python","age":27}
            ]

@router.get("/")
async def users():
    return users_list

@router.get("/{id}")       # PATH
async def user(id:int):
    return search_user(id)
# En PATH debería probarse así: */user/2
    
@router.get("/userquery/")      # QUERY
async def user(id:int):
    return search_user(id)
# En query debería probarse así: */userquery/?id=2

# Creacion de usuario:
@router.post("/",status_code=201)          # POST
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

# Modificación de usuarios:
@router.put("/")         # PUT
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user

# Eliminación de usuarios:
@router.delete("/{id}")    # DELETE
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]


# Creamos una función para PATH y Query
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "no se ha encontrado el usuario"}
    
{"id":4,"name":"Yasmin","surname":"Cherdemian","url":"htpps://mouredev.com/python","age":27}