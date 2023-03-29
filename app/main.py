from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title:": "Hello World", "content": "This is my first post", "id" : 1},
            {"title:": "Hello World 2", "content": "This is my second post", "id" : 2}]

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return -1

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict =  post.dict()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)

    return {"data": post_dict}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    try:
        post = my_posts[id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}

    return {"data": post}

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id=id)
    #delete the post with the id using index
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} not found")
    my_posts.pop(index)
    return {"message": f"Post with id {id} deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id=id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} not found")
    my_posts[index] = post
    return {"data": post}
