def figure_configurator(func):
    def wrapper(**kwargs):
        figsize = kwargs.get('figsize', [16, 9])
        dpi = kwargs.get('dpi', 100)
        facecolor = kwargs.get('facecolor', 'w')  # цвет фона
        edgecolor = kwargs.get('edgecolor', 'k')  # цвет линий

        fig = func(**kwargs)

        fig.set_size_inches(figsize)
        fig.set_dpi(dpi)
        fig.set_facecolor(facecolor)
        fig.set_edgecolor(edgecolor)

        return fig

    return wrapper


def axes_configurator(func):
    def wrapper(ax, **kwargs):
        linewidth = kwargs.get('linewidth', 1.5)
        kwargs['linewidth'] = linewidth

        y_scale = kwargs.get('yscale', 'linear')
        x_scale = kwargs.get('xscale', 'linear')

        ax.set_xscale(x_scale)
        ax.set_xscale(y_scale)
        ax.grid(True)

        return func(ax, **kwargs)

    return wrapper
