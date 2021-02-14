import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage.restoration import unwrap_phase

from src.model.configuration.interface.saver import Saver
from src.model.waves.interface.wave import Wave
from src.utils.math.general import *
from src.utils.math import units


# сохранение изображения неразвернутой и развернутой фаз
def save_phase(z: float, wave: Wave, unwrapped_phase: np.ndarray, phase_z, wavefront_radius: float, saver: Saver):
    focus = wave.focal_len
    gaussian_width_param = wave.gaussian_width_param
    k = 2 * np.pi / wave.wavelength
    fn = f'phase_z_{int(units.m2mm(z))}mm'
    unwrapped_phase_lbl = f'[{np.min(unwrapped_phase):.2f}, {np.max(unwrapped_phase):.2f}] rad; ' \
                          f'[{np.min(unwrapped_phase) * 1e+6 / k:.1f}, {np.max(unwrapped_phase) * 1e+6 / k:.1f}] um'
    wrapped_phase_lbl = f'z: {units.m2mm(z):.1f} mm; R: {wavefront_radius:.3f} mm'
    save_phase_slices(phase_z, fn,
                      package_name=f'phase/phase_f{int(units.m2mm(np.around(focus, decimals=3)))}_'
                                   f'g{gaussian_width_param}_'
                                   f's{wave.area.coordinate_grid[0].shape[0]}_test',
                      saver=saver,
                      unwrapped=False, geometry_center=True, linewidth=1,
                      unwrapped_ylims=(-100, 100), unwrapped_phase_lbl=unwrapped_phase_lbl,
                      wrapped_phase_lbl=wrapped_phase_lbl)


def save_intensity(z: float, wave: Wave, saver: Saver):
    save_intensity_slices(wave.intensity, filename=f'intensity_z_{int(units.m2mm(z))}mm',
                          package_name=f'intensity/intensity_f{int(units.m2mm(np.around(wave.focal_len, decimals=3)))}_'
                                       f'g{wave.gaussian_width_param}_'
                                       f's{wave.area.coordinate_grid[0].shape[0]}_test', saver=saver)


def save_intensity_slices(intensity, filename: str, package_name: str, saver: Saver, geometry_center=False, **kwargs):
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

    saver.save_image(fig1, package_name, filename)

    plt.close(fig1)


def save_phase_slices(phase, filename: str, package_name: str, saver: Saver, unwrapped=True, geometry_center=False,
                      **kwargs):
    linewidth = kwargs.get('linewidth', 1.5)
    unwrapped_ymin, unwrapped_ymax = kwargs.get('unwrapped_ylims', [None, None])
    wrapped_ymin, wrapped_ymax = kwargs.get('wrapped_ylims', [-np.pi, np.pi])
    xmin, xmax = kwargs.get('xlims', [None, None])
    unwrapped_phase_lbl = kwargs.get('unwrapped_phase_lbl', '')  # mm
    wrapped_phase_lbl = kwargs.get('wrapped_phase_lbl', '')  # mm
    grid_centering = kwargs.get('grid_centering', False)  # mm
    crosshair_halfwidth = kwargs.get('crosshair_halfwidth', 0)  # mm

    # Свертывание / Развертывание фазы
    if unwrapped:
        uwrp_phase = phase
        wrp_phase = np.angle(np.exp(1j * uwrp_phase))
    else:
        wrp_phase = phase
        uwrp_phase = unwrap_phase(wrp_phase)

    height, width = phase.shape

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

    saver.save_image(fig1, package_name, filename)

    plt.close(fig1)


# сохранение графика R(z)
def save_r_z(array_of_z_distances: list, array_of_wavefront_radius_arrays: list,
             matrix: np.ndarray, wave: Wave, saver: Saver, start=None, stop=None, step=None):
    fig, ax = plt.subplots(figsize=[8.0, 6.0], dpi=300, facecolor='w', edgecolor='k')

    for z in np.arange(0, np.shape(matrix)[0], 1):
        radius_y = array_of_wavefront_radius_arrays[z]
        z_propagation_distance = array_of_z_distances[z]
        theory_r_z = np.abs(np.array(z_propagation_distance) - units.m2mm(wave.focal_len))

        if z == 0:
            ax.plot(z_propagation_distance, theory_r_z, label='Theoretical', color='k', markersize=3.)
        ax.plot(z_propagation_distance, radius_y, '-o', label=f'size: {matrix[z]}', linewidth=1., markersize=3.)

    # ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(20))
    #
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(20))

    theory_r_z = np.abs(np.array(array_of_z_distances[0]) - units.m2mm(wave.focal_len))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, theory_r_z[-1])

    plt.xlabel('Propagation distance, mm')
    plt.ylabel('R(z), mm', )
    plt.legend()
    plt.title(f'f\' = {units.m2mm(np.around(wave.focal_len, decimals=3))} mm; '
              f'g = {wave.gaussian_width_param}; step = {step} mm',
              fontsize=14)
    # plt.show()

    ax.grid(True)

    package_name = 'r(z)'
    filename = f'trz_f_{int(units.m2mm(np.around(wave.focal_len, decimals=3)))}_' \
               f'g{wave.gaussian_width_param}_matrix_test'

    saver.save_image(fig, package_name, filename)
