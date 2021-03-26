# django_yandex
Django REST API сервис, который позволяет нанимать курьеров на работу, принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.
### Инструкция по развёртыванию:
1. Установить [Docker](https://docs.docker.com/get-docker/)
2. Установить [Docker-Compose](https://docs.docker.com/compose/install/)
3. Для запуска сервера выполнить команду `docker-compose up -d --build` в директории Relese_back_v1.
### Использованные инструменты:
1. Docker и Docker Compose для сборки и развёртывания проекта
2. Фреймворк Django
3. Cerberus 
4. PostgreSQL

### Реализованные методы:
1. POST /couriers
2. PATCH /couriers/$courier_id
3. POST /orders
4. POST /orders/assign
5. POST /orders/complete
6. GET /couriers/$courier_id <br>
[Документация на методы](/openapi.yaml)
### Тестирование
При запуске сервера автоматически запускаются тесты из [tests.py](/djangoProject/djangoProject/tests.py)<br>
