import numpy as np

from src.model.waves import spherical_wave
from src.model.areas import square_area
from src.model.areas.interfaces import area


# todo поменять все informal interfaces на formal interfaces


area_1 = square_area.SquareArea(128, 128, pixel_size=5.04e-6)

print(area_1)
print(area_1.width)
print(area_1.height)
print(area_1.get_coordinate_grid())
y, x = area_1.get_coordinate_grid()

print(y)
print(x)
print(area_1.pixel_size)

arr = np.arange(0, 100, 1)

wave = spherical_wave.SphericalWave(arr)

