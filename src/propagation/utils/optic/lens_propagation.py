import os
from datetime import datetime
import numpy as np
from skimage.restoration import unwrap_phase
import tools.math.general as math
from tools.optic.propagation import fresnel
from tools.optic.field import circ


DATA_NOW = datetime.now().strftime('%d.%m.%y')
TIME_NOW = datetime.now().strftime('%H_%M_%S')
OUTPUT_DIR = fr'lens_propagation {DATA_NOW}'
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

show_lens_plot = 1
show_initfield_phase = 1
show_initfield_intensity = 1
show_zfield = 1


def lens_tf(X, Y, focal_length, radius, wavelength) -> np.ndarray:
    """
    lens Transmittance Function - функция пропускания тонкой линзы
    :param X: координаты зрачка в [m]
    :param Y: координаты зрачка в [m]
    :param focal_length: фокусное расстояние в [m]
    :param radius: световой радиус в [m]
    :param wavelength: длина волны в [m]
    :return:
    """
    aperture = circ(np.sqrt(X**2 + Y**2), w=2*radius).astype(np.complex128)
    phase_coef = np.exp(-1j * np.pi * (X**2 + Y**2) / (wavelength * focal_length))  # todo откуда-то берутся круги!
    return aperture * phase_coef


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # исходные параметры
    width = 250
    height = 250
    focal_len = 100e-3
    wavelength = 0.5e-6
    delimiter = 8
    px_size = 5.04e-6
    z = 100e-3
    w = (width / 4) * px_size

    # создание координатной сетки
    Y, X = np.mgrid[-height/2:height/2, -width/2:width/2] * px_size

    # инициализация поля
    # phase = np.pi * np.ones((height, width), dtype=np.float64)
    r = np.sqrt(X**2 + Y**2)
    intensity = circ(r, w=w)
    # intensity = rect_2d(X, Y, wx=w, wy=w)
    field_init = np.sqrt(intensity) #* np.exp(1j * phase)
    field = np.asarray(field_init, dtype=np.complex128)

    if show_initfield_intensity:
        fig1 = plt.figure(figsize=(12, 4))
        ax1 = fig1.add_subplot(1, 4, 1)
        ax2 = fig1.add_subplot(1, 4, 2)
        ax3 = fig1.add_subplot(1, 4, 3, projection='3d')
        ax4 = fig1.add_subplot(1, 4, 4)

        intensity = np.abs(field_init) ** 2
        intensity_xslice_x, intensity_xslice_y = math.get_slice(intensity, intensity.shape[0] // 2, xslice=True)
        intensity_yslice_x, intensity_yslice_y = math.get_slice(intensity, intensity.shape[1] // 2, xslice=False)

        ax1.plot(intensity_xslice_x, intensity_xslice_y)
        ax2.plot(intensity_yslice_x, intensity_yslice_y)
        ax3.plot_surface(X, Y, intensity, cmap="jet", antialiased=False)
        ax4.imshow(intensity)

        ax1.title.set_text('intensity x slice (z=0)')
        ax2.title.set_text('intensity y slice (z=0)')
        ax3.title.set_text('intensity 3d (z=0)')
        ax4.title.set_text('intensity (z=0)')

    # преобразование поля линзой
    lens_coef = lens_tf(X, Y, focal_len, w, wavelength)
    field *= lens_coef

    start = 130e-3
    stop = 135e-3
    step = 5e-3
    for z in np.arange(start, stop, step):
        print(z)
        # распространение волны через слой пространства
        field_z = fresnel(field, z, wavelength, px_size)

        intensity_z = np.abs(field_z) ** 2
        phase_z = unwrap_phase(np.angle(field_z))

        if show_zfield:
            fig3 = plt.figure(figsize=(9, 7))
            ax1 = fig3.add_subplot(2, 3, 1)
            ax2 = fig3.add_subplot(2, 3, 2)
            ax3 = fig3.add_subplot(2, 3, 3)
            ax4 = fig3.add_subplot(2, 3, 4)
            ax5 = fig3.add_subplot(2, 3, 5)
            ax6 = fig3.add_subplot(2, 3, 6)

            intensity_xslice_x, intensity_xslice_y = math.get_slice(intensity_z, intensity_z.shape[0] // 2, xslice=True)
            intensity_yslice_x, intensity_yslice_y = math.get_slice(intensity_z, intensity_z.shape[1] // 2, xslice=False)
            phase_xslice_x, phase_xslice_y = math.get_slice(phase_z, phase_z.shape[0] // 2, xslice=True)
            phase_yslice_x, phase_yslice_y = math.get_slice(phase_z, phase_z.shape[1] // 2, xslice=False)

            ax1.plot(intensity_xslice_x, intensity_xslice_y, label=f'x slice')
            ax2.plot(intensity_yslice_x, intensity_yslice_y, label=f'y slice')
            ax3.imshow(intensity_z)

            ax4.plot(phase_xslice_x, phase_xslice_y, label=f'x slice')
            ax5.plot(phase_yslice_x, phase_yslice_y, label=f'y slice')
            ax6.imshow(phase_z)

            ax1.title.set_text('intensity_z')
            ax2.title.set_text('intensity_z')
            ax3.title.set_text(f'intensity z={z * 1e+3}mm')
            ax4.title.set_text('phase_z x')
            ax5.title.set_text('phase_z y')
            ax6.title.set_text(f'phase z={z * 1e+3}mm')

            [ax.legend() for ax in [ax1, ax2, ax4, ax5]]
            [ax.grid(True) for ax in [ax1, ax2, ax4, ax5]]

            fp = os.path.join(OUTPUT_DIR, f'z_{z * 1e+3:.1f} mm {TIME_NOW}.PNG')
            fig3.savefig(fp)
            plt.close(fig3)

        if show_lens_plot:
            fig5 = plt.figure(figsize=(12, 4))
            ax1 = fig5.add_subplot(1, 4, 1)
            ax2 = fig5.add_subplot(1, 4, 2)
            ax3 = fig5.add_subplot(1, 4, 3, projection='3d')
            ax4 = fig5.add_subplot(1, 4, 4)

            lens_phase = np.angle(lens_coef)
            # lens_phase = np.unwrap(lens_phase)
            lens_phase = unwrap_phase(lens_phase)
            phase_xslice_x, phase_xslice_y = math.get_slice(lens_phase, lens_phase.shape[0] // 2, xslice=True)
            phase_yslice_x, phase_yslice_y = math.get_slice(lens_phase, lens_phase.shape[1] // 2, xslice=False)

            ax1.plot(phase_xslice_x, phase_xslice_y, label=f'x slice')
            ax2.plot(phase_yslice_x, phase_yslice_y, label=f'y slice')
            ax3.plot_surface(X, Y, lens_phase, cmap="jet", antialiased=False)
            ax4.imshow(lens_phase)

            ax1.title.set_text('phase x slice')
            ax2.title.set_text('phase y slice')
            ax3.title.set_text('lens phase 3d')
            ax4.title.set_text('lens phase')

    plt.show()
