from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    post_list = list(posts_map)
    assert len(post_list) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client,test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get('/posts/8888')
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published",[
    ("Awersonme new title", "Awersome new content", True),
    ("Fav pizza", "good stuff", False)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == int(test_user["id"])

def test_create_post_default_published(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json={"title": "title published", "content": "dsfdsfsdfg"})
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title published"
    assert created_post.content == "dsfdsfsdfg"
    assert created_post.published == True
    assert created_post.owner_id == int(test_user["id"])

def test_unauthorized_user_create_all_posts(client,test_user,test_posts):
    res = client.post('/posts/', json={"title": "title published", "content": "dsfdsfsdfg"})
    assert res.status_code == 401



