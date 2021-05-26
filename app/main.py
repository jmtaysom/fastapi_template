import logging

import fastapi

from app.utils import logs, db

logger = logging.getLogger(__name__)


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app_logger = logs.CustomizeLogger.make_logger()
    app.logger = app_logger

    return app


app = create_app()


@app.on_event('startup')
async def startup_events():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


@app.get('/')
async def status_check(request: fastapi.Request):
    results = await db.database.execute("SELECT true")
    status = {
        "status": 'healthy',
        "database": 'connected' if results else 'not connected'
    }
    request.app.logger.info(status)
    return status
