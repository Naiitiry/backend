# Instalar FastApi con: pip install fastapi[all]

from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

# uvicorn main:app --reload --> inicia el servidor 

app = FastAPI()

# Routers, traido desde routers

app.include_router(products.router)
app.include_router(users.router)
app.mount("/static",StaticFiles(directory="static"),name="static")

# URL local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hola como están perros?!"

# URL local: http://127.0.0.1:8000/url

@app.get("/url")
async def root():
    return {"url_curso":"https://mouredev.com/python"}

# documentacion con Swagger: http://127.0.0.1:8000/docs
# documentacion con Redocly: http://127.0.0.1:8000/redoc

