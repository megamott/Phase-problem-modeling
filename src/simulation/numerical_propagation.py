from icecream import ic

from src.model.areas.radial_aperture import RadialAperture
from src.model.areas.radial_area import RadialArea
from src.model.areas.square_area import SquareArea
from src.model.configuration.mac_saver import MacSaver
from src.model.propagation.angular_spectrum import AngularSpectrum
from src.model.waves.spherical_wave import SphericalWave
from src.utils.files_routine import *
from src.utils.math.general import *

# todo интерфейс Saver переписать так, чтобы было удобно пользоваться
# todo создать класс Plotter
# todo добавть в Wave Propagable

# конфигурация
saver = MacSaver()

# основные параметры для синтеза волны
wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 100e-3
gaussian_width_param = 250

# вариации порога определения апертуры
thresholds = [np.exp(-2), units.percent2decimal(1), units.percent2decimal(0.5)]
t_num = 0

# параметры для итерации при рапространении волны
start = units.mm2m(0)
stop = units.mm2m(200)
step = units.mm2m(5)

# изменяющийся параметр для выборок
matrixes = np.array([1024])

# массивы для записи значений циклов
array_of_wavefront_radius_arrays = []
array_of_z_distances = []

# создание волны
square_area_1 = SquareArea(matrixes[0], matrixes[0], pixel_size=px_size)
radial_area_1 = RadialArea(square_area_1)
aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)
field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength)
field.field *= aperture.aperture

for matrix in matrixes:
    ic(matrix)
    matrix_size = matrix
    square_area_1 = SquareArea(matrix_size, matrix_size, pixel_size=px_size)

    # массивы для записи значений одного цикла
    wavefront_radius_array = []
    z_distances_array = []

    for z in np.arange(start, stop + step, step):
        # синтез апертуры
        radial_area_1 = RadialArea(square_area_1)
        aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)

        # выбор метода распространения волны
        propagation_method = AngularSpectrum()

        # создание волны
        field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength)
        field.field *= aperture.aperture

        # распространение волны на дистанцию z
        field_z = propagation_method.propagate_on_distance(z, field)

        # преобразование апертуры
        aperture = RadialAperture(radial_area_1, widest_diameter(field_z.intensity + 0.0005, thresholds[t_num]))
        ic(widest_diameter(field_z.intensity, thresholds[t_num]))

        # развернутая апертура
        up = field_z.get_unwrapped_phase(aperture=aperture)
        # неразвернутая апертура
        wp = field_z.get_wrapped_phase(aperture=aperture)
        # радиус волнового фронта
        r = field_z.get_wavefront_radius(aperture)

        wavefront_radius_array.append(r)
        z_distances_array.append(units.m2mm(z))

        save_phase(z, field_z, up, wp, r, saver)
        save_intensity(z, field_z, saver)

        ic(r)

    ic()
    array_of_wavefront_radius_arrays.append(wavefront_radius_array)
    array_of_z_distances.append(z_distances_array)


save_r_z(array_of_z_distances, array_of_wavefront_radius_arrays, matrixes, field, saver, step=step)
