from matplotlib.figure import Figure
import numpy as np

from ..configuration.interface.saver import Saver
from ..waves.interface.wave import Wave
from ...utils.math import units


class MacSaver(Saver):

    def save_image(self, fig: Figure, package_name: str, filename: str):
        filepath = f"/Users/megamot/Programming/Python/TIE_objects/data/images/{package_name}/{filename}"
        fig.savefig(filepath)

    @staticmethod
    def create_filename(wave: Wave, method: str, z=False, it=False) -> str:
        return f'{method}_' \
               f'f{int(units.m2mm(np.around(wave.focal_len, decimals=3)))}_' \
               f'g{wave.gaussian_width_param}_' \
               f's{wave.area.coordinate_grid[0].shape[0]}_' + \
               f'{str(int(units.m2mm(z))) + "_" if z else "0_"}' + \
               f'{f"{it}.png" if it else ".png"}'

    @staticmethod
    def create_package_name(method: str, wave=False) -> str:
        plot_package = {'i': 'intensity',
                        'p': 'phase',
                        'r': 'r(z)',
                        'b': 'bound'}[method]
        # package_name = f'{method if wave else method}'
        return plot_package
