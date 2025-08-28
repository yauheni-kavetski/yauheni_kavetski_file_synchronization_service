import os


def iter_files(base_folder):
    for root, _, files in os.walk(base_folder):
        for file in files:
            yield os.path.join(root, file)


def iter_empty_dirs(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if not dirs and not files:
            yield root
