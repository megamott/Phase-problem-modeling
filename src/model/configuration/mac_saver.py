from matplotlib.figure import Figure

from src.model.configuration.interface.saver import Saver


class MacSaver(Saver):

    def save_image(self, fig: Figure, package_name: str, filename: str):
        filepath = f"/Users/megamot/Programming/Python/TIE_objects/data/images/{package_name}/{filename}"
        fig.savefig(filepath)
