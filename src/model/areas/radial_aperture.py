import numpy as np

from src.model.areas.interface.aperture import Aperture
from src.model.areas.radial_area import RadialArea
from src.utils.optic.field import circ
from src.utils.math import units


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
        self.__aperture = circ(radial_area.coordinate_grid, w=aperture_diameter)

    @property
    def aperture_diameter(self):
        return self.__aperture_diameter

    @property
    def aperture(self):
        return self.__aperture

    @aperture_diameter.setter
    def aperture_diameter(self, aperture_diameter):
        self.__aperture_diameter = aperture_diameter
