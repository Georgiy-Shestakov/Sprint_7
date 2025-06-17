# Sprint_7

## Описание проекта

Этот проект представляет собой набор API тестов сервиса https://qa-scooter.praktikum-services.ru/
Документация размещена здесь: https://qa-scooter.praktikum-services.ru/docs/
Тесты проверяют функциональность создания курьеров и заказов, авторизацию курьеров и получение списка заказов

## Результаты тестов

Результаты тестов сохраняются в формате Allure и находятся в директории `tests/allure_results/`. Для просмотра результатов тестов используйте Allure Report

## Структура проекта

- `data.py`: Содержит данные, используемые в тестах
- `helpers.py`: Содержит вспомогательные функции для тестов
- `tests/`: Директория с тестами
  - `tests.py`: Файл с тест-кейсами
  - `allure_results/`: Директория с результатами тестов в формате Allure

## Зависимости

Для установки зависимостей используйте файл `tests/requirements.txt`:
```
allure-pytest==2.14.3
allure-python-commons==2.14.3
attrs==25.3.0
certifi==2025.6.15
charset-normalizer==3.4.2
colorama==0.4.6
exceptiongroup==1.3.0
idna==3.10
iniconfig==2.1.0
packaging==25.0
pluggy==1.6.0
Pygments==2.19.1
pytest==8.4.0
requests==2.32.4
tomli==2.2.1
typing_extensions==4.14.0
urllib3==2.4.0
```
