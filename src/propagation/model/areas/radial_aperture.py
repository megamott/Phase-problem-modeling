import numpy as np

from ..areas.interface.aperture import Aperture
from ..areas.radial_area import RadialArea
from ..waves.interface.wave import Wave
from ...utils.math.general import get_slice
from ...utils.optic.field import circ
from ...utils.math import units


# класс апертуры, circ
class RadialAperture(Aperture):

    def __init__(self, radial_area: RadialArea, aperture_diameter: float):
        """
        Создаёт круглую апертуру на основе сетки сферических координат
        :param radial_area: сетки сферических координат
        :param aperture_diameter: диаметр апертуры [px]
        """
        aperture_diameter = units.px2m(aperture_diameter, px_size_m=radial_area.pixel_size)  # [м]
        self.__aperture_diameter = aperture_diameter
        self.__radial_area = radial_area
        self.__aperture = circ(radial_area.coordinate_grid, w=aperture_diameter)

    def modify_aperture(self, wave: Wave):
        """
        Метод модификации апертуры для правильного разворачивания фазы
        :param wave: волны
        :return: модифицированная апертура
        """
        wrp_phase_values = get_slice(
            wave.phase,
            wave.phase.shape[0] // 2,
            )[1]

        ap_values = get_slice(
            self.aperture,
            self.aperture.shape[0] // 2,
            )[1]

        # Х координата скачка апертуры с 0 на 1
        jump = next((i for i, v in enumerate(ap_values) if v == 1),
                    None)

        # ближайшая к скачку апертуры координата Х слева от скачка
        # в кторой значение неразвернутой фазы наиболее близко к нулю
        lwrp = next((i for i in range(jump, 0, -1) if (wrp_phase_values[i] > 0) and (wrp_phase_values[i - 1] < 0)),
                    1)

        # ближайшая к скачку апертуры координата Х справа от скачка
        # в кторой значение неразвернутой фазы наиболее близко к нулю
        rwrp = next((i for i in range(jump, wave.area.coordinate_grid[0].shape[0], 1) if (wrp_phase_values[i] > 0) and (wrp_phase_values[i - 1] < 0)),
                    1)

        # определение, какая из нулевых координат неразвернутой фазы ближе к скачку
        jump = rwrp if lwrp - jump > rwrp - jump else lwrp

        # генерация новой апертуры с скорректированным диаметром
        # в случае, если волна сходящаяся, вводится дополнительная корректировка
        new_aperture_diameter = (wave.area.coordinate_grid[0].shape[0] // 2 - jump) * 2
        new_aperture_diameter += 2 if wave.distance < wave.focal_len else 0

        self.aperture_diameter = new_aperture_diameter

    @property
    def aperture_diameter(self):
        return self.__aperture_diameter

    @property
    def radial_area(self):
        return self.__radial_area

    @property
    def aperture(self):
        return self.__aperture

    @aperture_diameter.setter
    def aperture_diameter(self, aperture_diameter):
        self.__aperture_diameter = units.px2m(aperture_diameter, px_size_m=self.__radial_area.pixel_size)  # [м]
        self.__aperture = circ(self.radial_area.coordinate_grid, w=self.__aperture_diameter)
