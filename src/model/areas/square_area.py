import numpy as np

from src.model.areas.interfaces import area
from src.utils.math import units


class SquareArea(area.Area):

    def __init__(self, height, width, pixel_size=5.04e-6):
        self.__height = height
        self.__width = width
        self.__pixel_size = pixel_size

    def get_coordinate_grid(self):
        y_grid_array, x_grid_array = np.mgrid[-self.__height / 2:self.__height / 2, -self.__width / 2:self.__width / 2]
        y_grid_array, x_grid_array = (units.px2m(y_grid_array, px_size_m=self.__pixel_size),
                                      units.px2m(x_grid_array, px_size_m=self.__pixel_size))
        return y_grid_array, x_grid_array

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def pixel_size(self):
        return self.__pixel_size

    @pixel_size.setter
    def pixel_size(self, pixel_size):
        self.__pixel_size = pixel_size
