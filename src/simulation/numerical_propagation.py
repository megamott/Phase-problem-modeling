import numpy as np
from icecream import ic

from src.model.waves.spherical_wave import SphericalWave
from src.model.areas import square_area
from src.model.areas.interface import area


# todo поменять все informal interface на formal interface

wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 50e-3
gaussian_width_param = 250

area_1 = square_area.SquareArea(128, 128, pixel_size=px_size)

field = SphericalWave(area_1, focal_len, gaussian_width_param, wavelength)

ic(field.focal_len)
ic(field.wavelength)
ic(field.gaussian_width_param)
ic(field.intensity)
ic(field.field)
ic(field.phase)

