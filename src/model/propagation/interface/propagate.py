import numpy as np

from src.model.waves.spherical_wave import SphericalWave


class Propagable:
    def propagate_on_distance(self, z: float, wave: SphericalWave) -> np.ndarray:
        pass

    def propagate_from_to(self, start: float, stop: float, step: float, wave: SphericalWave):
        pass
