![workflow](https://github.com/IvanCh-dev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

IP сервера 84.201.158.76

# Api-Yamdb
### Описание
Проект Yamdb собирает отзывы пользователей на различные произведения.
### Технологии
Django Rest Framework
Python 3.7,
Django 2.2.16,
JWT
### Создание docker-compose и запуск проекта в dev-режиме
- 1) Клонировать репозиторий и перейти в него в командной строке
```bash
git clone git@github.com:IvanCh-dev/infra_sp2.git
```

 - 2) Перейти в ./infra и запустить docker-compose
```
сd infra
docker-compose up
```

 - 3) Выполнить миграции
```
docker-compose exec web python manage.py migrate
```

И  теперь наслаждайтесь нашей работой с командой))

Проект будет доступен по адресу http://localhost/

### Авторы
https://github.com/Vihapp
https://github.com/Evstigneefff
https://github.com/IvanCh-dev
