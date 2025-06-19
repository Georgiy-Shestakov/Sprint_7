import requests
import random
import string
import data

class Helpers:
    # Метод для генерации строк заданной длины length
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string


    # Функция создания тела запроса для курьера
    def courier_payload_creation(login, password):
        payload = {
            "login": login,
            "password": password
        }
        return payload
    

    # Функция для удаления созданных данных
    def delete_courier(id):
        response = requests.delete(f"{data.URL}/courier/{id}")
        return response
