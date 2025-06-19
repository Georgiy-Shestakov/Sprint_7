import requests
import data
import allure

class TestOrdersList:
    @allure.step('Отправляем запрос на получение списка заказов')
    def test_get_orders_list(self):
        response = requests.get(data.URL+'/orders')
        with allure.step('Проверяем, что пришёл статус код 200'):
            assert response.status_code == 200
        with allure.step('Проверяем, что в тело ответа возвращается список заказов'):
            assert response.json()['orders'] is not None 

