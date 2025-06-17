import pytest
import requests
from helpers import Helpers
import data
import allure

class TestCreateCourier:
    # Курьера можно создать
    # Запрос возвращает правильный код ответа
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле')
    def test_create_courier_status_code(self):
        response = Helpers.register_new_courier()
        with allure.step('Проверяем, что при успешном создании код 201'):
            assert response.status_code == 201


    # Успешный запрос возвращает {"ok":true}
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле')
    def test_create_courier_body(self):
        response = Helpers.register_new_courier()
        with allure.step('Проверяем, что при в теле ответа {"ok":true}'):
            assert response.text == '{"ok":true}'


    # Чтобы создать курьера, нужно передать в ручку 2 обязательных поля: login + password
    # Если одного из полей нет, запрос возвращает ошибку
    @pytest.mark.parametrize("payload", [
        {"login": Helpers.generate_random_string(10)},
        {"password": Helpers.generate_random_string(10)}
    ])
    @allure.step('Отправляем запрос на создание курьера, не заполнив одно из обязательных полей')
    def test_create_courier_body_without_one_of_required_fields(self, payload):
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(data.URL+'/courier', data=payload)
        with allure.step('Проверяем, что без одного из обязательных полей в ответ приходит код 400'):
            assert response.status_code == 400
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'


    # Нельзя создать двух одинаковых курьеров
    # Если создать пользователя с логином, который уже есть, возвращается ошибка
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле')
    def test_only_unique_courier_login_allowed(self):
        response_1 = Helpers.register_new_courier_and_return_login_password()
        # создаём тело запроса для создания курьера с уже существующим логином
        payload = Helpers.courier_payload_creation(response_1[0], Helpers.generate_random_string(10))
        with allure.step('Пробуем создать курьера с существующим логином'):
            response_2 = requests.post(data.URL+'/courier', data=payload)
        with allure.step('Проверяем, что при создании получили ошибку с кодом 409'):
            assert response_2.status_code == 409
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response_2.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'


class TestLogin:
    # Курьер может авторизоваться
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле и получаем логин и пароль учётки')
    def test_login(self):
        payload = Helpers.register_new_courier_and_return_login_password()
        # создаём тело для запроса авторизации
        payload_for_login = {"login":payload[0], "password":payload[1]}
        with allure.step('Пробуем авторизоваться с полученными кредами'):
            response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что при успешной авторизации код 200'):
            assert response.status_code == 200


    # Успешный запрос возвращает id
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле и получаем логин и пароль учётки')
    def test_id_after_login(self):
        payload = Helpers.register_new_courier_and_return_login_password()
        # создаём тело для запроса авторизации
        payload_for_login = {"login":payload[0], "password":payload[1]}
        with allure.step('Пробуем авторизоваться с полученными кредами'):
            response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что при успешной авторизации вернулся id курьера'):
            assert response.json()['id'] is not None


    # Для авторизации нужно передать все обязательные поля
    # Если какого-то поля нет, запрос возвращает ошибку
    @allure.step('Отправляем запрос на создание курьера только с одним полем')
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
        payload_for_login = {"login":Helpers.generate_random_string}
        response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что получили ошибку с кодом 504'):
            assert response.status_code == 504


    # Система вернёт ошибку, если неправильно указать логин или пароль
    @allure.step('Отправляем запрос на создание курьера с неправильными полями')
    def test_login_wrong_creds(self):
        payload_for_login = {"login":Helpers.generate_random_string, "password":Helpers.generate_random_string}
        response = requests.post(data.URL+'/courier/login', data=payload_for_login)
        with allure.step('Проверяем, что получили ошибку с кодом 404'):
            assert response.status_code == 404
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response.json()['message'] == 'Учетная запись не найдена'


class TestCreateOrder:
    # Заказ можно создать
    # Тело ответа содержит track
    # Можно указать один из цветов — BLACK или GREY
    # Можно совсем не указывать цвет
    # Можно совсем не указывать цвет
    @pytest.mark.parametrize("payload", [
        {**data.ORDER, "color": ["BLACK"]},
        {**data.ORDER, "color": ["GREY"]},
        {**data.ORDER, "color": ["BLACK", "GREY"]},
        {**data.ORDER}
    ])
    @allure.step('Отправляем запрос на создание заказа')
    def test_create_order_body(self, payload):
        response = requests.post(data.URL+'/orders', json=payload)
        with allure.step('Проверяем, что пришёл статус код 201'):
            assert response.status_code == 201
        with allure.step('Проверяем, что тело ответа содержит track'):
            assert response.json()['track'] is not None


class TestOrdersList:
    @allure.step('Отправляем запрос на получение списка заказов')
    def test_get_orders_list(self):
        response = requests.get(data.URL+'/orders')
        with allure.step('Проверяем, что пришёл статус код 200'):
            assert response.status_code == 200
        with allure.step('Проверяем, что в тело ответа возвращается список заказов'):
            assert response.json()['orders'] is not None 

