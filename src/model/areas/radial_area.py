import numpy as np

from src.model.areas.interface import area
from src.model.areas.square_area import SquareArea
from src.utils.math import units


class RadialArea(area.Area):

    def __init__(self, square_area: SquareArea):
        self.__height = square_area.height
        self.__width = square_area.width
        self.__pixel_size = square_area.pixel_size

    def get_coordinate_grid(self):
        y_grid_array, x_grid_array = np.mgrid[-self.__height / 2:self.__height / 2, -self.__width / 2:self.__width / 2]
        y_grid_array, x_grid_array = (units.px2m(y_grid_array, px_size_m=self.__pixel_size),
                                      units.px2m(x_grid_array, px_size_m=self.__pixel_size))
        radial_grid = np.sqrt(x_grid_array ** 2 + y_grid_array ** 2)
        return radial_grid

    def get_pixel_size(self):
        return self.__pixel_size

    @property
    def pixel_size(self):
        return self.__pixel_size

    @pixel_size.setter
    def pixel_size(self, pixel_size):
        self.__pixel_size = pixel_size
