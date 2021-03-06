import numpy as np


def gauss_2d(x, y, a=1., wx=1., wy=1., x0=0., y0=0.):
    """
    Возвращает 2-мерную гауссоиду с явно указанной амплитудой
    :param x: np.ndarray 2-мерная координатная сетка по оси X
    :param y: np.ndarray 2-мерная координатная сетка по оси Y
    :param a: Union[float, int] амплитуда
    :param wx: Union[float, int] ширина по оси X (может выступаить как СКО)
    :param wy: Union[float, int] ширина по оси Y (может выступаить как СКО)
    :param x0: Union[float, int] смещение относительно нуля координат по оси X
    :param y0: Union[float, int] смещение относительно нуля координат по оси Y
    :return: np.ndarray
    """
    return a * np.exp(-((x - x0) ** 2 / (2 * wx ** 2) + (y - y0) ** 2 / (2 * wy ** 2)))


def rect_1d(x, a=1., w=1., x0=0.):
    """
    Возвращает 1-мерную прямоугольную функцию
    :param x: np.ndarray координатная сетка
    :param a: Union[float, int] амплитуда
    :param w: Union[float, int] ширина
    :param x0: Union[float, int] смещение относительно нуля координат
    :return: np.ndarray
    """
    return a * (np.abs((x - x0) / w) < 0.5)


def rect_2d(x, y, a=1., wx=1., wy=1., x0=0., y0=0.):
    """
    Возвращает 2-мерную прямоугольную функцию
    :param x: np.ndarray 2-мерная координатная сетка по оси X
    :param y: np.ndarray 2-мерная координатная сетка по оси Y
    :param a: Union[float, int] амплитуда
    :param wx: Union[float, int] ширина по оси X
    :param wy: Union[float, int] ширина по оси Y
    :param x0: Union[float, int] смещение относительно нуля координат по оси X
    :param y0: Union[float, int] смещение относительно нуля координат по оси Y
    :return: np.ndarray
    """
    return a * (rect_1d(x, w=wx, x0=x0) * rect_1d(y, w=wy, x0=y0))


def circ(r, a=1., w=1., r0=0.):
    return a * rect_1d(r, w=w, x0=r0)


def circ_cartesian(x, y, a=1., w=1., x0=0., y0=0.):
    return a * ((np.sqrt((x - x0) ** 2 + (y - y0) ** 2) / w) < 0.5)
