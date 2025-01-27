import os
from dotenv import load_dotenv


def get_token_env(token_name):
    """
    Получает токен из переменных окружения
    :param token_name: Имя переменной окружения, содержащей токен
    :return: Токен
    """
    load_dotenv()
    # Проверяем, существует ли переменная окружения с именем token_name
    if not os.getenv(token_name):
        raise ValueError(f"{token_name} not found in environment variables.")

    return os.getenv(token_name)


if __name__ == '__main__':
    print(get_token_env('TOKEN'))