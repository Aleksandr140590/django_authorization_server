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
'''
 git clone git@github.com:Aleksandr140590/django_authorization_server.git
'''
