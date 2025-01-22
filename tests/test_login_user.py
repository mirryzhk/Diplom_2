import allure
import pytest
import data
import stellar_burgers_api


class TestLoginUser:
    @allure.title("Успешная авторизация существующего пользователя")
    @allure.description("Авторизация с email и password в теле запроса")
    def test_login_user_success(self, default_user):
        user_data = default_user['user_data']
        access_token = default_user['access_token']

        user_data.pop("name", None)
        login_response = stellar_burgers_api.login_user(user_data)
        stellar_burgers_api.delete_user(access_token)
        assert login_response.status_code == 200 and login_response.json()["success"] == True

    @allure.title("Проверка ошибки при попытке авторизоваться без email или password")
    @allure.description("Проверка возвращения ошибки при авторизации без обязательных полей: email и password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", ""),
                                 ("password", "")
                             ])
    def test_login_without_field_fail(self, key, value, default_user):
        user_data = default_user['user_data']
        access_token = default_user['access_token']

        login_data = user_data.copy()
        login_data[key] = value
        login_data.pop("name", None)
        login_response = stellar_burgers_api.login_user(login_data)
        stellar_burgers_api.delete_user(access_token)
        assert login_response.status_code == 401 and login_response.json()["message"] == data.MESSAGE_INCORRECT_DATA
