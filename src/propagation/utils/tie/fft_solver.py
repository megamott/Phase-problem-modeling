import numpy as np

from typing import Tuple
from numpy.fft import fftshift
from src.propagation.utils.tie.solver import TIESolver
from src.propagation.utils.tie.boundary_conditions import BoundaryConditions, clip
from src.propagation.model.areas.square_area import CoordinateGrid
from src.propagation.utils.math.derivative.fourier import gradient_2d, ilaplacian_2d


class FFTSolver(TIESolver):
    """
    Решение TIE методом Фурье.
    D. Paganin and K. A. Nugent, Phys. Rev. Lett. 80, 2586 (1998).
    """

    def __init__(self, paths, dz, wavelength, pixel_size, bc=BoundaryConditions.NONE):
        super().__init__(paths, dz, wavelength, bc)
        self.__pixel_size = pixel_size
        self.__kx, self.__ky = self.get_frequency_coefs()
        # todo метод solve находится вне конструктура чтобы можно было заменить paths без удаления объекта

    def solve(self, threshold) -> np.ndarray:
        wave_number = 2 * np.pi / self.wavelenth
        eps = 2.2204e-16  # from MatLab 2.2204e-16
        reg_param = eps / self.pixel_size ** 4

        # Умножение на волновое число
        phase = -wave_number * self.axial_derivative

        # Первые Лапласиан и градиент
        phase = ilaplacian_2d(phase, self.kx, self.ky, reg_param, return_spacedomain=False)
        phase_x, phase_y = gradient_2d(phase, phase, self.kx, self.ky, space_domain=False)

        # Деление на опорную интенсивность
        mask = self.add_threshold(threshold)
        phase_x /= self.ref_intensity
        phase_y /= self.ref_intensity
        phase_x[mask], phase_y[mask] = 0, 0

        # Вторые Лапласиан и градиент
        phase_x, phase_y = gradient_2d(phase_x, phase_y, self.kx, self.ky)
        phase = ilaplacian_2d(phase_x + phase_y, self.kx, self.ky, reg_param)

        phase = clip(phase, self.boundary_condition)
        return phase

    def get_frequency_coefs(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Расчет частотных коэффициентов
        :return:
        """
        area = CoordinateGrid(*self.ref_intensity.shape, self.pixel_size)
        nu_y_grid, nu_x_grid = area.grid

        kx = 1j * 2 * np.pi * fftshift(nu_x_grid)
        ky = 1j * 2 * np.pi * fftshift(nu_y_grid)

        return kx, ky

    @property
    def pixel_size(self):
        return self.__pixel_size

    @property
    def kx(self):
        return self.__kx

    @property
    def ky(self):
        return self.__ky
