from fastapi import FastAPI
from . import models
from .database import engine, Base
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = ["https://www.google.com"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):   #Tells FastAPI to call get_db to create a SQLAlchemy Session, pass it in as db, and then close it when the request finishes
#     posts = db.query(models.Post).all()              #fetch all the posts from the database
#     return {"data": posts}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")   #decorator- Links the url to the python code below
async def root():
    return {"message": "Bind mount"}
