import numpy as np
from typing import Tuple, Union


def widest_diameter(array: np.ndarray, threshold: Union[int, float], axis: int = 1) -> int:
    """
    Ищет строку/столбец с максимальным количеством элементов, отвечающих условию "array >= threshold",
    и возвращает количество этих элементов
    :param array: матрица
    :param threshold: порог (% в виде десятичной дроби: 10% == 0.1)
    :param axis: направление суммирования: по строкам строкам == 1, столбцам == 0
    :return: количество элементов
    """
    return np.max(np.sum(array >= array.max() * threshold, axis=axis))


def get_slice(array: np.ndarray, index: int, step: int = 1, xslice: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Возвращает сечение двумерной матрицы по указанно-му/-й столбцу/строчке с указанным шагом
    :param array: двумерная матрица
    :param index: номер столбца/строки
    :param step: шаг
    :param xslice: строка == True, столбец == False
    :return: (координатная сетка, сформированная с учетом шага; значения)
    """
    values = array[index, ::step] if xslice else array[::step, index]
    args = np.arange(0, values.size * step, step)
    return args, values


def calc_amplitude(array):
    return np.abs(np.max(array)) + np.abs(np.min(array))


def calculate_radius(s: Union[int, float], l: Union[int, float]) -> float:
    """
    Расчитывает значение радиуса окружности по известной стрелке прогиба и хорде.\n
    https://en.wikipedia.org/wiki/Sagitta_(geometry)
    :param s: стрелка прогиба
    :param l: хорда, на которую опирается дуга окружности, образующая стрелку
    :return: радиус окружности
    """
    return (s / 2) + (l ** 2 / (8 * s))
