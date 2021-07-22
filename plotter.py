from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


class Plotter:

    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(1, 1, 1)

    def get_plot(self, x, y):
        output = io.BytesIO()
        self.axes.bar(x, y)
        FigureCanvas(self.fig).print_png(output)
        return output


