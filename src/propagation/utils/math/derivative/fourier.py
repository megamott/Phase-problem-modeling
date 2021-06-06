from numpy.fft import fft2, ifft2
from numpy import ndarray, real
"""
Псевдо-дифференциальные операторы, реализованные через FFT.
Первоисточник: D. Paganin "Coherent X-Ray Imaging" p.299-300 2006
"""

norm = None


def gradient_2d(f_x: ndarray,
                f_y: ndarray,
                kx: ndarray,
                ky: ndarray,
                space_domain: bool = True) -> (ndarray, ndarray):
    """
    Возвращает сумму частных производных первого порядка (функция градиента) от функции f.
    :param f_x: array-like двумерная функция
    :param f_y: array-like двумерная функция
    :param kx: частотный коэффициент 1j * 2*np.pi * fftshift(nu_x_grid)
    :param ky: частотный коэффициент 1j * 2*np.pi * fftshift(nu_y_grid)
    :param space_domain:
    :return: array-like градиент от функции f
    """
    if space_domain:
        f_x = fft2(f_x, norm=norm)
        f_y = fft2(f_y, norm=norm)

    return real(ifft2(f_x * kx, norm=norm)), real(ifft2(f_y * ky, norm=norm))


def ilaplacian_2d(f: ndarray,
                  kx: ndarray,
                  ky: ndarray,
                  reg_param: float,
                  return_spacedomain: bool = True) -> ndarray:
    """
    Возвращает сумму частных производных минус второго порядка (обратный Лапласиан) от функции f.
    :param f: array-like двумерная функция
    :param kx: частотный коэффициент 1j * 2*np.pi * fftshift(nu_x_grid)
    :param ky: частотный коэффициент 1j * 2*np.pi * fftshift(nu_y_grid)
    :param reg_param: нужен, чтобы избежать деления на ноль
    :param return_spacedomain:
    :return: array-like градиент от функции f
    """
    res = fft2(f, norm=norm) * (kx**2 + ky**2) / (reg_param + (kx**2 + ky**2)**2)

    if return_spacedomain:
        res = real(ifft2(res, norm=norm))

    return res


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from numpy.fft import fft, ifft, ifftshift, fftfreq
    from tools.optic.field import *
    from tools.math.units import *

    fig = plt.figure()
    ax = fig.gca()
    ax2 = ax.twinx()

    width = 2000
    a = 1
    r0 = 100e-3
    wavelength = 659e-9
    pixel_size = 5.04e-6
    dx = pixel_size
    wave_number = 2 * np.pi / wavelength

    x0 = np.arange(-width / 2, width / 2) * pixel_size
    x2 = np.arange(-width, width) * pixel_size

    for z in range(5, 6, 35):
        for w in [750]:

            f = gauss_1d(x0, a=a, w=px2m(w)/4, x0=px2m(0))
            aperture = rect_1d(x0, w=px2m(width - 10))

            # todo
            # f2 = np.zeros((x0.size * 2))
            # f2[:f.size] = f
            # f2[f.size:] = f[::-1]
            # f, x = f2, x2
            x = x0

            r = np.sqrt(x ** 2 + r0 ** 2)
            phase = wave_number * r

            field = np.sqrt(f) * np.exp(-1j * phase)# * aperture

            nu_x = fftfreq(f.size, d=dx)
            kx = 1j * 2 * np.pi * nu_x
            exp_term = np.sqrt(1 - (wavelength * nu_x) ** 2)
            h = np.exp(1j * wave_number * mm2m(z) * exp_term)

            field_z = ifft(fft(field) * h)
            f_z, phase_z = np.abs(field_z) ** 2, np.angle(field_z)

            np_gradient = np.gradient(f_z, dx)
            fft_gradient = ifft(fft(f_z) * kx)
            fft_gradient_real = real(ifft(fft(f_z) * kx))

            error = np.abs(fft_gradient-np_gradient)
            # error_real = np.abs(fft_gradient_real-np_gradient)
            # error[error < 1e-20] = 1e-15

            # ax.plot(x, np_gradient, label=f'dx = {dx} numpy')
            # ax.plot(x, fft_gradient, label=f'dx = {dx} fft')
            # ax2.plot(x, f_z, label=f'z {z} w {w}')
            ax.plot(x, error, label=f'z = {z} mm; w = {w} px; {np.max(error)}')  # x[:width//2], error[:width//2]
            # ax.plot(x, error_real, '--*', label=f'z = {z} mm; w = {w} px; {np.max(error_real)}')  # x[:width//2], error[:width//2]
    # ax.set_yscale('log')
    ax.set_yscale('symlog')

    ax.grid(1)
    ax.legend(prop={'size': 12})
    # ax2.legend(prop={'size': 12})
    ax.set_title('FFT error')
    plt.show()
