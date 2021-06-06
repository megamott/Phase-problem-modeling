import os
import numpy as np

from os import path
from typing import Union, Dict
from matplotlib.figure import Figure

from src.propagation.utils.math import units


class Saver:
    """ Сохранение файлов """
    def __init__(self, folder_name: str):
        self.folder_name = folder_name

    def save_image(self, image: Union[Figure, np.ndarray], package_name: str, filename: str):

        # todo add path.join
        if not path.exists(f"./../../data/{self.folder_name}/{package_name}/"):
            os.makedirs(f"./../../data/{self.folder_name}/{package_name}")
        else:
            pass
            # todo логика, если директория уже существует

        filepath = os.getcwd() + f"/../../data/{self.folder_name}/{package_name}/{filename}"

        if isinstance(image, Figure):
            image.savefig(filepath)
        elif isinstance(image, np.ndarray):
            np.save(filepath, image)

    def save_text(self, text: Union[str, Dict], package_name: str, filename: str):

        if not path.exists(f"./../../data/{self.folder_name}/{package_name}/"):
            os.makedirs(f"./../../data/{self.folder_name}/{package_name}")
        else:
            pass # todo

        filepath = os.getcwd() + f"/../../data/{self.folder_name}/{package_name}/{filename}.txt"

        with open(filepath, 'a') as file:
            if isinstance(text, str):
                file.write(text + '\n')

            elif isinstance(text, Dict):
                for key, value in text.items():
                    file.write(f'{key}: {value}\n')
                file.write('\n' + '-' * 150 + '\n\n')
                file.write(
                    f'{"z": >6}'
                    f'{"R": >8}'
                    f'{"Ap": >8}'
                    f'{"Amp": >8}'
                    f'{"x0": >7}'
                    f'{"y0": >7}'
                    f'\n'
                )

    @staticmethod
    def create_filename(z: float, extension: str = 'png') -> str:
        return f'z_{units.m2mm(z):.3f}mm.{extension}'

    @staticmethod
    def create_folder_name(method: str, wave=False) -> str:
        plot_package = {'i': 'intensity',
                        'p': 'phase',
                        'r': 'r(z)',
                        'b': 'bound'}[method]
        # package_name = f'{method if wave else method}'
        return plot_package
