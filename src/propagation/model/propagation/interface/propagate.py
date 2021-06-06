from abc import ABC, abstractmethod


class Propagable(ABC):
    """ Интерфейс объекта, способного распространяться в пространстве """

    @abstractmethod
    def propagate_on_distance(self, z: float, method, **kwargs):
        """
        Возвращает распространившуюся в пространстве на дистанцию z (преобразованную) волну
        :param method: конкретный метод распространения волны
        :param z: дистанция распространения волны в пространстве [м]
        :return:
        """
        pass
