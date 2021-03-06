from abc import ABC, abstractmethod


# интерфейс объекта, способного распространяться в пространстве
class Propagable(ABC):

    @abstractmethod
    def propagate_on_distance(self, z: float, method):
        """
        Возвращает распространившуюся в пространстве на дистанцию z (преобразованную) волну
        :param method: конкретный метод распространения волны
        :param z: дистанция распространения волны в пространстве [м]
        :return:
        """
        pass
