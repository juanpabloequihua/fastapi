from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from httpx import post
from pydantic import BaseModel ## Get the input parameters automatically
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = "fastapi", 
                                user = 'postgres', password = "password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connected to db")
        break
    except Exception as error: 
        print("Connection failed")
        print(error)
        time.sleep(3)
        



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "Favoirite food", "content": "I like Pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!"}

@app.get('/sqlalchemy')
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}

@app.get("/posts")
def get_posts():
    cursor.execute(""" Select * from posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post): ## Extract the body of the post request into a dictionary called paylod
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *; """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    cursor.execute(""" Select * from posts where id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} was not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id:int, status_code = status.HTTP_204_NO_CONTENT):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist.")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist.")
    conn.commit()
    return {"data": updated_post}
