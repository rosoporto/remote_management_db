import os
from dotenv import load_dotenv


def get_token_env(token_name):
    """
    Получает токен из переменных окружения.
    :param token_name: Имя переменной окружения, содержащей токен.
    :return: Токен.
    :raises ValueError: Если переменная окружения не найдена.
    """
    # Загружаем переменные из .env с перезаписью существующих
    load_dotenv(override=True)

    # Проверяем, существует ли переменная окружения с именем token_name
    token_value = os.getenv(token_name)
    if token_value is None:
        raise ValueError(f"{token_name} not found in environment variables.")

    return token_value


# Пример использования
if __name__ == "__main__":
    try:
        ssh_user = get_token_env("SSH_USER")
        print(f"SSH_USER: {ssh_user}")
    except ValueError as e:
        print(e)