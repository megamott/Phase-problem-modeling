import os
from typing import Any, Union, Tuple
import numpy as np


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


# todo после вызова функции я изменил матрицу, которую передавал в array и почему-то объект slice-а изменился!!!
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


def calculate_radius(s: Union[int, float], l: Union[int, float]) -> float:
    """
    Расчитывает значение радиуса окружности по известной стрелке прогиба и хорде.\n
    https://en.wikipedia.org/wiki/Sagitta_(geometry)
    :param s: стрелка прогиба
    :param l: хорда, на которую опирается дуга окружности, образующая стрелку
    :return: радиус окружности
    """
    return (s / 2) + (l ** 2 / (8 * s))


def calculate_sagitta(r, l):
    """Рассчет стрелки прогиба по известным радиусу r и хорде l"""
    return r - np.sqrt(r ** 2 - (l / 2) ** 2)


def calc_amplitude(array):
    return np.abs(np.max(array)) + np.abs(np.min(array))


def normalize(array: np.ndarray, **kwargs) -> np.ndarray:
    """
    Нормирует входной массив в диапазоне от new_min до new_max
    :param array:
    :param kwargs: old_min = min(array), old_max = max(array), new_min = 0., new_max = 1., dtype = np.float64
    :return:
    """
    if array.dtype in (np.complex64, np.complex128, np.csingle, np.cdouble, np.clongdouble):
        raise TypeError(f'Not implemented for complex-valued arrays: array.dtype = {array.dtype}')

    old_min = kwargs.get('old_min', np.min(array))
    old_max = kwargs.get('old_max', np.max(array))
    new_min = kwargs.get('new_min', 0.)
    new_max = kwargs.get('new_max', 1.)
    dtype = kwargs.get('dtype', np.float64)

    if old_max < old_min or new_max < new_min:
        raise ValueError(f'Значения максимумов должны превышать значения минимумов:'
                         f'old_min = {old_min}\nold_max = {old_max}\nnew_min = {new_min}\nnew_max = {new_max}')

    array = (array - old_min) / (old_max - old_min)  # from old_range to 0 ... 1.0
    array = array * (new_max - new_min) + new_min  # from 0 ... 1.0 to new_range

    return np.asarray(array, dtype=dtype)


def print_min_max(array: np.ndarray, array_name: str = 'array'):
    print(f'{np.min(array): >10.2e}{np.max(array): >10.2e} - {array_name}')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import tools.files_routine as fr

    # параметры цикла
    i_first = 0
    i_last = 11
    i_step = 1

    # параметры графиков
    step = 1
    linewidth = 1.
    ymin = None
    ymax = None
    xmin = 1200
    xmax = 1500
    xmax_width = None  # 550 - step
    xmax_height = None  # 550 - step

    # создание объекта фигуры и осей
    fig, (ax1, ax2) = plt.subplots(1, 2, dpi=100)

    basic_fp = r"\\hololab.ru\store\Проекты\2020 — РНФ (МУ)\5. Эксперименты\22.01.21 cs2100 v2"

    for i_num in range(i_first, i_last, i_step):
        print(i_num)

        # инициализируем пути к файлам
        im1_fp = os.path.join(basic_fp, f"{int(i_num)}.tif")
        # загружаем изображения
        if im1_fp[-3:] == 'npy':
            im1 = np.load(im1_fp)
        else:
            im1 = fr.load_image(im1_fp)

            # поиск индексов максимального элемента
        i1_max_indexes = np.unravel_index(np.argmax(im1, axis=None), im1.shape)

        # сечение 1-й интенсивности по энергетическому центру
        x1slice_val = im1[i1_max_indexes[0], ::step]
        y1slice_val = im1[::step, i1_max_indexes[1]]

        # создание координатной сетки
        xslice_coord = np.arange(0, im1.shape[1], step)
        yslice_coord = np.arange(0, im1.shape[0], step)

        # создание графиков
        ax1.plot(xslice_coord, x1slice_val, linewidth=linewidth, label=f'{i_num} mm')
        ax2.plot(yslice_coord, y1slice_val, linewidth=linewidth, label=f'{i_num} mm')

    # кастомизация графиков
    ax1.set_xlim([1266, 1321]), ax2.set_xlim([400, 455])
    # ax1.set_ylim([ymin, ymax]), ax2.set_ylim([ymin, ymax])
    ax1.set_xlabel('x'), ax2.set_xlabel('y')
    ax1.set_ylabel('Intensity'), ax2.set_ylabel('Intensity')
    ax1.grid(True), ax2.grid(True)
    ax1.legend(), ax2.legend()

    # сохранение графиков
    fp = os.path.join(fr.get_images_dir(), f'slices.png')
    print(fp)
    fig.savefig(fp)
    plt.show()
