from abc import ABC, abstractmethod
import numpy as np

from src.model.waves.interface.wave import Wave


# интерфейс метода распространения волны в пространстве
class Propagable(ABC):

    @abstractmethod
    def propagate_on_distance(self, z: float, wave: Wave) -> np.ndarray:
        """
        Возвращает матрицу распространившейся волны на дистанцию z
        :param z: дистанция распространения волны в пространстве [м]
        :param wave: волна
        :return: возвращает матрицу волны в плоскости с координатой z
        """
        pass

    # @abstractmethod
    # def propagate_from_to(self, start: float, stop: float, step: float, wave: Wave) -> np.ndarray:
    #     """
    #     Возвращает матрицы распространившихся в пространстве волн от координаты start до координату stop с шагом step
    #     :param start: координата начала распространения волны
    #     :param stop: координата конца распространения волны
    #     :param step: шаг распространения волны
    #     :param wave: волна
    #     :return: массив матриц волн
    #     """
    #     pass
