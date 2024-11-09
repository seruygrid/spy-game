import uvicorn

from spy_game.app import create_app
from spy_game.settings.conf import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'spy_game.app:create_app',
        host='0.0.0.0',
        port=settings.PORT,
        log_level='info',
        loop='uvloop',
        reload=settings.DEBUG,
    )
