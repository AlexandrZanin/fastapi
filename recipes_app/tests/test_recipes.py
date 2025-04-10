from httpx import AsyncClient


data = {
    "title": "Каша манка",
    "cooking_time": 5,
    "text": "Налить молоко в кастрюлю. "
            "В горячее молоко засыпать манку, помешивая",
    "ingredients_list": "Молоко, манка, соль, сахар",
}


class Tests:
    async def test_post(self, ac: AsyncClient):
        response = await ac.post("/recipes/", json=data)
        assert response.status_code == 201

    async def test_post_invalid(self, ac: AsyncClient):
        response = await ac.post(
            "/recipes/",
            json={
                "title": "Каша манная",
                "cooking_time": "a",
                "text": "Налить молоко в кастрюлю."
                        " В горячее молоко засыпать манку, помешивая",
                "ingredients_list": "Молоко, манка, соль, сахар",
            },
        )
        assert response.status_code == 422

    async def test_get(self, ac: AsyncClient):
        response = await ac.get("/recipes/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Каша манка"
        assert response.json()["cooking_time"] == 5
        assert (
            response.json()["text"]
            == "Налить молоко в кастрюлю."
               " В горячее молоко засыпать манку, помешивая"
        )
        assert (response.json()["ingredients_list"]
                == "Молоко, манка, соль, сахар")

    async def test_get_invalid(self, ac: AsyncClient):
        response = await ac.get("/recipes/11")
        assert response.status_code == 404

    async def test_get_recipes(self, ac: AsyncClient):
        response = await ac.get("/recipes/")
        assert response.status_code == 200

    async def test_root(self, ac: AsyncClient):
        response = await ac.get("/")
        assert response.status_code == 200

    async def test_increase_views(self, ac: AsyncClient):
        response = await ac.get("/recipes/1")
        number_view = response.json()["number_view"]
        response = await ac.get("/recipes/1")
        assert response.json()["number_view"] == number_view + 1

    async def test_update(self, ac: AsyncClient):
        response = await ac.put(
            "/recipes/1",
            json={
                "title": "Бутерброд",
                "cooking_time": 1,
                "text": "Нарезать, намазать",
                "ingredients_list": "Хлеб, Сыр, Колбаса",
            },
        )
        assert response.status_code == 200
        response = await ac.get("/recipes/1")
        assert response.json()["title"] == "Бутерброд"
