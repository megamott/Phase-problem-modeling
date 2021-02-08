import numpy as np
from icecream import ic

from src.model.waves.spherical_wave import SphericalWave
from src.model.areas.square_area import SquareArea
from src.model.areas.radial_area import RadialArea
from src.model.areas.radial_aperture import RadialAperture
from src.model.propagation.angular_spectrum import AngularSpectrum


# todo поменять все informal interface на formal interface
# todo добавить у всех функций возвращаемые метдоы

wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 50e-3
gaussian_width_param = 50

square_area_1 = SquareArea(128, 128, pixel_size=px_size)
radial_area_1 = RadialArea(square_area_1)
aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)
ic(aperture.aperture)

field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength)
field.field *= aperture.aperture

ic(field.phase)

propagation_method = AngularSpectrum()
field_z = propagation_method.propagate_on_distance(100e-3, field)

field_z_array = propagation_method.propagate_from_to(0e-3, 100e-3, 5e-3, field)

print(field_z_array)

