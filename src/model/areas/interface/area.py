import numpy as np


# интерфейс координатной сетки
class Area:
    def get_coordinate_grid(self) -> np.ndarray:
        """
        Возвращает сетку координат
        :return:
        """
        pass

    def get_pixel_size(self) -> float:
        """
        Возвращает размер пикселя
        :return:
        """
        pass
