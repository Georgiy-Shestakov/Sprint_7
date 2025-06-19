import pytest
import requests
from helpers import Helpers
import data

@pytest.fixture
def courier_creation_and_delete_after_test_list():
    # генерируем логин и пароль
    login = Helpers.generate_random_string(10)
    password = Helpers.generate_random_string(10)
    
    # Формируем тело для дальнейшей передачи в запрос на логин
    payload = Helpers.courier_payload_creation(login, password)   

    # отправляем запрос на регистрацию курьера и сохраняем данные в переменную creation_response
    requests.post(data.URL+'/courier', data=payload)

    # Логинимся под созданным курьером, чтобы получить логин
    login_response = requests.post(f"{data.URL}/courier/login", data=payload).json()
    courier_id = login_response['id']

    # Передаём данные созданного курьера в тесты
    yield payload

    # Удаляем созданного ранее курьера
    Helpers.delete_courier(courier_id)


@pytest.fixture
def register_new_courier_and_delete_after_test():
    # генерируем логин и пароль
    login = Helpers.generate_random_string(10)
    password = Helpers.generate_random_string(10)
    
    # Формируем тело для дальнейшей передачи в запрос на логин
    payload = Helpers.courier_payload_creation(login, password)

    # отправляем запрос на регистрацию курьера и сохраняем данные в переменную creation_response
    creation_response = requests.post(data.URL+'/courier', data=payload)

     # Логинимся под созданным курьером, чтобы получить логин
    login_response = requests.post(f"{data.URL}/courier/login", data=payload).json()
    courier_id = login_response['id']

    # Передаём ответ на запрос регистрации курьера в тесты
    yield creation_response

    # Удаляем созданного ранее курьера
    Helpers.delete_courier(courier_id)
