from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import io


class Plotter:

    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.fig.autofmt_xdate()

    def get_plot(self, x, y):
        output = io.BytesIO()
        self.axes.bar(x, y)
        FigureCanvas(self.fig).print_png(output)
        return output


