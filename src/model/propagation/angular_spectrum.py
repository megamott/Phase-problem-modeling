import numpy as np
from numpy.fft import fft2, fftshift, ifft2

from src.model.propagation.interface.propagate import Propagable
from src.model.waves.spherical_wave import SphericalWave


class AngularSpectrum(Propagable):

    @staticmethod
    def propagation(z: float, wave: SphericalWave) -> SphericalWave:
        propagated_wave = wave

        height = propagated_wave.field.shape[0]  # 1024 строк - количество строк
        width = propagated_wave.field.shape[1]  # 1024 строк - количество строк

        wave_number = 2 * np.pi / propagated_wave.wavelength

        # Сетка в частотной области
        nu_x = np.arange(-width / 2, width / 2) / (width * propagated_wave.area.get_pixel_size())
        nu_y = np.arange(-height / 2, height / 2) / (height * propagated_wave.area.get_pixel_size())
        nu_x_grid, nu_y_grid = np.meshgrid(nu_x, nu_y)

        nu_x_grid, nu_y_grid = fftshift(nu_x_grid), fftshift(nu_y_grid)

        # Фурье-образ исходного поля
        field = fft2(propagated_wave.field)

        # Передаточная функция слоя пространства
        exp_term = np.sqrt(
            1 - (propagated_wave.wavelength * nu_x_grid) ** 2 - (propagated_wave.wavelength * nu_y_grid) ** 2)
        h = np.exp(1j * wave_number * z * exp_term)

        field_after_propagation = ifft2(field * h)

        propagated_wave.field = field_after_propagation
        propagated_wave.phase = np.angle(field_after_propagation)
        propagated_wave.intensity = np.abs(field_after_propagation) ** 2

        return propagated_wave

    def propagate_on_distance(self, z: float, wave: SphericalWave) -> SphericalWave:
        return self.propagation(z, wave)

    # Будет работать, если перед каждой новой итерацией создавать новую волну и умножать её на апертуру
    # def propagate_from_to(self, start: float, stop: float, step: float, wave: SphericalWave) -> np.ndarray:
    #     wave_z_array = []
    #
    #     for z in np.arange(start, stop + step, step):
    #
    #         wave_z = self.propagation(z, wave)
    #         wave_z_array.append(wave_z)
    #
    #     return np.array(wave_z_array)
