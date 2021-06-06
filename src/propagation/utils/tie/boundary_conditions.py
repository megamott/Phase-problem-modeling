import enum
import numpy as np


@enum.unique
class BoundaryConditions(enum.Enum):
    DIRICHLET = enum.auto()
    NEUMANN = enum.auto()
    PERIODIC = enum.auto()
    NONE = enum.auto()


def apply_volkov_scheme(array: np.ndarray, condition: BoundaryConditions) -> np.ndarray:
    """
    Генерирует массив в 2 раза больше array, заполняя площадь отражённым array по различным направлениям.
    Volkov mirror-padding scheme - DOI: 10.1117/12.2020662
    :param array:
    :param condition:
    :return: mirrored_array
    """

    h, w = array.shape
    m_array = np.zeros((h * 2, w * 2), dtype=array.dtype)  # mirrored

    array_lr = np.fliplr(array)
    array_ud = np.flipud(array)
    array_udlr = np.fliplr(array_ud)

    if condition == BoundaryConditions.DIRICHLET:
        m_array[0: h:, w: 2 * w:] = -array_lr  # право-верх
        m_array[h: 2 * h:, 0: w:] = -array_ud  # лево-низ

    elif condition == BoundaryConditions.NEUMANN:
        m_array[0: h:, w: 2 * w:] = array_lr  # право-верх
        m_array[h: 2 * h:, 0: w:] = array_ud  # лево-низ

    elif condition == BoundaryConditions.PERIODIC:
        raise NotImplementedError

    elif condition == BoundaryConditions.NONE:
        return array

    m_array[0: h:, 0: w:] = array
    m_array[h: 2 * h:, w: 2 * w:] = array_udlr  # право-низ

    return m_array


def clip(mirrored_array: np.ndarray, condition: BoundaryConditions) -> np.ndarray:
    """
    Вырезает исходную часть (2-й квадрант) из отражённого массива
    :param mirrored_array:
    :param condition:
    :return:
    """
    if condition in [BoundaryConditions.DIRICHLET, BoundaryConditions.NEUMANN]:
        h, w = mirrored_array.shape
        clipped_array = mirrored_array[0:h // 2, 0:w // 2]
        return clipped_array

    else:
        return mirrored_array

