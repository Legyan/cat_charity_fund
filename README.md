# Cat Charity Fund
Приложение благотворительного фонда поддержки котиков

### Описание:
Cat Charity Fund - это API для сбора средств, разработанное для поддержки различных целевых проектов, в том числе направленных на помощь популяции кошек. 

Фонд может одновременно вести несколько целевых проектов. У каждого проекта есть название, описание и целевая сумма для сбора. Проекты финансируются по очереди, когда проект набирает необходимую сумму и закрывается, пожертвования начинают поступать в следующий проект.

Пользователи могут делать ненаправленные пожертвования и сопровождать их комментарием. Пожертвования делаются в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который еще не набрал нужную сумму. Если пожертвование больше требуемой суммы или в фонде нет открытых проектов, оставшиеся средства будут ждать открытия следующего проекта.

Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml.

### Стек технологий 

![](https://img.shields.io/badge/Python-3.9-black?style=flat&logo=python) 
![](https://img.shields.io/badge/FastAPI-0.78.0-black?style=flat&logo=fastapi)
![](https://img.shields.io/badge/Pydantic-1.9.1-black?style=flat)
![](https://img.shields.io/badge/SQLAlchemy-1.4.29-black?style=flat)

### Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Legyan/cat_charity_fund.git
```

```
cd cat_charity_fund
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Создать в корневой директории файл .env и заполнить его:

```
nano .env
```

```
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=<YOUR_SECRET_WORD>
FIRST_SUPERUSER_EMAIL=<SUPERUSER_EMAIL>
FIRST_SUPERUSER_PASSWORD=<SUPERUSER_PASSWORD>
```

5. Выполнить миграции:

```
alembic upgrade head
```

6. Запустить приложение:

```
uvicorn app.main:app
```

### Примеры запросов к API:

#### Получение всех благотворительных проектов

Запрос:
```
GET /charity_project
```

Ответ:
```
[
    {
      "id": 1,
      "name": "Помощь приюту котиков",
      "description": "Сбор средств на покупку корма и медицинских принадлежностей для приюта котиков",
      "full_amount": 30000,
      "invested_amount": 30000,
      "create_date": "2023-04-08T17:40:31.733Z",
      "close_date": "2023-04-0917:44:55.733Z",
      "fully_invested": true
    },
    {
      "id": 2,
      "name": "Постройка нового приюта",
      "description": "Помощь в постройке нового дома для бездомных кошек",
      "full_amount": 30000,
      "invested_amount": 15000,
      "create_date": "2023-04-09T15:32:05.337Z",
      "close_date": null,
      "fully_invested": false
    }
]
```

#### Cоздание нового благотворительного проекта:

Запрос:
```
POST /charity_project
{
  "name": "Помощь ветеринарной клинике",
  "description": "Сбор средств на покупку оборудования для ветеринарной клиники",
  "full_amount": 35000
}
```

Ответ:
```
{
    "id": 3,
    "name": "Помощь ветеринарной клинике",
    "description": "Сбор средств на покупку оборудования для ветеринарной клиники",
    "full_amount": 35000,
    "invested_amount": 0,
    "create_date": "2023-04-08T17:47:37.460Z",
    "is_closed": false
}

```

#### Cоздание пожертвования:

Запрос:
```
POST /donation
{
  "full_amount": 1500,
  "comment": "Спасите котиков!"
}
```

Ответ:
```
{
    "id": 1,
    "full_amount": 1500,
    "comment": "Спасите котиков!",
    "create_date": "2023-04-08T17:51:13.382Z"
}

```

#### Получение списка всех пожертвований пользователя:

Запрос:
```
GET /donation/my
```

Ответ:
```
[
    {
      "id": 1,
      "full_amount": 300,
      "comment": "На корм",
      "create_date": "2023-04-08T17:54:16.054Z"
    }
]
```

Полная документация API со всеми возможными запросами доступна на развёрнутом проекте по адресам [```http://localhost/api/docs/```](http://localhost/api/docs/) или [```http://localhost/api/redoc/```](http://localhost/api/redoc/).
