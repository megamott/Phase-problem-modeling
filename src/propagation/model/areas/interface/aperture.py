from abc import ABC, abstractmethod
import numpy as np


class Aperture(ABC):
    """
    Интерфейс апертур
    """

    @property
    @abstractmethod
    def aperture(self) -> np.ndarray:
        """
        Матрица поля вида:
        1 в пределах апертуры
        0 за пределами апертуры
        :return:
        """
        pass

    @property
    @abstractmethod
    def aperture_diameter(self) -> float:
        """
        Диаметр апертуры
        :return:
        """
        pass

    @aperture_diameter.setter
    @abstractmethod
    def aperture_diameter(self, aperture_diameter):
        """
        Изменение диаметра апертуры
        :param aperture_diameter:
        :return:
        """
        pass
