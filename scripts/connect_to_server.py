import os
import paramiko
from scripts.get_token import get_token_env


class RemoteSQLExecutor:
    """
    Класс для выполнения SQL-запросов на удаленном сервере через SSH.
    """
    SSH_HOST = get_token_env('SSH_HOST')
    SSH_PORT = get_token_env('SSH_PORT')
    SSH_USER = get_token_env('SSH_USER')
    SSH_KEY_PATH = get_token_env('SSH_KEY_PATH')
    REMOTE_DB_PATH = get_token_env('REMOTE_DB_PATH')
    
    def __init__(self, host, port, username, private_key_path, remote_db_path):
        """
        Инициализация класса для выполнения SQL-запросов на удаленном сервере через SSH.

        :param host: Адрес удаленного сервера.
        :param port: Порт SSH (по умолчанию 22).
        :param username: Имя пользователя для подключения по SSH.
        :param private_key_path: Путь к приватному SSH-ключу.
        :param remote_db_path: Путь к SQLite3 базе данных на удаленном сервере.
        """
        self.host = self.SSH_HOST
        self.port = self.SSH_PORT
        self.username = self.SSH_USER
        self.private_key_path = os.path.expanduser(self.SSH_KEY_PATH)
        self.remote_db_path = self.REMOTE_DB_PATH

    def execute(self, sql_command):
        """
        Выполняет SQL-запрос на удаленном сервере через SSH.

        :param sql_command: SQL-запрос для выполнения.
        :return: Результат выполнения запроса.
        :raises Exception: Если произошла ошибка при выполнении запроса.
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(self.private_key_path)

        try:
            ssh.connect(self.host, self.port, self.username, pkey=private_key)
            stdin, stdout, stderr = ssh.exec_command(f'sqlite3 {self.remote_db_path} "{sql_command}"')
            result = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                raise Exception(f"Error executing SQL command: {error}")
            return result
        finally:
            ssh.close()

def main(db_name):
    # Пример использования класса для выполнения SQL-запроса на удаленном сервере
    remote_sql_executor = RemoteSQLExecutor()
    
    # Пример SQL-запроса
    sql_command = f"SELECT * FROM {db_name}"  # Замените на ваш SQL-запрос
    
    try:
        result = remote_sql_executor.execute(sql_command)
        print("Query result:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
