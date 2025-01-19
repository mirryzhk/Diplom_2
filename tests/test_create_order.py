import allure
import stellar_burgers_api
import data


class TestCreateOrder:
    @allure.title("Успешное создание заказа авторизованным пользователем с ингредиентами")
    @allure.description("Авторизация в системе и создание заказа с бургером")
    def test_create_order_burger_auth_user_success(self, default_burger, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = stellar_burgers_api.create_new_order(headers, default_burger)
        assert create_response.status_code == 200 and create_response.json()["order"]["number"] != None

    @allure.title("Ошибка 400 Bad Request при попытке сделать пустой заказ авторизованным пользователем")
    @allure.description(
        "При попытке сделать пустой заказ авторизованным пользователем, возвращается ошибка 400 Bad Request")
    def test_create_order_without_burger_auth_user_fail(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = stellar_burgers_api.create_new_order(headers, None)
        assert create_response.status_code == 400 and create_response.json()["message"] == data.MESSAGE_EMPTY_ORDER_AUTH


    @allure.title("Ошибка 401 Unauthorized при попытке сделать заказ бургера неавторизованным пользователем")
    @allure.description(
        "Неавторизованный пользователь не может сделать заказ бургера, возвращается ошибка 401 Unauthorized")
    def test_create_order_burger_not_auth_user_fail(self, default_burger):
        create_response = stellar_burgers_api.create_new_order(None, default_burger)
        assert create_response.status_code == 200


    @allure.title("Ошибка 400 Bad Request при попытке сделать пустой заказ неавторизованным пользователем")
    @allure.description(
        "При попытке сделать пустой заказ неавторизованным пользователем возвращается ошибка 400 Bad Request")
    def test_create_order_without_burger_not_auth_user_fail(self):
        create_response = stellar_burgers_api.create_new_order(None, None)
        assert create_response.status_code == 400 and create_response.json()["message"] == data.MESSAGE_EMPTY_ORDER_NOT_AUTH

    @allure.title("Ошибка 500 Internal Server Error при попытке сделать заказ авторизованным пользователем с невалидным хешем ингредиента")
    @allure.description(
        "При попытке сделать заказ авторизованным пользователем ингредиенты с невалидным хешем, возвращается ошибка 500 Internal Server Error")
    def test_create_order_auth_user_wrong_hash_fail(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        ingredients = data.WRONG_INGREDIENTS
        create_response = stellar_burgers_api.create_new_order(headers, ingredients)
        assert create_response.status_code == 500

    @allure.title(
        "Ошибка 500 Internal Server Error при попытке сделать заказ неавторизованным пользователем с невалидным хешем ингредиента")
    @allure.description(
        "При попытке сделать заказ неавторизованным пользователем ингредиенты с невалидным хешем, возвращается ошибка 500 Internal Server Error")
    def test_create_order_not_auth_user_wrong_hash_fail(self):
        ingredients = data.WRONG_INGREDIENTS
        create_response = stellar_burgers_api.create_new_order(None, ingredients)
        assert create_response.status_code == 500
