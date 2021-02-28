import matplotlib.pyplot as plt
import numpy as np

from ..areas.interface.aperture import Aperture
from ..configuration.interface.plotter import Plotter
from ..configuration.interface.saver import Saver
from ..waves.interface.wave import Wave
from ...utils.math import units


class OneWavePlotter(Plotter):

    def __init__(self, wave: Wave, aperture: Aperture, distance: float, saver: Saver):
        self.__wave = wave
        self.__aperture = aperture
        self.__z = distance
        self.__saver = saver

    def save_phase(self):
        focus = self.__wave.focal_len
        gaussian_width_param = self.__wave.gaussian_width_param
        k = 2 * np.pi / self.__wave.wavelength

        unwrapped_phase_lbl = f'[{np.min(self.__wave.get_unwrapped_phase(self.__aperture)[0]):.2f}, ' \
                              f'{np.max(self.__wave.get_unwrapped_phase(self.__aperture)[0]):.2f}] rad; ' \
                              f'[{np.min(self.__wave.get_unwrapped_phase(self.__aperture)[0]) * 1e+6 / k:.1f}, ' \
                              f'{np.max(self.__wave.get_unwrapped_phase(self.__aperture)[0]) * 1e+6 / k:.1f}] um'

        wrapped_phase_lbl = f'z: {units.m2mm(self.__z):.1f} mm; R: {self.__wave.get_wavefront_radius(self.__aperture):.3f} mm'

        fig = super().make_phase_plot(self.__wave.get_wrapped_phase(self.__aperture),
                                      self.__wave.get_unwrapped_phase(self.__aperture)[0], geometry_center=True, linewidth=1,
                                      unwrapped_ylims=(-100, 100), unwrapped_phase_lbl=unwrapped_phase_lbl,
                                      wrapped_phase_lbl=wrapped_phase_lbl)

        package_name = f'phase/phase_f{int(units.m2mm(np.around(focus, decimals=3)))}_' \
                       f'g{gaussian_width_param}_' \
                       f's{self.__wave.area.coordinate_grid[0].shape[0]}'

        filename = self.__saver.create_filename(self.__wave, 'phase', z=self.__z)
        self.__saver.save_image(fig, package_name, filename)
        plt.close(fig)

    def save_intensity(self):
        fig = super().make_intensity_plot(self.__wave.intensity)

        package_name = f'intensity/intensity_f{int(units.m2mm(np.around(self.__wave.focal_len, decimals=3)))}_' \
                       f'g{self.__wave.gaussian_width_param}_' \
                       f's{self.__wave.area.coordinate_grid[0].shape[0]}'
        filename = self.__saver.create_filename(self.__wave, 'intensity', z=self.__z)
        self.__saver.save_image(fig, package_name, filename)

        plt.close(fig)

    def save_aperture_bound(self, bound, **kwargs):
        dpi = kwargs.get('dpi', 300)
        line_widths = kwargs.get('linewidths', 3)
        labels = kwargs.get('labels', [])
        grid = kwargs.get('grid', True)
        x_label = kwargs.get('xlabel', 'x')
        y_label = kwargs.get('ylabel', 'y')
        y_scale = kwargs.get('yscale', 'linear')

        fig, ax = plt.subplots(figsize=[10.0, 8.0], dpi=dpi)

        data = super()._make_aperture_bound_dependency(self.__wave, self.__aperture, bound)

        for (x, y) in data:
            ax.plot(x, y, label=f'z: {units.m2mm(self.__z):.1f} mm; '
                                f'R: {self.__wave.get_wavefront_radius(self.__aperture):.3f} mm;'
                                f'D: {self.__aperture.aperture_diameter}')

        plt.legend(loc='upper right')
        ax.grid(grid)
        plt.title(f'f\' = {units.m2mm(np.around(self.wave.focal_len, decimals=3))} mm; '
                  f'g = {self.wave.gaussian_width_param}',
                  fontsize=14)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.yscale(y_scale)

        package_name = self.__saver.create_package_name('b')
        filename = self.__saver.create_filename(self.__wave, 'bound', z=self.__z)
        self.__saver.save_image(fig, package_name, filename)

        plt.close(fig)

    def save_r_z(self, matrix, step):
        """
        Данный метод может быть реализован для серии волна, а не для одной волны
        :return:
        """
        pass

    @property
    def wave(self):
        return self.__wave

    @wave.setter
    def wave(self, wave):
        self.__wave = wave

    @property
    def aperture(self):
        return self.__aperture

    @aperture.setter
    def aperture(self, aperture):
        self.__aperture = aperture

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, z):
        self.__z = z

    @property
    def saver(self):
        return self.__saver

    @saver.setter
    def saver(self, saver):
        self.__saver = saver
