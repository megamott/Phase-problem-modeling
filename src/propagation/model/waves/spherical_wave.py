from icecream import ic
import numpy as np
from numpy.fft import fft2, fftshift, ifft2
from skimage.restoration import unwrap_phase

from ..areas.radial_aperture import RadialAperture
from ..areas.radial_area import RadialArea
from ...utils.math import units
from ...model.waves.interface.wave import Wave
from ...model.areas.interface.aperture import Aperture
from ...model.areas.interface.area import Area
from ...utils.optic.field import gauss_2d
from ...utils.math.general import get_slice
from ...utils.math.general import calc_amplitude
from ...utils.math.general import calculate_radius


# класс волны со сферической аберрацией или сходящейся сферической волны
class SphericalWave(Wave):

    def __init__(self, area: Area, focal_len: float, gaussian_width_param: int, wavelength: float, distance: float):
        """
        Создание распределения поля на двухмерной координатной сетке
        :param area: двухмерная координатная сетка расчёта распределения поля
        :param focal_len: фокусное расстояние [м]
        :param gaussian_width_param: ширина гауссоиды на уровне интенсивности 1/e^2 [px]
        :param wavelength: длина волны [м]
        :param distance дистанция, на которую распространилась волна из начала координат [м]
        """

        self.__area = area
        self.__focal_len = focal_len
        self.__gaussian_width_param = gaussian_width_param
        self.__wavelength = wavelength
        self.__distance = distance

        # задание распределения интенсивности волны
        y_grid, x_grid = self.__area.coordinate_grid
        gaussian_width_param = units.px2m(gaussian_width_param, px_size_m=area.pixel_size)
        self.__intensity = gauss_2d(x_grid, y_grid,
                                    wx=gaussian_width_param / 4,
                                    wy=gaussian_width_param / 4)

        # волновой вектор
        k = 2 * np.pi / self.__wavelength
        # задание распределения комлексной амплитуды поля
        radius_vector = np.sqrt(x_grid ** 2 + y_grid ** 2 + focal_len ** 2)
        self.__field = np.sqrt(self.__intensity) * np.exp(-1j * k * radius_vector)

        # задание распределения фазы волны
        self.__phase = np.angle(self.__field)

    def get_wrapped_phase(self, aperture=None) -> np.ndarray:
        if aperture:
            return self.__phase * aperture.aperture
        else:
            return self.__phase

    def get_unwrapped_phase(self, aperture=None):
        if aperture:

            # оптимизация апертуры для правильного разворачивания фазы
            # второй подоход через свёрнутую фазу
            aperture = self.__modify_aperture(aperture)

            return unwrap_phase(self.__phase * aperture.aperture), aperture
        else:
            return unwrap_phase(self.__phase)

    def __modify_aperture(self, aperture: Aperture):
        """
        Метод модификации апертуры для правильного разворачивания фазы
        :param aperture: изначальная апертура
        :return: модифицированная апертура
        """
        wrp_phase_values = get_slice(
            self.__phase,
            self.__phase.shape[0] // 2,
        )[1]

        ap_values = get_slice(
            aperture.aperture,
            aperture.aperture.shape[0] // 2,
        )[1]

        # Х координата скачка апертуры с 0 на 1
        jump = next((i for i, v in enumerate(ap_values) if v == 1),
                    None)

        # ближайшая к скачку апертуры координата Х слева от скачка
        # в кторой значение неразвернутой фазы наиболее близко к нулю
        lwrp = next((i for i in range(jump, 0, -1) if (wrp_phase_values[i] > 0) and (wrp_phase_values[i - 1] < 0)),
                    None)

        # ближайшая к скачку апертуры координата Х справа от скачка
        # в кторой значение неразвернутой фазы наиболее близко к нулю
        rwrp = next((i for i in range(jump, 0, -1) if (wrp_phase_values[i] > 0) and (wrp_phase_values[i - 1] < 0)),
                    None)

        # определение, какая из нулевых координат неразвернутой фазы ближе к скачку
        jump = rwrp if lwrp - jump > rwrp - jump else lwrp

        # генерация новой апертуры с скорректированным диаметром
        # в случае, если волна сходящаяся, вводится дополнительная корректировка
        new_aperture_diameter = (self.__area.coordinate_grid[0].shape[0] // 2 - jump) * 2
        new_aperture_diameter += 2 if self.__distance < self.__focal_len else False
        radial_area = RadialArea(self.__area)
        new_aperture = RadialAperture(radial_area, new_aperture_diameter)

        return new_aperture

    def get_wavefront_radius(self, aperture: Aperture) -> float:
        # развернутая фаза, обрезанная апертурой
        cut_phase, new_aperture = self.get_unwrapped_phase(aperture=aperture)

        # преобразование развернутой фазы для устранения ошибок
        # первый подход через развернутую фазу
        # mask2 = cut_phase == 0
        # cut_phase[mask2] = np.max(cut_phase)
        # cut_phase -= cut_phase.min()
        # cut_phase[mask2] = 0

        # поиск стрелки прогиба
        amplitude = calc_amplitude(cut_phase)
        sagitta = units.rad2mm(amplitude, self.__wavelength)

        # определение радиуса кривизны волнового фронта
        ap_diameter = units.m2mm(new_aperture.aperture_diameter)
        wavefront_radius = calculate_radius(sagitta, ap_diameter)

        return wavefront_radius

    def propagate_on_distance(self, z: float, method='angular_spectrum'):
        if method == 'angular_spectrum':
            self.__angular_spectrum_propagation(z)

    def __angular_spectrum_propagation(self, z: float):
        """
        Метод распространения (преобразования) волны методом углового спектра
        :param z: дистанция распространения
        :return:
        """

        height = self.__field.shape[0]  # количество строк матрицы
        width = self.__field.shape[1]  # количество элеметов в каждой строке матрицы

        # волновое число
        wave_number = 2 * np.pi / self.__wavelength

        # создание сетки в частотной области при условии выполнения теоремы Котельникова
        nu_x = np.arange(-width / 2, width / 2) / (width * self.__area.pixel_size)
        nu_y = np.arange(-height / 2, height / 2) / (height * self.__area.pixel_size)
        nu_x_grid, nu_y_grid = np.meshgrid(nu_x, nu_y)

        # сдвиг высоких частот к краям сетки
        nu_x_grid, nu_y_grid = fftshift(nu_x_grid), fftshift(nu_y_grid)

        # Фурье-образ исходного поля
        field = fft2(self.__field)

        # передаточная функция слоя пространства
        exp_term = np.sqrt(
            1 - (self.__wavelength * nu_x_grid) ** 2 -
            (self.__wavelength * nu_y_grid) ** 2)
        h = np.exp(1j * wave_number * z * exp_term)

        # обратное преобразование Фурье
        self.__field = ifft2(field * h)

        self.__phase = np.angle(self.__field)
        self.__intensity = np.abs(self.__field) ** 2

    @property
    def field(self) -> np.ndarray:
        return self.__field

    @property
    def area(self) -> Area:
        return self.__area

    @property
    def phase(self) -> np.ndarray:
        return np.angle(self.__field)

    @property
    def intensity(self) -> np.ndarray:
        return np.abs(self.__field) ** 2

    @property
    def wavelength(self) -> float:
        return self.__wavelength

    @property
    def focal_len(self) -> float:
        return self.__focal_len

    @property
    def gaussian_width_param(self) -> float:
        return self.__gaussian_width_param

    @property
    def distance(self) -> float:
        return self.__distance

    @field.setter
    def field(self, field):
        self.__field = field

    @area.setter
    def area(self, area):
        self.__area = area

    @wavelength.setter
    def wavelength(self, wavelength):
        self.__wavelength = wavelength

    @gaussian_width_param.setter
    def gaussian_width_param(self, gaussian_width_param):
        self.__gaussian_width_param = gaussian_width_param

    @focal_len.setter
    def focal_len(self, focal_len):
        self.__focal_len = focal_len

    @intensity.setter
    def intensity(self, intensity):
        self.__intensity = intensity

    @phase.setter
    def phase(self, phase):
        self.__phase = phase
