from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage.restoration import unwrap_phase

from ...areas.interface.aperture import Aperture
from ...waves.interface.wave import Wave
from ....utils.math import units
from ....utils.math.general import get_slice


# абстрактный класс строителя графиков
class Plotter(ABC):

    @abstractmethod
    def save_phase(self):
        """
        Сохраняет графики фаз
        :return:
        """
        pass

    @abstractmethod
    def save_intensity(self):
        """
        Сохраняет графики интенсивности
        :return:
        """
        pass

    @abstractmethod
    def save_aperture_bound(self, bound: float):
        """
        Сохраняет зависимости с пересечением скачка апертуры (с 0 на 1) с неразвернутой фазой волны
        :param bound: диапазон значений вблизи скачка апертуры (с 0 на 1)
        :return:
        """
        pass

    @abstractmethod
    def save_r_z(self, matrix, step):
        """
        Сохраняет графики зависимости радиуса волнового фронта от дистанции распространения волны
        :param step:
        :param matrix: изменяемый параметр в инициализации волны
        :return:
        """
        pass

    @staticmethod
    def make_intensity_plot(intensity, geometry_center=False, **kwargs):
        """
        Строит график с исчерпывающей информацией об интенсивности волны
        :return:
        """
        # title = kwargs.get('title', '')
        dpi = kwargs.get('dpi', 100)
        linewidth = kwargs.get('linewidth', 1.5)
        cmap = kwargs.get('cmap', 'jet')
        color_bar = kwargs.get('color_bar', True)
        # xlabel = kwargs.get('xlabel', 'x')
        # ylabel = kwargs.get('ylabel', 'y')
        ymin, ymax = kwargs.get('ylims', [None, None])
        xmin, xmax = kwargs.get('xlims', [None, None])
        intensity_lbl = kwargs.get('intensity_lbl', '')  # mm

        fig1 = plt.figure(dpi=dpi, figsize=(16, 9))
        ax1, ax2, ax3 = fig1.add_subplot(1, 3, 1), fig1.add_subplot(1, 3, 2), fig1.add_subplot(1, 3, 3)

        if geometry_center:
            max_indexes = [intensity.shape[0] // 2, intensity.shape[1] // 2]
        else:
            max_indexes = np.unravel_index(np.argmax(intensity, axis=None), intensity.shape)

        wrapped_phase_xslice_x, wrapped_phase_xslice_y = get_slice(intensity, max_indexes[0], xslice=True)
        wrapped_phase_yslice_x, wrapped_phase_yslice_y = get_slice(intensity, max_indexes[1], xslice=False)

        wrapped_phase_xslice_x -= wrapped_phase_xslice_x[wrapped_phase_xslice_x.size // 2]
        wrapped_phase_yslice_x -= wrapped_phase_yslice_x[wrapped_phase_yslice_x.size // 2]

        ax1.plot(wrapped_phase_xslice_x, wrapped_phase_xslice_y, linewidth=linewidth, label=f'x: {max_indexes[1]}')
        ax2.plot(wrapped_phase_yslice_x, wrapped_phase_yslice_y, linewidth=linewidth, label=f'y: {max_indexes[0]}')
        img = ax3.imshow(intensity, cmap=cmap,
                         extent=[-intensity.shape[1] // 2, intensity.shape[1] // 2,
                                 -intensity.shape[0] // 2, intensity.shape[0] // 2])

        if color_bar:
            divider = make_axes_locatable(ax3)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            plt.colorbar(img, cax=cax)

        ax1.title.set_text('x slice'), ax2.title.set_text('y slice')
        ax3.title.set_text(f'Intensity. {intensity_lbl}')

        [ax.set_ylim([ymin, ymax]) for ax in [ax1, ax2]]
        [ax.set_xlim([xmin, xmax]) for ax in [ax1, ax2]]
        [ax.legend() for ax in [ax1, ax2]]
        [ax.grid(True) for ax in [ax1, ax2]]

        return fig1

    @staticmethod
    def make_phase_plot(wrp_phase, uwrp_phase, geometry_center=False,
                        **kwargs):
        """
        Строит график с исчерпывающей информацией о фазе волны
        :return:
        """
        linewidth = kwargs.get('linewidth', 1.5)
        unwrapped_ymin, unwrapped_ymax = kwargs.get('unwrapped_ylims', [None, None])
        wrapped_ymin, wrapped_ymax = kwargs.get('wrapped_ylims', [-np.pi, np.pi])
        xmin, xmax = kwargs.get('xlims', [None, None])
        unwrapped_phase_lbl = kwargs.get('unwrapped_phase_lbl', '')  # mm
        wrapped_phase_lbl = kwargs.get('wrapped_phase_lbl', '')  # mm
        grid_centering = kwargs.get('grid_centering', False)  # mm
        crosshair_halfwidth = kwargs.get('crosshair_halfwidth', 0)  # mm

        height, width = wrp_phase.shape

        # Поиск максимальных по модулю координат для заданного центра: геометрического или энергетического
        if geometry_center:
            y_max, x_max = [height // 2, width // 2]
        else:
            abs_max = np.argmax(uwrp_phase)
            if np.abs(np.min(uwrp_phase)) > np.abs(np.max(uwrp_phase)):  # Отрицательный энергетический центр
                abs_max = np.argmin(uwrp_phase)
            y_max, x_max = np.unravel_index(abs_max, uwrp_phase.shape)

        # Поиск сечений по 2-м осям
        wrp_phase_xslice_x, wrp_phase_xslice_y = get_slice(wrp_phase, x_max, xslice=True)
        wrp_phase_yslice_x, wrp_phase_yslice_y = get_slice(wrp_phase, y_max, xslice=False)
        uwrp_phase_xslice_x, uwrp_phase_xslice_y = get_slice(uwrp_phase, x_max, xslice=True)
        uwrp_phase_yslice_x, uwrp_phase_yslice_y = get_slice(uwrp_phase, y_max, xslice=False)

        # Центрирование координатной сетки
        if grid_centering:
            wrp_phase_xslice_x -= wrp_phase_xslice_x[wrp_phase_xslice_x.size // 2]  # plot()
            wrp_phase_yslice_x -= wrp_phase_yslice_x[wrp_phase_yslice_x.size // 2]
            uwrp_phase_xslice_x -= uwrp_phase_xslice_x[uwrp_phase_xslice_x.size // 2]
            uwrp_phase_yslice_x -= uwrp_phase_yslice_x[uwrp_phase_yslice_x.size // 2]
            extent = [-width // 2, width // 2, height // 2, -height // 2]  # imshow()
        else:
            extent = [0, width, height, 0]

        # Перекрестные линии для визуального различения заданного центра
        if crosshair_halfwidth != 0:
            wrp_phase, uwrp_phase = wrp_phase.copy(), uwrp_phase.copy()
            wrp_mean = (wrp_phase.max() - wrp_phase.min()) / 2
            uwrp_mean = (uwrp_phase.max() - uwrp_phase.min()) / 2
            wrp_phase[y_max - crosshair_halfwidth:y_max + crosshair_halfwidth, :] = wrp_mean
            wrp_phase[:, x_max - crosshair_halfwidth:x_max + crosshair_halfwidth] = wrp_mean
            uwrp_phase[y_max - crosshair_halfwidth:y_max + crosshair_halfwidth, :] = uwrp_mean
            uwrp_phase[:, x_max - crosshair_halfwidth:x_max + crosshair_halfwidth] = uwrp_mean

        # Создание окна и 6-ти осей
        fig1 = plt.figure(figsize=(16, 9))
        ax1, ax2, ax3 = fig1.add_subplot(2, 3, 1), fig1.add_subplot(2, 3, 2), fig1.add_subplot(2, 3, 3)
        ax4, ax5, ax6 = fig1.add_subplot(2, 3, 4), fig1.add_subplot(2, 3, 5), fig1.add_subplot(2, 3, 6)

        ax1.plot(wrp_phase_xslice_x, wrp_phase_xslice_y, linewidth=linewidth, label=f'x: {y_max}')
        ax2.plot(wrp_phase_yslice_x, wrp_phase_yslice_y, linewidth=linewidth, label=f'y: {x_max}')
        img = ax3.imshow(wrp_phase, extent=extent, cmap='jet')
        divider = make_axes_locatable(ax3)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(img, cax=cax)

        ax4.plot(uwrp_phase_xslice_x, uwrp_phase_xslice_y, linewidth=linewidth, label=f'x: {y_max}')
        ax5.plot(uwrp_phase_yslice_x, uwrp_phase_yslice_y, linewidth=linewidth, label=f'y: {x_max}')
        img = ax6.imshow(uwrp_phase, extent=extent, cmap='jet')
        divider = make_axes_locatable(ax6)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(img, cax=cax)

        ax1.title.set_text('x slice'), ax2.title.set_text('y slice')
        ax4.title.set_text('x slice'), ax5.title.set_text('y slice')
        ax3.title.set_text(f'Wrapped. {wrapped_phase_lbl}')
        ax6.title.set_text(f'Unwrapped. {unwrapped_phase_lbl}')

        [ax.set_ylim([wrapped_ymin, wrapped_ymax]) for ax in [ax1, ax2]]
        [ax.set_ylim([unwrapped_ymin, unwrapped_ymax]) for ax in [ax4, ax5]]
        [ax.set_xlim([xmin, xmax]) for ax in [ax4, ax5]]
        [ax.legend() for ax in [ax1, ax2, ax4, ax5]]
        [ax.grid(True) for ax in [ax1, ax2, ax4, ax5]]

        return fig1

    @staticmethod
    def _make_aperture_bound_dependency(wave: Wave, aperture: Aperture, bound: float) -> (tuple, tuple):
        """
        Создаёт зависимость с пересечением скачка апертуры (с 0 на 1) с неразвернутой фазой волны
        :param wave: волна
        :param aperture: апертура
        :param bound: диапазон значений
        :return: два кортежа из массивов [x, y] значений неразвернутой фазы и апертуры в пределах скачка
        в указанном диапазоне (+- диапазон)
        """

        wrp_phase_x_slice_x, wrp_phase_x_slice_y = get_slice(
            wave.phase,
            wave.phase.shape[0] // 2,
            xslice=True
        )
        ap_x_slice_x, ap_x_slice_y = get_slice(
            aperture.aperture,
            aperture.aperture.shape[0] // 2,
            xslice=True
        )

        change_index = 0

        for i, v in enumerate(ap_x_slice_y):
            if v == 0:
                continue
            else:
                change_index = i
                break

        return (wrp_phase_x_slice_x[change_index - bound:change_index + bound],
                wrp_phase_x_slice_y[change_index - bound:change_index + bound]), \
               (ap_x_slice_x[change_index - bound:change_index + bound],
                ap_x_slice_y[change_index - bound:change_index + bound])

    @staticmethod
    def _make_r_z_dependency(wave: Wave, aperture: Aperture, z: float) -> (tuple, tuple):
        """
        Создаёт зависимость радиуса кривизны волнового фронта от расстояния
        :return:
        """

        return (z, wave.get_wavefront_radius(aperture)) + \
               (z, np.abs(z - units.m2mm(wave.focal_len)))



