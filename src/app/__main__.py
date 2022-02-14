import fastapi
from src import __appdescription__, __version__
from src.app.routers import healthcheck

app_config = dict(
    debug=True,
    title=__appdescription__,
    version=__version__
)
app = fastapi.FastAPI(**app_config)
app.include_router(healthcheck.router)


@app.get('/')
async def root():
    return {
        'title': __appdescription__,
        'version': __version__
    }
