from abc import ABC, abstractmethod
import numpy as np


# интерфейс апертуры
class Aperture(ABC):

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
        Размер апертуры
        :return:
        """
        pass
