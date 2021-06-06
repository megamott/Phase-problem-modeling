import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from src.propagation.presenter.configuration.configurator import axes_configurator
from src.propagation.utils.math import units
from src.propagation.utils.math.general import get_slice


@axes_configurator
def make_intensity_x_slice_ax(ax, **kwargs):
    intensity = kwargs.get('intensity')
    geometry_center = kwargs.get('geometry_center')
    linewidth = kwargs.get('linewidth', 1.5)
    ymin, ymax = kwargs.get('ylims', [None, None])
    xmin, xmax = kwargs.get('xlims', [None, None])

    if geometry_center:
        max_indexes = [intensity.shape[0] // 2, intensity.shape[1] // 2]
    else:
        max_indexes = np.unravel_index(np.argmax(intensity, axis=None), intensity.shape)

    intensity_xslice_x, intensity_xslice_y = get_slice(intensity, max_indexes[0], xslice=True)
    intensity_xslice_x -= intensity_xslice_x[intensity_xslice_x.size // 2]

    ax.plot(intensity_xslice_x, intensity_xslice_y, linewidth=linewidth, label=f'x: {max_indexes[1]}')

    ax.title.set_text('x slice')
    ax.set_ylim([ymin, ymax])
    ax.set_xlim([xmin, xmax])
    ax.legend()


@axes_configurator
def make_intensity_y_slice_ax(ax, **kwargs):
    intensity = kwargs.get('intensity')
    geometry_center = kwargs.get('geometry_center')
    linewidth = kwargs.get('linewidth', 1.5)
    ymin, ymax = kwargs.get('ylims', [None, None])
    xmin, xmax = kwargs.get('xlims', [None, None])

    if geometry_center:
        max_indexes = [intensity.shape[0] // 2, intensity.shape[1] // 2]
    else:
        max_indexes = np.unravel_index(np.argmax(intensity, axis=None), intensity.shape)

    intensity_yslice_x, intensity_yslice_y = get_slice(intensity, max_indexes[1], xslice=False)
    intensity_yslice_x -= intensity_yslice_x[intensity_yslice_x.size // 2]

    ax.plot(intensity_yslice_x, intensity_yslice_y, linewidth=linewidth, label=f'y: {max_indexes[0]}')

    ax.title.set_text('y slice')
    ax.set_ylim([ymin, ymax])
    ax.set_xlim([xmin, xmax])
    ax.legend()


@axes_configurator
def make_intensity_color_ax(ax, **kwargs):
    intensity = kwargs.get('intensity')
    intensity_lbl = kwargs.get('intensity_lbl', '')  # mm
    cmap = kwargs.get('cmap', 'jet')

    img = ax.imshow(intensity, cmap=cmap,
                    extent=[-intensity.shape[1] // 2, intensity.shape[1] // 2,
                            -intensity.shape[0] // 2, intensity.shape[0] // 2])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img, cax=cax)

    ax.title.set_text(f'Intensity. {intensity_lbl}')
    ax.grid(False)


def __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase) -> (float, float):
    """
    Поиск максимальных по модулю координат для заданного центра: геометрического или энергетического
    """
    height, width = wrp_phase.shape
    if geometry_center:
        y_max, x_max = [height // 2, width // 2]
    else:
        abs_max = np.argmax(unwrp_phase)
        if np.abs(np.min(unwrp_phase)) > np.abs(np.max(unwrp_phase)):  # Отрицательный энергетический центр
            abs_max = np.argmin(unwrp_phase)
        y_max, x_max = np.unravel_index(abs_max, unwrp_phase.shape)
    return y_max, x_max


@axes_configurator
def make_wrp_phase_x_slice_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    wrapped_ymin, wrapped_ymax = kwargs.get('wrapped_ylims', [-np.pi, np.pi])
    linewidth = kwargs.get('linewidth', 1.5)
    grid_centering = kwargs.get('grid_centering', False)  # mm

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    wrp_phase_xslice_x, wrp_phase_xslice_y = get_slice(wrp_phase, x_max, xslice=True)

    # Центрирование координатной сетки
    if grid_centering:
        wrp_phase_xslice_x -= wrp_phase_xslice_x[wrp_phase_xslice_x.size // 2]  # plot()

    ax.title.set_text('x slice')
    ax.plot(wrp_phase_xslice_x, wrp_phase_xslice_y, linewidth=linewidth, label=f'x: {y_max}')
    ax.set_ylim([wrapped_ymin, wrapped_ymax])
    ax.legend()


@axes_configurator
def make_wrp_phase_y_slice_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    wrapped_ymin, wrapped_ymax = kwargs.get('wrapped_ylims', [-np.pi, np.pi])
    linewidth = kwargs.get('linewidth', 1.5)
    grid_centering = kwargs.get('grid_centering', False)  # mm

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    wrp_phase_yslice_x, wrp_phase_yslice_y = get_slice(wrp_phase, y_max, xslice=False)

    # Центрирование координатной сетки
    if grid_centering:
        wrp_phase_yslice_x -= wrp_phase_yslice_x[wrp_phase_yslice_x.size // 2]  # plot()

    ax.title.set_text('y slice')
    ax.plot(wrp_phase_yslice_x, wrp_phase_yslice_y, linewidth=linewidth, label=f'y: {x_max}')
    ax.set_ylim([wrapped_ymin, wrapped_ymax])
    ax.legend()


@axes_configurator
def make_unwrp_phase_x_slice_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    unwrapped_ymin, unwrapped_ymax = kwargs.get('unwrapped_ylims', [None, None])
    linewidth = kwargs.get('linewidth', 1.5)
    grid_centering = kwargs.get('grid_centering', False)  # mm
    xmin, xmax = kwargs.get('xlims', [None, None])

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    unwrp_phase_xslice_x, unwrp_phase_xslice_y = get_slice(unwrp_phase, x_max, xslice=True)

    # Центрирование координатной сетки
    if grid_centering:
        unwrp_phase_xslice_x -= unwrp_phase_xslice_x[unwrp_phase_xslice_x.size // 2]  # plot()

    ax.title.set_text('x slice')
    ax.plot(unwrp_phase_xslice_x, unwrp_phase_xslice_y, linewidth=linewidth, label=f'x: {y_max}')
    ax.set_ylim([unwrapped_ymin, unwrapped_ymax])
    ax.set_xlim([xmin, xmax])
    ax.legend()


@axes_configurator
def make_unwrp_phase_y_slice_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    unwrapped_ymin, unwrapped_ymax = kwargs.get('unwrapped_ylims', [None, None])
    linewidth = kwargs.get('linewidth', 1.5)
    grid_centering = kwargs.get('grid_centering', False)  # mm
    xmin, xmax = kwargs.get('xlims', [None, None])

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    unwrp_phase_yslice_x, unwrp_phase_yslice_y = get_slice(unwrp_phase, y_max, xslice=False)

    # Центрирование координатной сетки
    if grid_centering:
        unwrp_phase_yslice_x -= unwrp_phase_yslice_x[unwrp_phase_yslice_x.size // 2]  # plot()

    ax.title.set_text('y slice')
    ax.plot(unwrp_phase_yslice_x, unwrp_phase_yslice_y, linewidth=linewidth, label=f'y: {x_max}')
    ax.set_ylim([unwrapped_ymin, unwrapped_ymax])
    ax.set_xlim([xmin, xmax])
    ax.legend()


@axes_configurator
def make_wrp_phase_color_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    wrapped_phase_lbl = kwargs.get('wrapped_phase_lbl', '')  # mm
    grid_centering = kwargs.get('grid_centering', False)  # mm
    crosshair_halfwidth = kwargs.get('crosshair_halfwidth', 0)  # mm

    height, width = wrp_phase.shape

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    # Центрирование координатной сетки
    if grid_centering:
        extent = [-width // 2, width // 2, height // 2, -height // 2]  # imshow()
    else:
        extent = [0, width, height, 0]

    # Перекрестные линии для визуального различения заданного центра
    if crosshair_halfwidth != 0:
        wrp_phase = wrp_phase.copy()
        wrp_mean = (wrp_phase.max() - wrp_phase.min()) / 2
        wrp_phase[y_max - crosshair_halfwidth:y_max + crosshair_halfwidth, :] = wrp_mean
        wrp_phase[:, x_max - crosshair_halfwidth:x_max + crosshair_halfwidth] = wrp_mean

    img = ax.imshow(wrp_phase, extent=extent, cmap='jet')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img, cax=cax)

    ax.title.set_text(f'Wrapped. {wrapped_phase_lbl}')
    ax.grid(False)


@axes_configurator
def make_unwrp_phase_color_ax(ax, **kwargs):
    wrp_phase = kwargs.get('wrp_phase')
    unwrp_phase = kwargs.get('unwrp_phase')
    geometry_center = kwargs.get('geometry_center')
    unwrapped_phase_lbl = kwargs.get('unwrapped_phase_lbl', '')  # mm
    grid_centering = kwargs.get('grid_centering', False)  # mm
    crosshair_halfwidth = kwargs.get('crosshair_halfwidth', 0)  # mm

    height, width = wrp_phase.shape

    y_max, x_max = __find_max_coordinates(geometry_center, wrp_phase, unwrp_phase)

    # Центрирование координатной сетки
    if grid_centering:
        extent = [-width // 2, width // 2, height // 2, -height // 2]  # imshow()
    else:
        extent = [0, width, height, 0]

    # Перекрестные линии для визуального различения заданного центра
    if crosshair_halfwidth != 0:
        wrp_phase, unwrp_phase = wrp_phase.copy(), unwrp_phase.copy()
        unwrp_mean = (unwrp_phase.max() - unwrp_phase.min()) / 2
        unwrp_phase[y_max - crosshair_halfwidth:y_max + crosshair_halfwidth, :] = unwrp_mean
        unwrp_phase[:, x_max - crosshair_halfwidth:x_max + crosshair_halfwidth] = unwrp_mean

    img = ax.imshow(unwrp_phase, extent=extent, cmap='jet')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img, cax=cax)

    ax.title.set_text(f'Unwrapped. {unwrapped_phase_lbl}')
    ax.grid(False)


@axes_configurator
def make_r_z_ax(ax, **kwargs):
    array_wave_array = kwargs['array_wave_array'],
    array_aperture_array = kwargs['array_aperture_array'],
    z_array = kwargs['z_array'],
    matrix = kwargs['matrixes'],
    step = kwargs['step']

    array_wave_array = array_wave_array[0]
    array_aperture_array = array_aperture_array[0]
    z_array = z_array[0]
    matrix = matrix[0]

    marker = '-o'  # вид маркера линий
    markersize = kwargs.get('markersize', 2)  # размер марера линий
    linewidth = kwargs.get('linewidth', 1.)  # толщина линии графика реальных радиусов

    # определение реальных и теоретических радиусов кривизны волн и построение их графиков
    for z in np.arange(0, np.shape(matrix)[0], 1):
        radius_y = []
        theory_r_z = []
        waves = array_wave_array[z]
        apertures = array_aperture_array[z]
        for wave, aperture, k in zip(waves, apertures, z_array):
            radius_y.append(wave.get_wavefront_radius(aperture=aperture, z=z))
            theory_r_z.append(np.abs(np.array(k) - units.m2mm(wave.focal_len)))

        if z == 0:
            theory_r_z = np.abs(np.array(z_array) - units.m2mm(array_wave_array[0][0].focal_len))
            ax.plot(z_array, theory_r_z,
                    label='Theoretical',
                    color='k',
                    markersize=markersize)

        ax.plot(z_array, radius_y,
                marker,
                label=f'size: {matrix[z]}',
                linewidth=linewidth,
                markersize=markersize)

    #  определение масштаба графиков
    theory_r_z = np.abs(np.array(z_array) - units.m2mm(array_wave_array[0][0].focal_len))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, theory_r_z[-1])

    # заголовок графика
    ax.title.set_text(f'f\' = {units.m2mm(np.around(array_wave_array[0][0].focal_len, decimals=3))} mm; '
                      f'g = {array_wave_array[0][0].gaussian_width_param}; '
                      f'step = {step} mm')
    ax.legend()
