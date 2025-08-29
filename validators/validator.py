import os # noqa
from loguru import logger


def check_local_folder(path):
    import os
    if not os.path.exists(path):
        message = f"Ошибка: локальная папка для синхронизации не найдена: {path}"
        print(message)
        logger.error(message)
        return False
    return True


def check_token(storage):
    try:
        storage.client.check_token()
        return True
    except Exception as e:
        message = f"Ошибка: недействительный токен: {str(e)}"
        print(message)
        logger.error(message)
        return False


def check_remote_folder(storage):
    try:
        if not storage.is_dir(f"/{storage.remote_folder}"):
            message = f"Ошибка: папка на удалённом хранилище не найдена: /{storage.remote_folder}"
            print(message)
            logger.error(message)
            return False
        return True
    except Exception as e:
        message = f"Ошибка проверки папки на удалённом хранилище: {str(e)}"
        print(message)
        logger.error(message)
        return False
