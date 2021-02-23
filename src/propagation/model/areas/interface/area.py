from abc import ABC, abstractmethod
import numpy as np


# интерфейс координатной сетки
class Area(ABC):

    @property
    @abstractmethod
    def coordinate_grid(self) -> np.ndarray:
        """
        Сетка координат
        :return:
        """
        pass

    @property
    @abstractmethod
    def pixel_size(self) -> float:
        """
        Размер пикселя
        :return:
        """
        pass
