import math
import cmath
import random
import os
import tempfile
os.environ['MPLCONfigureDIR'] = tempfile.mkdtemp()

from cStringIO import StringIO
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.patches import Ellipse
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False

class Canvas(object):

    def __init__(self, title='', xlab='x', ylab='y', xrange=None, yrange=None):
        self.fig = Figure()
        self.fig.set_facecolor('white')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlab)
        self.ax.set_ylabel(ylab)
        if xrange:
            self.ax.set_xlim(xrange)
        if yrange:
            self.ax.set_ylim(yrange)
        self.legend = []

    def save(self, filename='plot.png'):
        if self.legend:
            legend = self.ax.legend([e[0] for e in self.legend],
                                    [e[1] for e in self.legend])
            legend.get_frame().set_alpha(0.7)
        if filename:
            FigureCanvasAgg(self.fig).print_png(open(filename, 'wb'))
        else:
            s = StringIO()
            FigureCanvasAgg(self.fig).print_png(s)
            return s.getvalue()

    def binary(self):
        return self.save(None)

    def hist(self, data, bins=20, color='blue', legend=None):
        q = self.ax.hist(data, bins)
        #if legend:
        #    self.legend.append((q[0], legend))
        return self

    def plot(self, data, color='blue', style='-', width=2,
             legend=None, xrange=None):
        if callable(data) and xrange:
            x = [xrange[0]+0.01*i*(xrange[1]-xrange[0]) for i in xrange(0,101)]
            y = [data(p) for p in x]
        elif data and isinstance(data[0],(int,float)):
            x, y = xrange(len(data)), data
        else:
            x, y = [p[0] for p in data], [p[1] for p in data]
        q = self.ax.plot(x, y, linestyle=style, linewidth=width, color=color)
        if legend:
            self.legend.append((q[0],legend))
        return self

    def errorbar(self, data, color='black', marker='o', width=2, legend=None):
        x,y,dy = [p[0] for p in data], [p[1] for p in data], [p[2] for p in data]
        q = self.ax.errorbar(x, y, yerr=dy, fmt=marker, linewidth=width, color=color)
        if legend:
            self.legend.append((q[0],legend))
        return self

    def ellipses(self, data, color='blue', width=0.01, height=0.01, legend=None):
        for point in data:
            x, y = point[:2]
            dx = point[2] if len(point)>2 else width
            dy = point[3] if len(point)>3 else height
            ellipse = Ellipse(xy=(x, y), width=dx, height=dy)
            self.ax.add_artist(ellipse)
            ellipse.set_clip_box(self.ax.bbox)
            ellipse.set_alpha(0.5)
            ellipse.set_facecolor(color)
        if legend:
            self.legend.append((q[0],legend))
        return self

    def imshow(self, data, interpolation='bilinear'):
        self.ax.imshow(data).set_interpolation(interpolation)
        return self
