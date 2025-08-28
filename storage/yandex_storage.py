import os

import yadisk
from loguru import logger

from config_data import config
from .base_storage import BaseStorage


class YandexStorage(BaseStorage):
    def __init__(self, token: str, remote_folder: str):
        super().__init__(token, remote_folder)
        self.client = yadisk.YaDisk(token=token)

    def load(self, path: str):
        remote_path = self._remote_path(path)
        self._ensure_remote_dirs(remote_path)
        self.client.upload(path, remote_path)
        logger.info(f"Загружен новый файл: {remote_path}")

    def reload(self, path: str):
        remote_path = self._remote_path(path)
        self.client.remove(remote_path, permanently=True)
        self.load(path)
        logger.info(f"Перегружен файл: {remote_path}")

    def delete(self, remote_path: str):
        try:
            self.client.remove(remote_path, permanently=True)
            logger.info(f"Удален файл/папка: {remote_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении {remote_path}: {str(e)}")

    def get_info(self):
        files = []
        stack = [f"/{self.remote_folder}"]
        while stack:
            current = stack.pop()
            try:
                for item in self.client.listdir(current):
                    item_path = f"{current}/{item.name}"
                    if item.type == "dir":
                        stack.append(item_path)
                    else:
                        files.append(item_path)
            except Exception as e:
                logger.error(f"Ошибка при получении содержимого {current}: {str(e)}")
        return files

    def is_dir(self, remote_path: str):
        try:
            return self.client.is_dir(remote_path)
        except Exception as e:
            logger.error(f"Ошибка при проверке директории {remote_path}: {str(e)}")
            return False

    def _remote_path(self, local_path: str) -> str:
        relative = os.path.relpath(local_path, os.path.abspath(config.LOCAL_FOLDER))
        return f"/{self.remote_folder}/{relative.replace(os.sep, '/')}"

    def _ensure_remote_dirs(self, remote_path: str):
        parts = remote_path.strip("/").split("/")
        dirs = parts[:-1]
        current = ""
        for d in dirs:
            current += f"/{d}"
            if not self.is_dir(current):
                try:
                    self.client.mkdir(current)
                    logger.info(f"Создана удаленная директория: {current}")
                except Exception as e:
                    logger.error(f"ошибка при создании директории {current}: {e}")
