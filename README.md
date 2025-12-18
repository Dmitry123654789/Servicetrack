# ServiceTrack

Это корпоративная система учета и управления заявками на ремонт или обслуживание.
Его главная ценность — в централизации, прозрачности и контроле над потоком мелких проблем

## Предварительные требования

- [Python 3.12](https://www.python.org/downloads/)
- [Git](https://git-scm.com/install/)
- [Gettext](https://launchpad.net/gettext/+download)

## Установка и запуск

### 1. Клонирование репозитория и переход в папку проекта

```bash
git clone https://gitlab.crja72.ru/django/2025/autumn/course/projects/team-13.git
cd team-13
```

### 2. Создание и активация виртуального окружения

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

**Для разработки (dev режим):**

```bash
pip install -r requirements/dev.txt
```

*Включает все зависимости для разработки, включая инструменты для тестирования, линтеры и отладку.*

**Для production (prod режим):**

```bash
pip install -r requirements/prod.txt
```

*Содержит только минимальный набор пакетов, необходимых для работы приложения.*

**Для запуска тестов (test режим):**

```bash
pip install -r requirements/test.txt
```

*Включает зависимости для тестирования и проверки качества кода.*

### 4. Настройка переменных окружения

Создайте файл `.env` необходимые переменные.
Пример заполнения можно увидеть в файле `template.env`

**Для копирования настроек из template.env в .env:**

**Windows:**

```bash
copy template.env .env
```

**Mac/Linux:**

```bash
cp template.env .env
```

**После создания файла `.env` обязательно отредактируйте его, заполнив реальные значения переменных вместо
placeholder'ов.**

### 5. Переход в корень проекта

```bash
cd servicetrack
```

### 6. Создание базы данных

```bash
python manage.py migrate
```

**Создается файл db.sqlite3 в корне проекта.**

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Создание многоязычности

```bash
django-admin compilemessages
```

### 9. Сборка статических файлов

```bash
python manage.py collectstatic
```

**Команда собирает все статические файлы из проекта, включая файлы из каждого установленного приложения, и копирует их в
директорию, указанную в STATIC_ROOT.**

### 10. Запуск сервера

```bash
python manage.py runserver
```

## Загрузка тестовых данных

Для загрузки тестовых данных в базу данных выполните:

```bash
python manage.py loaddata fixtures/data.json
```

|Пользователь (Username)    |   Роль в системе  |   Главный управляющий (Organization)  | Рабочая группа (WorkerGroup)|
|-----------|-----------------------|-------------------|------------|
|director_a |   Директор            |   Организация A   |   —        |
|manager_a1 |   Руководитель группы |   Организация A   |   Группа A1|
|worker_a1  |   Работник            |   Организация A   |   Группа A1|
|manager_a  |   Руководитель группы |   Организация A   |   Группа A2|
|director_b |   Директор            |   Организация B   |   —        |
|manager_b1 |   Руководитель группы |   Организация B   |   Группа B1|
|worker_b1  |   Работник            |   Организация B   |   Группа B1|

Общий пароль для всех пользователей: testpassword
