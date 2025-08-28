import os # noqa
from loguru import logger


def check_local_folder(path):
    import os
    if not os.path.exists(path):
        msg = f"Ошибка: локальная папка для синхронизации не найдена: {path}"
        print(msg)
        logger.error(msg)
        return False
    return True


def check_token(storage):
    try:
        storage.client.check_token()
        return True
    except Exception as e:
        msg = f"Ошибка: недействительный токен: {str(e)}"
        print(msg)
        logger.error(msg)
        return False


def check_remote_folder(storage):
    try:
        if not storage.is_dir(f"/{storage.remote_folder}"):
            msg = f"Ошибка: папка на удалённом хранилище не найдена: /{storage.remote_folder}"
            print(msg)
            logger.error(msg)
            return False
        return True
    except Exception as e:
        msg = f"Ошибка проверки папки на удалённом хранилище: {str(e)}"
        print(msg)
        logger.error(msg)
        return False
