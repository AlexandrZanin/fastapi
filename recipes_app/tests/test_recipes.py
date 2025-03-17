from httpx import AsyncClient
from sqlalchemy import insert, select
from core.models import Recipe
from sqlalchemy.orm import Session


data = {
    "title": "Каша манка",
    "cooking_time": 5,
    "text": "Налить молоко в кастрюлю. В горячее молоко засыпать манку, помешивая",
    "ingredients_list": "Молоко, манка, соль, сахар"}


async def test_post(ac: AsyncClient):
    response = await ac.post("/recipes/", json=data)
    assert response.status_code == 201


async def test_post_invalid(ac: AsyncClient):
    response = await ac.post("/recipes/", json={
        "title": "Каша манная",
        "cooking_time": "a",
        "text": "Налить молоко в кастрюлю. В горячее молоко засыпать манку, помешивая",
        "ingredients_list": "Молоко, манка, соль, сахар"})
    assert response.status_code == 422


async def test_get(ac: AsyncClient):
    response = await ac.get("/recipes/1")
    assert response.status_code == 200
    assert response.json()['title'] == "Каша манка"
    assert response.json()['cooking_time'] == 5
    assert response.json()['text'] == "Налить молоко в кастрюлю. В горячее молоко засыпать манку, помешивая"
    assert response.json()['ingredients_list'] == "Молоко, манка, соль, сахар"



async def test_get_invalid(ac: AsyncClient):
    response = await ac.get("/recipes/11")
    assert response.status_code == 404


async def test_get_recipes(ac: AsyncClient):
    response = await ac.get("/recipes/")
    assert response.status_code == 200


async def test_root(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200


async def test_increase_views(ac: AsyncClient):
    response = await ac.get("/recipes/1")
    number_view=response.json()['number_view']
    response = await ac.get("/recipes/1")
    assert response.json()['number_view']==number_view+1