from abc import ABC, abstractmethod

class BaseStorage(ABC):

    @abstractmethod
    def __init__(self, token: str, remote_folder: str):
        self.token = token
        self.remote_folder = remote_folder

    @abstractmethod
    def load(self, path: str):
        pass

    @abstractmethod
    def reload(self, path: str):
        pass

    @abstractmethod
    def delete(self, filename: str):
        pass

    @abstractmethod
    def get_info(self):
        pass