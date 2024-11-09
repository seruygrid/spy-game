import logging

from fastapi import FastAPI

from spy_game.api import game
from spy_game.settings.conf import settings

logger = logging.getLogger(__name__)


def init_routes(app: 'FastAPI') -> None:
    app.include_router(game.router, tags=['Game'])


def create_app() -> 'FastAPI':
    app = FastAPI(title='SPY Game', debug=settings.DEBUG)
    init_routes(app)
    return app
