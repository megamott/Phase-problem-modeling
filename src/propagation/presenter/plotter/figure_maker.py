import matplotlib.pyplot as plt

from src.propagation.presenter.configuration.configurator import figure_configurator
from src.propagation.presenter.plotter.ax_maker import make_intensity_x_slice_ax, make_intensity_y_slice_ax, \
    make_intensity_color_ax, make_wrp_phase_x_slice_ax, make_wrp_phase_y_slice_ax, make_unwrp_phase_x_slice_ax, \
    make_unwrp_phase_y_slice_ax, make_wrp_phase_color_ax, make_unwrp_phase_color_ax, make_r_z_ax


@figure_configurator
def make_intensity_plot(**kwargs):
    fig = plt.figure()
    ax1, ax2, ax3 = fig.add_subplot(1, 3, 1), fig.add_subplot(1, 3, 2), fig.add_subplot(1, 3, 3)

    make_intensity_x_slice_ax(ax1, **kwargs)
    make_intensity_y_slice_ax(ax2, **kwargs)
    make_intensity_color_ax(ax3, **kwargs)

    return fig


@figure_configurator
def make_phase_plot(**kwargs):
    fig = plt.figure(figsize=(16, 9))
    ax1, ax2, ax3 = fig.add_subplot(2, 3, 1), fig.add_subplot(2, 3, 2), fig.add_subplot(2, 3, 3)
    ax4, ax5, ax6 = fig.add_subplot(2, 3, 4), fig.add_subplot(2, 3, 5), fig.add_subplot(2, 3, 6)

    make_wrp_phase_x_slice_ax(ax1, **kwargs)
    make_wrp_phase_y_slice_ax(ax2, **kwargs)
    make_unwrp_phase_x_slice_ax(ax4, **kwargs)
    make_unwrp_phase_y_slice_ax(ax5, **kwargs)
    make_wrp_phase_color_ax(ax3, **kwargs)
    make_unwrp_phase_color_ax(ax6, **kwargs)

    return fig


@figure_configurator
def make_r_z_plot(**kwargs):
    fig, ax = plt.subplots()

    make_r_z_ax(ax, **kwargs)

    return fig
