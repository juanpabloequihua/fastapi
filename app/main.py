
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, config
from .database import engine
from .routers import post, user, auth, vote


# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# models.Base.metadata.create_all(bind = engine)
## Adding new comment for commit test

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## redirect routers from corresponding py files. 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!! Now deployed.!"}


