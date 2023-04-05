from fastapi import FastAPI
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router) 