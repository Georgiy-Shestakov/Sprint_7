import pytest
import requests
from helpers import Helpers
import data
import allure

class TestCreateCourier:
    # Курьера можно создать
    # Запрос возвращает правильный код ответа
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле')
    def test_create_courier_status_code(self, register_new_courier_and_delete_after_test):
        response = register_new_courier_and_delete_after_test
        with allure.step('Проверяем, что при успешном создании код 201'):
            assert response.status_code == 201


    # Успешный запрос возвращает {"ok":true}
    @allure.step('Отправляем запрос на создание курьера с рандомными значениями в теле')
    def test_create_courier_body(self, register_new_courier_and_delete_after_test):
        response = register_new_courier_and_delete_after_test
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
    def test_only_unique_courier_login_allowed(self, courier_creation_and_delete_after_test_list):
        response_1 = courier_creation_and_delete_after_test_list
        # создаём тело запроса для создания курьера с уже существующим логином
        payload = Helpers.courier_payload_creation(response_1["login"], Helpers.generate_random_string(10))
        with allure.step('Пробуем создать курьера с существующим логином'):
            response_2 = requests.post(data.URL+'/courier', data=payload)
        with allure.step('Проверяем, что при создании получили ошибку с кодом 409'):
            assert response_2.status_code == 409
        with allure.step('Проверяем, что в теле ответа вернулось описание ошибки'):
            assert response_2.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'