from abc import ABC, abstractmethod
from matplotlib.figure import Figure

from ...waves.interface.wave import Wave


class Saver(ABC):
    """
    Интерфейс сохранения файлов в папку
    """

    @abstractmethod
    def save_image(self, fig: Figure, package_name: str, filename: str):
        """
        Сохраняет кратинку
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def create_filename(wave: Wave, method: str, z=False, it=False) -> str:
        """
        Создаёт имя файла по указанным параметрам типа:
        method_f..._g..._s..._it.png
        :param wave: волна
        :param method: тип графика
        :param z: в случае, если нужно передать дистанцию распространения
        :param it: в случае, если нужно передать какой-то итератор или любое другое дополнительное значение
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def create_folder_name(method: str) -> str:
        """
        Создаёт имя пакаета по указанному типу графика
        :param method: тип графика
        :return:
        """
        pass
