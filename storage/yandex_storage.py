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
        try:
            remote_path = self._remote_path(path)
            self._ensure_remote_dirs(remote_path)
            self.client.upload(path, remote_path)
            logger.info(f"Загружен новый файл: {remote_path}")
        except FileNotFoundError:
            logger.error(f"Локальный файл для загрузки не найден: {path}")
        except PermissionError:
            logger.error(f"Нет прав для доступа к файлу: {path}")
        except yadisk.exceptions.YaDiskError as e:
            logger.error(f"Ошибка при загрузке файла {remote_path}: {e}")
        except OSError as e:
            logger.error(f"Системная ошибка при загрузке файла {remote_path}: {e}")

    def reload(self, path: str):
        try:
            remote_path = self._remote_path(path)
            self.client.remove(remote_path, permanently=True)
            self.load(path)
            logger.info(f"Перегружен файл: {remote_path}")
        except yadisk.exceptions.YaDiskError as e:
            logger.error(f"Ошибка при перезагрузке файла {remote_path}: {e}")
        except OSError as e:
            logger.error(f"Системная ошибка при перезагрузке файла {remote_path}: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при перезагрузке файла {remote_path}: {e}")


    def delete(self, remote_path: str):
        try:
            self.client.remove(remote_path, permanently=True)
            logger.info(f"Удален файл/папка: {remote_path}")
        except FileNotFoundError:
            logger.error(f"Файл/папка не найдены для удаления: {remote_path}")
        except PermissionError:
            logger.error(f"Нет прав на удаление: {remote_path}")
        except yadisk.exceptions.YaDiskError as e:  # конкретное исключение библиотеки yadisk
            logger.error(f"Ошибка Yandex Disk API при удалении {remote_path}: {e}")
        except OSError as e:
            logger.error(f"Системная ошибка при удалении {remote_path}: {e}")

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
            except yadisk.exceptions.YaDiskError as e:
                logger.error(f"Ошибка при получении содержимого {current}: {e}")
            except OSError as e:
                logger.error(f"Системная ошибка при получении содержимого {current}: {e}")
        return files

    def is_dir(self, remote_path: str):
        try:
            return self.client.is_dir(remote_path)
        except yadisk.exceptions.YaDiskError as e:
            logger.error(f"Ошибка при проверке директории {remote_path}: {e}")
            return False
        except OSError as e:
            logger.error(f"Системная ошибка при проверке директории {remote_path}: {e}")
            return False

    def _remote_path(self, local_path: str) -> str:
        relative = os.path.relpath(local_path, os.path.abspath(config.LOCAL_FOLDER))
        return f"/{self.remote_folder}/{relative.replace(os.sep, '/')}"

    def _ensure_remote_dirs(self, remote_path: str):
        parts = remote_path.strip("/").split("/")
        directories = parts[:-1]
        current = ""
        for directory in directories:
            current += f"/{directory}"
            if not self.is_dir(current):
                try:
                    self.client.mkdir(current)
                    logger.info(f"Создана удаленная директория: {current}")
                except yadisk.exceptions.YaDiskError as e:
                    logger.error(f"Ошибка при создании директории {current}: {e}")
                except OSError as e:
                    logger.error(f"Системная ошибка при создании директории {current}: {e}")
