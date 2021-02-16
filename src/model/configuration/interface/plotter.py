from abc import ABC, abstractmethod


# интерфейс для построения графиков
class Plotter(ABC):

    def make_r_z_plot(self):
        """
        Строит график зависимости радиуса кривизны волнового фронта от дистанции его распространения
        :return:
        """
        pass

    def make_intensity_plot(self):
        """
        Строит график с исчерпывающей информацией об интенсивности волны
        :return:
        """
        pass

    def make_phase_plot(self):
        """
        Строит график с исчерпывающей информацией о фазе волны
        :return:
        """
        pass
