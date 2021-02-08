import numpy as np

from src.model.areas.interfaces import area
from src.utils.math import units


class SquareArea(area.Area):

    def __init__(self, height, width):
        self.__height = height
        self.__width = width

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

    def get_coordinate_grid(self):
        y_grid_array, x_grid_array = np.mgrid[-self.__height / 2:self.__height / 2, -self.__width / 2:self.__width / 2]
        y_grid_array, x_grid_array = units.px2m(y_grid_array), units.px2m(x_grid_array)
        return y_grid_array, x_grid_array
