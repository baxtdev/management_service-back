# Management Service Backend

Этот проект — backend-сервис на Django с поддержкой запуска как локально, так и через Docker.

---

## Требования

- Python 3.11+
- pip
- Docker и docker-compose
- (По умолчанию используется SQLite, но можно заменить на PostgreSQL)   

---

##  Установка и запуск

###  Вариант 1: Без Docker

#### 1. Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/baxtdev/management_service-back.git
cd management_service-back
```

#### 2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 3. Установите зависимости:

```bash
pip install -r requirements.txt
```

#### 4. Примените миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

#### 6. Запустите сервер разработки:

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

---

### Вариант 2: С использованием Docker

#### 1. Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/baxtdev/management_service-back.git
cd management_service-back
```

#### 2. Создайте `.env` файл:

```bash
cp .env.example .env
```

#### 3. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

#### 4. Примените миграции:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

#### 5. Создайте суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

Проект доступен по адресу:

[http://localhost:8000](http://localhost:8000)

---

## Полезные команды Docker

- Остановить контейнер:
  ```bash
  docker-compose down
  ```
- Перезапустить:
  ```bash
  docker-compose up --build
  ```

---

