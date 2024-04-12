import uvicorn
from fastapi import FastAPI

from app.api import middlewares, routes
from app.config import settings
from app.db.init_db import init_db
from app.log import init_loguru


class Server:
    def __init__(self):
        init_loguru()
        self.app = FastAPI()

    def init_app(self):
        init_db()
        middlewares.init_middleware(self.app)
        routes.init_routers(self.app)

    def run(self):
        self.init_app()
        uvicorn.run(
            app=self.app,
            host=settings.SERVER.HOST,
            port=settings.SERVER.PORT,
        )
