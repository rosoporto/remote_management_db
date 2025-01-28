# Удаленное управление базой данных sqlite3 на linux сервере под управлением Ubuntu


## Описание

Этот проект предоставляет инструкции и скрипты для удаленного управления базой данных sqlite3 на linux сервере под управлением Ubuntu. Вы можете использовать этот метод для управления базой данных с удаленного компьютера. В данном примере используется протокол SSH для доступа к серверу и выполнения команд.

Пример БД с которой реализована работа:
```python
...
class UserUsage(db.Model):
    __tablename__ = 'user_usage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    username = db.Column(db.String, index=True, nullable=False)
    is_admin = db.Column(db.Integer, default=0)
    is_premium = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Integer, default=0)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ...
 
  ```


## Требования

- Установленный sqlite3 на удаленном сервере
- Установленный ssh на удаленном сервере
- Установленный ssh на локальном компьютере
- Доступ к удаленному серверу по SSH


## Основные функции

- **Поиск пользователей**: Поиск по `user_id` или `username`.
- **Редактирование данных**: Изменение количества попыток использования (`usage_count`).
- **Блокировка/разблокировка пользователей**: Возможность блокировки и разблокировки пользователей.
- **Управление через SSH**: Все операции с базой данных выполняются на удаленном сервере через SSH.


## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/rosoporto/remote_management_db.git
cd remote_management_db
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/MacOS
# или
venv\Scripts\activate     # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:

```bash
SSH_HOST=ip_адрес_сервера
SSH_PORT=22
SSH_USER=ваш_username_на_сервере
REMOTE_DB_PATH=/path/to/your/database.db
REMOTE_DB_NAME=имя_базы_данных
FLASK_SECRET_KEY=ваш_секретный_ключ
```

Убедитесь, что у вас есть SSH-ключи `id_rsa` и `id_rsa.pub` и они настроены для доступа к удаленному серверу.

### 5. Запуск приложения

```bash
python app.py
```

Приложение будет доступно по адресу `http://127.0.0.1:5000/`.


## Использование

Главная страница: Введите `user_id` или `username` в поле поиска и нажмите "Search".

Редактирование пользователя: После поиска вы попадете на страницу редактирования, где можно изменить количество попыток использования (usage_count).

Блокировка/разблокировка: На странице редактирования также можно заблокировать или разблокировать пользователя (TODO: реализовать блокировку).


## Компоненты проекта

`app.py`: Основной файл Flask-приложения.

`scripts/connect_to_server.py`: Класс RemoteSQLExecutor для выполнения SQL-запросов на удаленном сервере через SSH.

`scripts/get_token.py`: Утилита для получения переменных окружения.

`components/fields.py`: Список имен полей таблицы user_usage.

`templates/`: HTML-шаблоны для веб-интерфейса.