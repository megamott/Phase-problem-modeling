import numpy as np
import matplotlib.ticker as ticker
from icecream import ic

from src.model.areas.radial_aperture import RadialAperture
from src.model.areas.radial_area import RadialArea
from src.model.areas.square_area import SquareArea
from src.model.propagation.angular_spectrum import AngularSpectrum
from src.model.waves.spherical_wave import SphericalWave
from src.utils.math import units
from src.utils.files_routine import *
from src.utils.math.general import *

# todo поменять все informal interface на formal interface
# todo добавить у всех функций возвращаемые метдоы

wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 200e-3
gaussian_width_param = 250

# Вариации порога
thresholds = [np.exp(-2), units.percent2decimal(1), units.percent2decimal(0.5)]
t_num = 0

# параметры цикла
start = units.mm2m(0)
stop = units.mm2m(500)
step = units.mm2m(5)

array_of_wavefront_radius_arrays = []
matrix = np.array([256, 512, 1024])
array_of_z_distances = []

for i in np.arange(0, 3, 1):
    matrix_size = matrix[i]
    square_area_1 = SquareArea(matrix_size, matrix_size, pixel_size=px_size)

    wavefront_radius_array = []
    z_distances_array = []

    for z in np.arange(start, stop + step, step):
        # z = 0e-3
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
        wp = field_z.get_wrapped_phase_with_aperture(aperture)
        r = field_z.get_wavefront_radius(aperture)

        wavefront_radius_array.append(r)
        z_distances_array.append(units.m2mm(z))

        # save_phase(z, field_z, up, wp, r)
        # save_intensity_slices(field_z.intensity, filename=f'intensity_z_{int(units.m2mm(z))}mm',
        #                       package_name=f'intensity_f{int(units.m2mm(np.around(field_z.focal_len, decimals=3)))}_g{gaussian_width_param}_s{field_z.area.get_coordinate_grid()[0].shape[0]}',)

        ic(r)
    array_of_wavefront_radius_arrays.append(wavefront_radius_array)
    array_of_z_distances.append(z_distances_array)

fig, ax = plt.subplots(figsize=[8.0, 6.0], dpi=300, facecolor='w', edgecolor='k')

# matrix = np.array([0, 1, 2, 3])
# m = [np.around(np.exp(-2), decimals=4), np.around(units.percent2decimal(1), decimals=4),
#      np.around(units.percent2decimal(0.5), decimals=4), np.around(units.percent2decimal(50), decimals=4)]

for z in np.arange(0, np.shape(matrix)[0], 1):
    radius_y = array_of_wavefront_radius_arrays[z]
    z_propagation_distance = array_of_z_distances[z]
    theory_r_z = np.abs(np.array(z_propagation_distance) - units.m2mm(focal_len))

    if z == 0:
        ax.plot(z_propagation_distance, theory_r_z, label='Theoretical', color='k', markersize=3.)
    ax.plot(z_propagation_distance, radius_y, '-o', label=f'size: {matrix[z]}', linewidth=1., markersize=3.)

# save_r_z(z_propagation_distance, radius_y, focus, e_width_param, thresholds[t_num], step)

# ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(20))
#
# ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(20))

theory_r_z = np.abs(np.array(array_of_z_distances[0]) - units.m2mm(focal_len))
ax.set_xlim(0, 500)
ax.set_ylim(0, theory_r_z[-1])

plt.xlabel('Propagation distance, mm')
plt.ylabel('R(z), mm', )
plt.legend()
plt.title(f'f\' = {units.m2mm(np.around(focal_len, decimals=3))} mm; g = {gaussian_width_param}; step = {step} mm', fontsize=14)
# plt.show()

ax.grid(True)

filepath = f"/Users/megamot/Programming/Python/TIE_objects/data/images/r(z)/trz_f_{int(units.m2mm(np.around(focal_len, decimals=3)))}_g{gaussian_width_param}_matrix"
fig.savefig(filepath)
