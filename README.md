# Сервер авторизации и аутентификации

## Описание

Сервер позволяет производить регистрацию, авторизацию и аутентификацию пользователей.

После прохождения аутентификации пользователя, полученные токены добавляются в Куки.

При последующих запросах авторизация производится по данным из Куков.

Использование nginx в качестве API GateWay, позволяет проводить проверку валидности токена и пропускать запросы к другим сервисам.

## **Backend and infra**

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 3.9-slim
- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) 4.1.10
- ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) 3.14.0
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 14.4-alpine
- ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) 1.19.3

## Запуск проекта

1. склонировать проект
```
 git clone git@github.com:Aleksandr140590/django_authorization_server.git
```

2. Создать образ на основе докерфайла
```
docker build --tag auth-server:last -f ./infra/Dockerfile .
```
2. Перейти в каталог /infra/prod/

3. Создать .env файл на основе файла .env.example

4. Запустить docker-compose файл
```
docker compose up -d
```

После запуска доступ к localhost/admin/ закрыт для неавторизованного пользователя.

После прохождения токена по адресу localhost/auth/jwt/create/, он будет записан в Куки и доступ к админке будет доступен.

Запрет к админке сделан для примера, это ограничение может быть сделано для любого другого сервиса.
Использование SECRET_KEY в любом из сервисов позволит расшифровать передаваемые в токене данные и провести авторизацию
