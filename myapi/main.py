import fastapi

from myapi.actors import router as actor_router

app = fastapi.FastAPI()

app.include_router(actor_router.router, tags=["actors"])


@app.get("/")
def index():
    return {"message": "Welcome to my API"}
