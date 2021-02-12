import numpy as np


# интерфейс апертуры
class Aperture:
    def get_aperture(self) -> np.ndarray:
        """
        Возвращает матрицу поля вида:
        1 в пределах апертуры
        0 за пределами апертуры
        :return:
        """
        pass

    def get_aperture_diameter(self) -> float:
        """
        Возвращает размер апертуры
        :return:
        """
        pass
