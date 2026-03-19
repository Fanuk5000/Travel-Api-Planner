from fastapi import FastAPI

from . import models
from .database import engine
from .routers import places, projects

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Planner API!"}


app.include_router(projects.router)
app.include_router(places.router)
