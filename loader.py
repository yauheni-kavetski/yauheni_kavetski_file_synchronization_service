import time

from loguru import logger

from config_data import config
from logs.logger_setup import setup_logging
from storage.yandex_storage import YandexStorage
from sync.sync_manager import sync_folder, sync_empty_dirs
from validators.validator import check_local_folder, check_token, check_remote_folder


def main():
    setup_logging()
    logger.info(
        f"Программа запущена. Синхронизация папки: {config.LOCAL_FOLDER}")
    print("Синхронизация запущена")

    storage = YandexStorage(config.YA_TOKEN, config.REMOTE_FOLDER)

    if not check_local_folder(config.LOCAL_FOLDER) or not check_token(
            storage) or not check_remote_folder(storage):
        print("Исправьте ошибки и перезапустите программу.")
        return False

    while True:
        logger.info("Началась новая итерация синхронизации")
        sync_empty_dirs(storage, config.LOCAL_FOLDER)
        sync_folder(storage, config.LOCAL_FOLDER)
        time.sleep(config.SYNC_INTERVAL)


if __name__ == "__main__":
    main()
