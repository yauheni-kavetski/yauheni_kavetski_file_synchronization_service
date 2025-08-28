import os

from loguru import logger

from .sync_utils import iter_files, iter_empty_dirs


def sync_empty_dirs(storage, local_folder):
    logger.info("Начинаем синхронизацию пустых папок")
    for local_dir in iter_empty_dirs(local_folder):
        relative_path = os.path.relpath(local_dir, local_folder)
        remote_path = f"/{storage.remote_folder}/{relative_path.replace(os.sep, '/')}"
        try:
            if not storage.is_dir(remote_path):
                storage.client.mkdir(remote_path)
                logger.info(f"Создана удаленная пустая директория: {remote_path}")
        except Exception as e:
            logger.error(f"Ошибка при создании пустой директории {remote_path}: {e}")


def remove_remote_empty_dirs(storage, local_folder):
    # Собираем папки с удалённого хранилища
    remote_dirs = get_remote_dirs(storage, f"/{storage.remote_folder}")
    remote_dirs.sort(key=len, reverse=True)
    for remote_dir in remote_dirs:
        relative_path = os.path.relpath(remote_dir, f"/{storage.remote_folder}")
        local_dir = os.path.join(local_folder, relative_path)
        if not os.path.exists(local_dir):
            try:
                storage.delete(remote_dir)
                logger.info(f"Удалена удаленная директория, которая не существует локально: {remote_dir}")
            except Exception as e:
                logger.error(f"Ошибка при удалении удаленной директории {remote_dir}: {e}")


def get_remote_dirs(storage, remote_folder):
    remote_dirs = []
    stack = [remote_folder]
    while stack:
        current_folder = stack.pop()
        try:
            for item in storage.client.listdir(current_folder):
                item_path = f"{current_folder}/{item.name}"
                if item.type == "dir":
                    remote_dirs.append(item_path)
                    stack.append(item_path)
        except Exception as e:
            logger.error(f"Ошибка при получении директорий {current_folder}: {str(e)}")
    return remote_dirs


def sync_folder(storage, local_folder):
    logger.info("Начинаем синхронизацию файлов")
    local_files = []
    for local_path in iter_files(local_folder):
        relative_path = os.path.relpath(local_path, local_folder)
        remote_path = f"/{storage.remote_folder}/{relative_path.replace(os.sep, '/')}"
        local_files.append(remote_path)
        try:
            if not storage.client.exists(remote_path):
                storage._ensure_remote_dirs(remote_path)
                storage.load(local_path)
            else:
                remote_info = storage.client.get_meta(remote_path)
                local_size = os.path.getsize(local_path)
                remote_size = remote_info.size if hasattr(remote_info, 'size') else -1
                if local_size != remote_size:
                    storage.reload(local_path)
        except Exception as e:
            logger.error(f"Ошибка загрузки {remote_path}: {str(e)}")

    # Получаем все файлы удалённого хранилища
    remote_files = storage.get_info()

    # Удаляем файлы отсутствующие локально
    for remote_file in remote_files:
        if remote_file not in local_files:
            try:
                storage.delete(remote_file)
                logger.info(f"Удален удаленно расположенный файл, который отсутствует локально: {remote_file}")
            except Exception as e:
                logger.error(f"Ошибка удаления удаленно расположенного файла {remote_file}: {str(e)}")

    remove_remote_empty_dirs(storage, local_folder)
