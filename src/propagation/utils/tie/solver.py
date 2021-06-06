import numpy as np

from abc import ABC, abstractmethod
from typing import List, Union
from src.propagation.presenter.loader.loader import load_files
from src.propagation.utils.tie.boundary_conditions import BoundaryConditions, apply_volkov_scheme
from src.propagation.utils.math.derivative.finite_difference import central_2point


class TIESolver(ABC):
    """
    Абстрактный класс для решения TIE
    """

    def __init__(self, paths: List[str], dz: float, wavelength: Union[float, None], bc: BoundaryConditions):
        """
        :param paths: список с путям к файлам интенсивностей
        :param dz: шаг, м
        :param wavelength: длина волны когерентного излучения, м (None для частично-когерентного случая)
        :param bc: граничные условия
        """

        if len(paths) > 2:
            raise NotImplementedError(f'Expect 2 intensities, instead got {len(paths)}')

        self.__intensities = load_files(paths)
        self.__intensities = [apply_volkov_scheme(i, bc) for i in self.__intensities]

        self.__dz = dz
        self.__wavelenth = wavelength
        self.__boundary_condition = bc

        self.__axial_derivative = central_2point(*self.__intensities, dz)

    @abstractmethod
    def solve(self, threshold) -> np.ndarray:
        """
        :param threshold:
        :return: unwrapped phase
        """
        pass

    def add_threshold(self, threshold: float):
        """
        Пороговая обработка
        :param threshold:
        :return: Бинарная маска
        """
        if threshold == 0. or 0.0 in self.ref_intensity:
            raise ValueError(f'Нельзя делить на нулевые значения в интенсивности.')

        mask = self.ref_intensity < threshold

        # intensity = self.ref_intensity.copy()  # todo этот менто изменяет опорную интенсивность!!!
        self.ref_intensity[mask] = threshold
        return mask

    @property
    def intensities(self):
        return self.__intensities

    @property
    def ref_intensity(self):
        return self.__intensities[0]

    @property
    def dz(self):
        return self.__dz

    @property
    def wavelenth(self):
        return self.__wavelenth

    @property
    def axial_derivative(self):
        return self.__axial_derivative

    @property
    def boundary_condition(self):
        return self.__boundary_condition
