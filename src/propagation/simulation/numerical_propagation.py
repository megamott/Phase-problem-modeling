from icecream import ic

from src.propagation.model.areas.radial_aperture import RadialAperture
from src.propagation.model.areas.radial_area import RadialArea
from src.propagation.model.areas.square_area import SquareArea
from src.propagation.model.configuration.mac_saver import MacSaver
from src.propagation.model.configuration.multiwave_plotter import MultiWavePlotter
from src.propagation.model.configuration.onewave_plotter import OneWavePlotter
from src.propagation.model.configuration.serieswave_plotter import SeriesWavePlotter
from src.propagation.model.waves.spherical_wave import SphericalWave
from src.propagation.utils.files_routine import *
from src.propagation.utils.math.general import *

# todo интерфейс Saver переписать так, чтобы было удобно пользоваться
# todo создать класс Plotter

# конфигурация
saver = MacSaver()

# основные параметры для синтеза волны
wavelength = 659.6e-9
px_size = 5.04e-6
focal_len = 100e-3
gaussian_width_param = 247

# вариации порога определения апертуры
thresholds = [np.exp(-2), units.percent2decimal(13), units.percent2decimal(0.5), units.percent2decimal(0.8)]
t_num = 0

# параметры для итерации при рапространении волны
start = units.mm2m(0)
stop = units.mm2m(200)
step = units.mm2m(50)
z_array = np.array(np.arange(units.m2mm(start), units.m2mm(stop + step), units.m2mm(step)))

# изменяющийся параметр для выборок
matrixes = np.array([512, 1024])

# массивы для записи значений циклов
wave_array = []
aperture_array = []
array_wave_array = []
array_aperture_array = []
array_of_wavefront_radius_arrays = []
array_of_z_distances = []

# создание волны
square_area_1 = SquareArea(matrixes[0], matrixes[0], pixel_size=px_size)
radial_area_1 = RadialArea(square_area_1)
aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)
field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength, 0)
field.field *= aperture.aperture

for matrix in matrixes:
    ic(matrix)
    matrix_size = matrix
    square_area_1 = SquareArea(matrix_size, matrix_size, pixel_size=px_size)

    z_distances_array = []
    wavefront_radius_array = []

    for z in np.arange(start, stop + step, step):
        # синтез апертуры
        radial_area_1 = RadialArea(square_area_1)
        aperture = RadialAperture(radial_area_1, 2 * gaussian_width_param)

        # создание волны
        field = SphericalWave(square_area_1, focal_len, gaussian_width_param, wavelength, z)
        field.field *= aperture.aperture

        # распространение волны на дистанцию z
        field.propagate_on_distance(z)

        # преобразование апертуры
        aperture = RadialAperture(radial_area_1, widest_diameter(field.intensity, thresholds[t_num]))
        ic(widest_diameter(field.intensity, thresholds[t_num]))

        # развернутая апертура
        # up = field.get_unwrapped_phase(aperture=aperture)

        # неразвернутая апертура
        # wp = field.get_wrapped_phase(aperture=aperture)

        # радиус волнового фронта
        r = field.get_wavefront_radius(aperture)

        one_wave_plotter = OneWavePlotter(field, aperture, z, saver)
        # one_wave_plotter.save_aperture_bound(100)
        # one_wave_plotter.save_phase()
        # one_wave_plotter.save_intensity()

        ic(r)
        wave_array.append(field)
        aperture_array.append(aperture)
        # wavefront_radius_array.append(r)
        z_distances_array.append(units.m2mm(z))

    series_wave_plotter = SeriesWavePlotter(wave_array, aperture_array, z_array, step, saver)
    # series_wave_plotter.save_r_z(step)

    ic()
    array_wave_array.append(wave_array)
    array_aperture_array.append(aperture_array)
    array_of_wavefront_radius_arrays.append(wavefront_radius_array)
    array_of_z_distances.append(z_distances_array)
    wave_array = []
    aperture_array = []

multi_wave_plotter = MultiWavePlotter(array_wave_array, array_aperture_array, z_array, matrixes, step, saver)
multi_wave_plotter.save_r_z(xlabel='Propagation distance, mm', ylabel='R(z), mm')

# save_r_z(array_of_z_distances, array_of_wavefront_radius_arrays, matrixes, field, saver, step=step)
# save_plots(w_arrays + a_arrays, saver)
