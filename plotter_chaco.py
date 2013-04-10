import numpy as np

from coroutines import coroutine
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

def quiverPlotter(data_q,num):
	from enable.component_editor import ComponentEditor

	from traits.api import HasTraits,Instance
	from traitsui.api import View, Item

	from pyface.timer.api import Timer

	from chaco.api import ArrayDataSource, MultiArrayDataSource, \
		DataRange1D, LinearMapper, QuiverPlot, OverlayPlotContainer, \
		add_default_axes, add_default_grids

	from chaco.tools.api import PanTool, ZoomTool

	class PlotterWindow(HasTraits):
		plot = Instance(OverlayPlotContainer)
		timer = Instance(Timer)

		traits_view = View(
			Item('plot',editor=ComponentEditor(),show_label=False),
			width=500,height=500,resizable=True,title="Plotter")

		def __init__(self,data_q,num):
			super(PlotterWindow,self).__init__()

			self.data_q = data_q

			self.x = ArrayDataSource(np.zeros(num))
			self.y = ArrayDataSource(np.zeros(num))
			self.v = MultiArrayDataSource(np.zeros((num,2)))

			xrange = DataRange1D()
			xrange.add(self.x)
			yrange = DataRange1D()
			yrange.add(self.y)

			quiverplot = QuiverPlot(index=self.x,value=self.y,vectors=self.v,
				index_mapper=LinearMapper(range=xrange),
				value_mapper=LinearMapper(range=yrange),
				bgcolor='white')
			add_default_axes(quiverplot)
			add_default_grids(quiverplot)

			quiverplot.tools.append(PanTool(quiverplot,constrain_key='shift'))
			quiverplot.overlays.append(ZoomTool(quiverplot))

			self.plot = OverlayPlotContainer(quiverplot, padding=50)
			self.timer = Timer(50.0, self.onTimer)

			self.configure_traits()

		def onTimer(self,*args):
			d = self.data_q.get()

			self.x.set_data(d[0])
			self.y.set_data(d[1])
			self.v.set_data(d[2])

	PlotterWindow(data_q,num)

@coroutine
def QuiverPlotter(num):
	data_q = SimpleQueue()

	plot = Process(target=quiverPlotter,args=(data_q,num))
	plot.start()

	try:
		while True:
			data = (yield)
			if data_q.empty() == False:
				continue
			data_q.put(data)
	except GeneratorExit:
		plot.join()

def histPlotter(data_q,plots):
	from traits.api import HasTraits,Instance
	from traitsui.api import View, Item
	from chaco.api import Plot, ArrayPlotData
	from enable.component_editor import ComponentEditor
	from pyface.timer.api import Timer

	class PlotterWindow(HasTraits):
		plot = Instance(Plot)
		timer = Instance(Timer)

		traits_view = View(
			Item('plot',editor=ComponentEditor(),show_label=False),
			width=500,height=500,resizable=True,title="Plotter")

		def __init__(self,data_q,plots):
			super(PlotterWindow,self).__init__()

			self.data_q = data_q

			self.plotdata = ArrayPlotData(**self.read_args(plots))

			plot = Plot(self.plotdata)

			for name,style in plots.iteritems():
				plot.plot((name+'_x',name), type='line', color=style, render_style='connectedhold')

			self.plot = plot

			self.timer = Timer(50.0, self.onTimer)

			self.configure_traits()

		def onTimer(self, *args):
			d = self.data_q.get()

			for name,data in d.iteritems():
				# x = self.plotdata.get_data(name+'_x')
				# y = self.plotdata.get_data(name)
				# x = np.append(x,data[0])
				# y = np.append(y,data[1])
				# self.plotdata.set_data(name+'_x',x)
				# self.plotdata.set_data(name,y)
				self.plotdata.set_data(name+'_x',data[1])
				self.plotdata.set_data(name,data[0])

		@staticmethod
		def read_args(plots):
			data_dict = {k: np.array([]) for k in plots}
			data_dict.update({k+'_x': np.array([]) for k in plots})

			return data_dict

	PlotterWindow(data_q,plots)

@coroutine
def HistPlotter(plots):
	data_q = SimpleQueue()

	plot = Process(target=histPlotter,args=(data_q,plots))
	plot.start()

	data = {}
	try:
		while True:
			data.update((yield))
			if data_q.empty() == False:
				continue
			data_q.put(data)
	except GeneratorExit:
		plot.join()