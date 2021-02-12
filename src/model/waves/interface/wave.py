import numpy as np

from src.model.areas.interface.aperture import Aperture
from src.model.areas.interface.area import Area


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

    def get_wavelength(self) -> float:
        """
        Возвращает длину волны в метрах
        :return:
        """
        pass

    def get_area(self) -> Area:
        """
        Возвращает координатную сетку волны
        :return:
        """
        pass

    def get_focus(self) -> float:
        """
        Возвращает фокусное расстояние
        :return:
        """
        pass

    # данный метод нужно убрать, так как не у всех волн в профиле интенсивности гауссоида
    def get_gaussian_width(self) -> float:
        """
        Возвращает размер гауссоиды на уровне 1/e^2 в [px]
        :return:
        """