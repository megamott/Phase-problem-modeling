import numpy as np
from icecream import ic

from src.model.waves.spherical_wave import SphericalWave
from src.model.areas.square_area import SquareArea
from src.model.areas.radial_area import RadialArea


# todo поменять все informal interface на formal interface

wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 50e-3
gaussian_width_param = 250

square_area_1 = SquareArea(128, 128, pixel_size=px_size)
radial_area_1 = RadialArea(square_area_1)
ic(radial_area_1.get_coordinate_grid())

radial_area_1.__setattr__('pixel_size', 1.04e-6)

ic(radial_area_1.get_coordinate_grid())

field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength)



