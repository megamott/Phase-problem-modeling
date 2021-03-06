import numpy as np
from numpy.fft import fft2, fftshift, ifft2, ifftshift

from src.propagation.model.waves.interface.wave import Wave
from src.propagation.utils.optic.field import rect_2d


def angular_spectrum_propagation(wave: Wave, z: float):
    """
    Метод распространения (преобразования) волны методом углового спектра
    :param wave: волна
    :param z: дистанция распространения
    :return:
    """

    height = wave.field.shape[0]  # количество строк матрицы
    width = wave.field.shape[1]  # количество элеметов в каждой строке матрицы

    # волновое число
    wave_number = 2 * np.pi / wave.wavelength

    # создание сетки в частотной области при условии выполнения теоремы Котельникова
    nu_x = np.arange(-width / 2, width / 2) / (width * wave.area.pixel_size)
    nu_y = np.arange(-height / 2, height / 2) / (height * wave.area.pixel_size)
    nu_x_grid, nu_y_grid = np.meshgrid(nu_x, nu_y)

    # сдвиг высоких частот к краям сетки
    nu_x_grid, nu_y_grid = fftshift(nu_x_grid), fftshift(nu_y_grid)

    # Фурье-образ исходного поля
    field = fft2(wave.field)

    # передаточная функция слоя пространства
    exp_term = np.sqrt(
        1 - (wave.wavelength * nu_x_grid) ** 2 -
        (wave.wavelength * nu_y_grid) ** 2)
    h = np.exp(1j * wave_number * z * exp_term)

    # обратное преобразование Фурье
    wave.field = ifft2(field * h)

    wave.phase = np.angle(wave.field)
    wave.intensity = np.abs(wave.field) ** 2


def angular_spectrum_bl_propagation(wave: Wave, z: float):
    """
    Распространение (преобразование) волны при помощи band-limited angular spectrum метода
    :param wave: волна
    :param z: дистанция распространения
    :return:
    """

    # Увеличение транспаранта в 2 раза для трансформации линейной свертки в циклическую
    # (периодические граничные условия)
    height = 2 * wave.field.shape[0]  # количество строк матрицы
    width = 2 * wave.field.shape[1]  # количество элеметов в каждой строке матрицы

    # Индексы для "старого" поля
    left = int(width * .25)
    right = int(width * .75)
    top = int(height * .25)
    bottom = int(height * .75)

    # Вписываем "старое" поле в новое
    new_field = np.zeros((height, width), dtype=wave.field.dtype)
    new_field[top:bottom, left:right] = wave.field

    # Сетка в частотной области
    nu_x = np.arange(-width / 2, width / 2) / (width * wave.area.pixel_size)
    nu_y = np.arange(-height / 2, height / 2) / (height * wave.area.pixel_size)
    nu_x_grid, nu_y_grid = np.meshgrid(nu_x, nu_y)
    nu_x_grid, nu_y_grid = ifftshift(nu_x_grid), ifftshift(nu_y_grid)
    nu_z_grid = np.sqrt(wave.wavelength ** -2 - nu_x_grid ** 2 - nu_y_grid ** 2)
    nu_z_grid[nu_x_grid ** 2 + nu_y_grid ** 2 > wave.wavelength ** -2] = 0

    # Расчет граничных частот U/V_limit
    dnu_x = 1 / (width * wave.area.pixel_size)
    dnu_y = 1 / (height * wave.area.pixel_size)
    nu_x_limit = 1 / (np.sqrt((2 * dnu_x * z) ** 2 + 1) * wave.wavelength)
    nu_y_limit = 1 / (np.sqrt((2 * dnu_y * z) ** 2 + 1) * wave.wavelength)

    # Передаточная функция (угловой спектр)
    h_clipper = rect_2d(nu_x_grid, nu_y_grid, wx=2 * nu_x_limit, wy=2 * nu_y_limit)
    h = np.exp(1j * 2 * np.pi * nu_z_grid * z) * h_clipper

    # обратное преобразование Фурье
    wave.field = ifft2(fft2(new_field) * h)[top:bottom, left:right]

    wave.phase = np.angle(wave.field)
    wave.intensity = np.abs(wave.field) ** 2
