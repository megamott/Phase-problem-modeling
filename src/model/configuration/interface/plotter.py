from abc import ABC, abstractmethod


# интерфейс строителя графиков
class Plotter(ABC):

    def make_plots(self):
        """
        Строит несколько зависимостей на одном графике
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
