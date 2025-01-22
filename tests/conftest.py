import allure
import pytest
import stellar_burgers_api

@allure.step("Создание пользователя")
@pytest.fixture(scope='function')
def default_user():
    user_body = stellar_burgers_api.create_user_body()
    user_response = stellar_burgers_api.create_user(user_body)
    access_token = stellar_burgers_api.get_access_token(user_response)
    yield {"user_data": user_body,
           "access_token": access_token,
           "user_response" : user_response
           }
    stellar_burgers_api.delete_user(access_token)


@allure.step("Создание бургера из имеющихся ингредиентов")
@pytest.fixture(scope='function')
def default_burger():
    ingredients = stellar_burgers_api.get_ingredients().json()
    ingredient_types = {"main": None, "sause": None, "bun": None}
    for item in ingredients["data"]:
        if item["type"] in ingredient_types and ingredient_types[item["type"]] is None:
            ingredient_types[item["type"]] = item["_id"]
    burger_ingredient = {"ingredients": list(ingredient_types.values())}
    return burger_ingredient

