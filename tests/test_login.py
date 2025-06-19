import requests
from helpers import Helpers
import data
import allure

class TestLogin:
    # Курьер может авторизоваться
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле и получаем логин и пароль учётки')
    def test_login_first(self, courier_creation_and_delete_after_test_list):
        # создаём тело для запроса авторизации
        payload = courier_creation_and_delete_after_test_list
        with allure.step('Пробуем авторизоваться с полученными кредами'):
            response = requests.post(data.URL+'/courier/login', data=payload)
        with allure.step('Проверяем, что при успешной авторизации код 200'):
            assert response.status_code == 200


    # Успешный запрос возвращает id
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле и получаем логин и пароль учётки')
    def test_id_after_login(self, courier_creation_and_delete_after_test_list):
        # создаём тело для запроса авторизации
        payload = courier_creation_and_delete_after_test_list
        with allure.step('Пробуем авторизоваться с полученными кредами'):
            response = requests.post(data.URL+'/courier/login', data=payload)
        with allure.step('Проверяем, что при успешной авторизации вернулся id курьера'):
            assert response.json()['id'] is not None


    # Для авторизации нужно передать все обязательные поля
    # Если какого-то поля нет, запрос возвращает ошибку
    @allure.step('Отправляем запрос на регистрацию курьера только с одним полем')
    def test_login_required_fields(self):
        payload_for_login = {"password":"1234"}
        response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что получили ошибку с кодом 400'):
            assert response.status_code == 400
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response.json()['message'] == 'Недостаточно данных для входа'


    # Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку
    @allure.step('Отправляем запрос на создание курьера с несуществующим логином')
    def test_login_nonexistent_user(self):
        payload_for_login = {"login":Helpers.generate_random_string(10)}
        response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что получили ошибку с кодом 504'):
            assert response.status_code == 504


    # Система вернёт ошибку, если неправильно указать логин или пароль
    @allure.step('Отправляем запрос на создание курьера с неправильными полями')
    def test_login_wrong_creds(self):
        payload_for_login = {"login":Helpers.generate_random_string(10), "password":Helpers.generate_random_string(10)}
        response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что получили ошибку с кодом 404'):
            assert response.status_code == 404
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response.json()['message'] == 'Учетная запись не найдена'
