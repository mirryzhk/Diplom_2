import allure
import requests

import data
import urls
import pytest
import stellar_burgers_api


class TestChangeUserData:
    @allure.title("Проверка успешного изменения данных авторизованного пользователя")
    @allure.description("Успешное редактирование данных пользователя авторизованным пользователем: email, name, password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "vladvladov@yandex.ru"),
                                 ("name", " Vlad Vladov"),
                                 ("password", "777777")
                             ])
    def test_change_auth_user_data_success(self, key, value):
        user_data = stellar_burgers_api.create_user_body()
        stellar_burgers_api.create_user(user_data)
        body_data = user_data.copy()
        body_data.pop("name", None)
        login_response = stellar_burgers_api.login_user(body_data)
        access_token = stellar_burgers_api.get_access_token(login_response)
        body_data[key] = value
        change_response = stellar_burgers_api.change_user_data(access_token, body_data)
        stellar_burgers_api.delete_user(access_token)
        assert change_response.status_code == 200 and change_response.json()["success"] == True

    @allure.title("Проверка невозможности изменения данных неавторизованным пользователем")
    @allure.description(
        "Невозможность редактирования данных неавторизованным: email, name, password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", " vladvladov@yandex.ru "),
                                 ("name", " Vlad Vladov "),
                                 ("password", "777777")
                             ])
    def test_change_not_auth_user_data_fail(self, key, value):
        user_data = stellar_burgers_api.create_user_body()
        create_response = stellar_burgers_api.create_user(user_data)
        body_data = user_data.copy()
        body_data[key] = value
        change_response = requests.patch(urls.BASE_URL + urls.GET_USER_ENDPOINT, json=body_data)
        access_token = stellar_burgers_api.get_access_token(create_response)
        stellar_burgers_api.delete_user(access_token)
        assert change_response.status_code == 401 and change_response.json()["message"] == data.MESSAGE_NOT_CHANGE
