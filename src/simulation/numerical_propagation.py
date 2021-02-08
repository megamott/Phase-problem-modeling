import numpy as np

from src.model.waves import spherical_wave
from src.model.areas import square_area


# todo поменять все informal interfaces на formal interfaces

area = square_area.SquareArea(128, 128)

print(area)
print(area.width)
print(area.height)
print(area.get_coordinate_grid())
y, x = area.get_coordinate_grid()

print(y)
print(x)

arr = np.arange(0, 100, 1)

wave = spherical_wave.SphericalWave(arr)

