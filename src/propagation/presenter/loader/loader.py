import numpy as np

from typing import List
from PIL import Image
from src.propagation.utils.math.general import normalize


def load_files(paths: List[str]) -> List[np.ndarray]:
    """
    Возвращает список матриц интенсивностей, загруженных из файлов
    :param paths: список путей к файлам
    :return:
    """
    first_path = paths[0]

    if first_path[-3:] == 'npy':
        return [np.load(path) for path in paths]
    else:
        return [load_image(path) for path in paths]


def load_image(path: str) -> np.ndarray:
    """
    Загружает изображение, конвертирует его в numpy.ndarray (dtype=np.float64), приводит к динамическому диапазону
    [0.0 ... 1.0].
    Цветные изображения конвертируются в полутоновые.
    :param path: путь к файлу
    :return матрица
    """
    gray_8bit = 'L'
    gray_16bit = 'I;16'

    img = Image.open(path)
    gray_mode = img.mode

    if gray_mode == gray_8bit:
        old_max = 2 ** 8 - 1  # 255

    elif gray_mode == gray_16bit:
        old_max = 2 ** 16 - 1  # 65 535

    else:  # color-image
        img = img.convert(gray_8bit)
        old_max = 2 ** 8 - 1

    return normalize(np.asarray(img, np.float64), old_min=0, old_max=old_max)
