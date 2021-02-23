from abc import abstractmethod
import numpy as np

from src.propagation.model.areas.interface.aperture import Aperture
from src.propagation.model.areas.interface.area import Area
from src.propagation.model.propagation.interface.propagate import Propagable


# интерфейс волны
class Wave(Propagable):

    @abstractmethod
    def get_wrapped_phase(self, aperture=None) -> np.ndarray:
        """
        Возвращает неразвернутую фазу волны
        :param aperture: апертура (circ) для обрезания поля
        :rtype: Aperture
        :return: матрица значений фаз
        """
        pass

    @abstractmethod
    def get_unwrapped_phase(self, aperture=None):
        """
        Возвращает развернутую фазу волны
        :param aperture: апертура (circ) для обрезания поля
        :rtype: Aperture
        :return: матрица значений фаз
        """
        pass

    @abstractmethod
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

    @property
    @abstractmethod
    def field(self) -> np.ndarray:
        """
        Распределение поля волны на координатной сетке в комплексной форме
        """
        pass

    @field.setter
    @abstractmethod
    def field(self, field):
        pass

    @property
    @abstractmethod
    def area(self) -> Area:
        """
        Координатная сетка
        """
        pass

    @area.setter
    @abstractmethod
    def area(self, area):
        pass

    @property
    @abstractmethod
    def phase(self) -> np.ndarray:
        """
        Распределение фазы поля волны
        :return:
        """
        pass

    @phase.setter
    @abstractmethod
    def phase(self, phase):
        pass

    @property
    @abstractmethod
    def intensity(self) -> np.ndarray:
        """
        Распределение интенсивности поля волны
        :return:
        """
        pass

    @intensity.setter
    @abstractmethod
    def intensity(self, intensity):
        pass

    @property
    @abstractmethod
    def wavelength(self) -> float:
        """
        Длина волны [м]
        :return:
        """
        pass

    @wavelength.setter
    @abstractmethod
    def wavelength(self, wavelength):
        pass

    @property
    @abstractmethod
    def focal_len(self) -> float:
        """
        Фокусное расстояние [м]
        :return:
        """
        pass

    @focal_len.setter
    @abstractmethod
    def focal_len(self, focal_len):
        pass

    # данный метод нужно убрать, так как не у всех волн в профиле интенсивности гауссоида
    @property
    @abstractmethod
    def gaussian_width_param(self) -> float:
        """
        Размер гауссоиды на уровне 1/e^2 в [px]
        :return:
        """
        pass

    @gaussian_width_param.setter
    @abstractmethod
    def gaussian_width_param(self, gaussian_width_param):
        pass


