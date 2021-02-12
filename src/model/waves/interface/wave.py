import numpy as np

from src.model.areas.interface.aperture import Aperture


# интерфейс волны
class Wave:

    def get_wrapped_phase(self, aperture=None) -> np.ndarray:
        """
        Возвращает неразвернутую фазу волны
        :param aperture: апертура (circ) для обрезания поля
        :rtype: Aperture
        :return: матрица значений фаз
        """
        pass

    def get_unwrapped_phase(self, aperture=None) -> np.ndarray:
        """
        Возвращает развернутую фазу волны
        :param aperture: апертура (circ) для обрезания поля
        :rtype: Aperture
        :return: матрица значений фаз
        """
        pass

    def get_intensity(self) -> np.ndarray:
        """
        Возвращает интенсивность волны
        :return: матрица значений интенсивности
        """
        pass

    def get_wavefront_radius(self, aperture: Aperture) -> float:
        """
        Возвращает радиус волнового фронта, найденный по следующей формуле:
        r = (s / 2) + (l ** 2 / (8 * s))
        s - стрелка прогиба
        l - хорда, являющаяся диаметром апертуры
        :param aperture: апертура (circ) для обрезания поля
        :rtype: Aperture
        :return: радиус волнового фронта при заданной обрезающей апертуре
        """
        pass
