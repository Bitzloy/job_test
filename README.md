# Запуск приложения
* выполнить команду `make up`
* выполнить миграцию `make migrate`


Приложение будет доступно по URL http://localhost:5000
Пример запроса к Api curl -X 'POST' http://127.0.0.1:5000/api/v1/wallets/4f61d89f-cb81-43af-ba36-f33e37f9a3d7/operation -d '{"operation_type":"DEPOSIT","amount":1000 }' -H "Content-Type: application/json; charset=UTF-8"

# Как запустить тесты
* `make test`

# Запустить форматирование PEP8
* `make cs_docker`