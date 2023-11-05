from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{
    "id": 1,
    "title": "Hello",
    "content": "This is a blog post",
    "published": True,
    "rating": None
},
{
    "id": 95,
    "title": "Second Post",
    "content": "This is another blog post",
    "published": True,
    "rating": 5
}
]

def get_post_from_database(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = get_post_from_database(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = get_post_from_database(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    current = get_post_from_database(id)

    if not current:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[id] = post_dict
    return {"data": post_dict}