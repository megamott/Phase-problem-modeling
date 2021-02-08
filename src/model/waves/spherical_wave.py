import numpy as np

from src.model.waves.interface import wave


class SphericalWave(wave.Wave):

    def __init__(self, field: np.ndarray):
        self.field = field

    @property
    def field(self):
        return self.__field

    @property
    def phase(self):
        return self.__field ** 2

    @field.setter
    def field(self, field):
        self.__field = field

    def get_wrapped_phase(self):
        pass

    def get_unwrapped_phase(self):
        pass

    def get_intensity(self):
        pass

    def get_wavelength(self):
        pass
