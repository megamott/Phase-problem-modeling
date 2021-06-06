import numpy as np


def central_4point(p_minus2, p_minus1, p_plus1, p_plus2, h: float = 1.):
    """

    :param p_minus2:
    :param p_minus1:
    :param p_plus1:
    :param p_plus2:
    :param h: Шаг между СОСЕДНИМИ точками!
    :return:
    """
    return (p_minus2 - 8 * p_minus1 + 8 * p_plus1 - p_plus2) / (12 * h)


def central_2point(p_minus, p_plus, h):
    """

    :param p_minus:
    :param p_plus:
    :param h: 2*h = distance(p_plus - p_minus)
    :return:
    """
    if isinstance(p_minus, np.ndarray) and isinstance(p_plus, np.ndarray):
        if p_minus.shape != p_plus.shape:
            raise ValueError(f"Arrays shapes must be equal: {p_minus.shape} != {p_plus.shape}")
        return (p_plus - p_minus) / (2 * h)
    else:
        raise NotImplementedError("Implemented only for ndarrays")


def forward_2point(p, p_plus, h):
    if isinstance(p, np.ndarray) and isinstance(p_plus, np.ndarray):
        if p.shape != p_plus.shape:
            raise ValueError(f"Arrays shapes must be equal: {p.shape} != {p_plus.shape}")
        return (p_plus - p) / h
    else:
        raise NotImplementedError("Implemented only for ndarrays")


def backward_2point(p_minus, p, h):
    if isinstance(p, np.ndarray) and isinstance(p_minus, np.ndarray):
        if p.shape != p_minus.shape:
            raise ValueError(f"Arrays shapes must be equal: {p.shape} != {p_minus.shape}")
        return (p - p_minus) / h
    else:
        raise NotImplementedError("Implemented only for ndarrays")

