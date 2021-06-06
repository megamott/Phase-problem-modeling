from .grid import PolarGrid
from ...utils.optic.field import circ
from ...utils.math.general import get_slice
from ...utils.math.units import px2m


class Aperture:
    """ Апертура, circ """

    def __init__(self, polar_grid: PolarGrid, aperture_diameter: float):
        """
        Создаёт апертуру (circ) на основе сетки в полярных координатах
        :param polar_grid: сетка в полярных координатах
        :param aperture_diameter: диаметр апертуры [px]
        """
        aperture_diameter = px2m(aperture_diameter, px_size_m=polar_grid.pixel_size)  # [м]
        self._aperture_diameter = aperture_diameter
        self._polar_grid = polar_grid
        self._aperture_view = circ(polar_grid.grid, w=aperture_diameter)

    def modify(self, wave, z: float):
        """
        Метод модификации апертуры для правильного разворачивания фазы из-за рпспространения волны в пространстве
        :param wave: волна для корректировки диаметра апертуры
        :param z: дистанция, на которую распространилась волна из начала координат
        :return: модифицированная апертура
        """
        from ..waves.interface.wave import Wave  # чтобы избежать круговой импорт

        if not isinstance(wave, Wave):
            raise TypeError('Переданный параметр "wave" не является Wave')

        wrp_phase_values = get_slice(
            wave.phase,
            wave.phase.shape[0] // 2,
        )[1]

        ap_values = get_slice(
            self.aperture_view,
            self.aperture_view.shape[0] // 2,
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
        rwrp = next((i for i in range(jump, wave.grid.grid[0].shape[0], 1) if
                     (wrp_phase_values[i] > 0) and (wrp_phase_values[i - 1] < 0)),
                    1)

        # определение, какая из нулевых координат неразвернутой фазы ближе к скачку
        jump = rwrp if lwrp - jump > rwrp - jump else lwrp

        # генерация новой апертуры с скорректированным диаметром
        # в случае, если волна сходящаяся, вводится дополнительная корректировка
        new_aperture_diameter = (wave.grid.grid[0].shape[0] // 2 - jump) * 2
        new_aperture_diameter += 2 if z < wave.focal_len else 0

        self.aperture_diameter = new_aperture_diameter

    @property
    def aperture_diameter(self):
        return self._aperture_diameter

    @aperture_diameter.setter
    def aperture_diameter(self, aperture_diameter):
        self._aperture_diameter = px2m(aperture_diameter, px_size_m=self._polar_grid.pixel_size)  # [м]
        self._aperture_view = circ(self.polar_grid.grid, w=self._aperture_diameter)

    @property
    def polar_grid(self):
        return self._polar_grid

    @property
    def aperture_view(self):
        return self._aperture_view
