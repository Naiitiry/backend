from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
# timedelta para trabajar con calculos de fechas

'''
********* JSON Web Tokens *********

Se debe instalar la siguiente depencias de criptografía:
pip install "python-jose[cryptography]"
'''

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()
#uvicorn jwt_auth_users:app --reload

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Algoritmo de encriptación
crypt = CryptContext(schemes=["bcrypt"])

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
        "password":"$2a$12$jNoCklId4PIFUcRIQj4Hv.d0hZAXMrlLY8cKwsPNqNghKdmbo3v9S"
    },
    "roman2":{
        "username": "roman2",
        "full_name": "roman chanchuk",
        "email": "romanchanchuk@prowerrangers.com",
        "disable": True,
        "password":"$2a$12$GVR51K8OWjWfF7K/CpBs.OUzvMJF0unt4/W8fK40v9LMBic.RkiKa"
    },
    "facundo":{
        "username": "facundo",
        "full_name": "facundo danchuk",
        "email": "facundodanchuk@prowerrangers.com",
        "disable": False,
        "password":"$2a$12$LHpPnbikhQQ4BcZ0vEloFe0xsm2c94RSL057upNSnW54koVsy8DwC"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta.")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub":user.username,
                    "exp":expire,

                    }

    return {"access_token":jwt.encode(access_token,algorithm=ALGORITHM),"token_type":"bearer"}

# minutos 5:19:00, continuar viendolo para aprender.