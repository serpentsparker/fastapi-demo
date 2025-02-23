import fastapi

from myapi.actors import router as actor_router
from myapi.async_actors import router as async_actor_router

app = fastapi.FastAPI()

app.include_router(actor_router.router, tags=["actors"])
app.include_router(async_actor_router.router, tags=["async-actors"])


@app.get("/")
def index():
    return {"message": "Welcome to my API"}
