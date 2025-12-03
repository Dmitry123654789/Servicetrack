# Проект команды 13

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

### 5. Переход в корнень проекта

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

### 9. Сборка статическх файлов

```bash
python manage.py collectstatic
```

**Команда собирает все статические файлы из проекта, включая файлы из каждого установленного приложения, и копирует их в
директорию, указанную в STATIC_ROOT.**

### 10. Запуск сервера

```bash
python manage.py runserver
```

