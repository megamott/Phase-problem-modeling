import numpy as np
from icecream import ic

from src.model.areas.radial_aperture import RadialAperture
from src.model.areas.radial_area import RadialArea
from src.model.areas.square_area import SquareArea
from src.model.propagation.angular_spectrum import AngularSpectrum
from src.model.waves.spherical_wave import SphericalWave
from src.utils.math import units
from src.utils.math.general import *

# todo поменять все informal interface на formal interface
# todo добавить у всех функций возвращаемые метдоы

wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 100e-3
gaussian_width_param = 100

# Вариации порога
thresholds = [np.exp(-2), units.percent2decimal(1), units.percent2decimal(0.5)]
t_num = 0

square_area_1 = SquareArea(1024, 1024, pixel_size=px_size)


for z in np.arange(0e-3, 300e-3 + 5e-3, 5e-3):
    # синтез апертуры
    radial_area_1 = RadialArea(square_area_1)
    aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)
    propagation_method = AngularSpectrum()
    field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength)
    field.field *= aperture.aperture

    field_z = propagation_method.propagate_on_distance(z, field)

    # преобразование апертуры
    aperture = RadialAperture(radial_area_1, widest_diameter(field_z.intensity, thresholds[t_num]))

    up = field_z.get_unwrapped_phase_with_aperture(aperture)
    r = field_z.get_wavefront_radius(aperture)

    ic(r)
