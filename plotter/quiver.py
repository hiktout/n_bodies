from numpy import zeros

from util import coroutine
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

			self.x = ArrayDataSource(zeros(num))
			self.y = ArrayDataSource(zeros(num))
			self.v = MultiArrayDataSource(zeros((num,2)))

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
