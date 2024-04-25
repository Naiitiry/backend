from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

'''
OAuth2PasswordBearer: 
                        Se encarga de gestionar usuario y contraseña.

OAuth2PasswordRequestForm:
                        Forma de capturar usuario y contraseña y contrastar con nuestra BD, verificando
                        que exista realmente ese usuario con esa contraseña.
'''

app = FastAPI()

# uvicorn basic_auth_users:app --reload

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "roman":{
        "username": "roman",
        "full_name": "roman danchuk",
        "email": "romandanchuk@prowerrangers.com",
        "disable": False,
        "password":"123456"
    },
    "roman2":{
        "username": "roman2",
        "full_name": "roman chanchuk",
        "email": "romanchanchuk@prowerrangers.com",
        "disable": True,
        "password":"1234"
    },
    "facundo":{
        "username": "facundo",
        "full_name": "facundo danchuk",
        "email": "facundodanchuk@prowerrangers.com",
        "disable": False,
        "password":"4r4g5ghxd"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia
async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate":"Bearer"}
            )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    
    return user

"Como voy a enviar usuario y contraseña para recibir algo, va POST"
"Depends: recibe datos pero no depende de nadie"
@app.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta.")
    
    return {"access_token":user.username,"token_type":"bearer"}

@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user