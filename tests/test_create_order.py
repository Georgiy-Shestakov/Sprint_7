import pytest
import requests
import data
import allure

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