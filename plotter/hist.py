from numpy import array

from util import coroutine
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

def histPlotter(data_q,plots):
	from traits.api import HasTraits,Instance
	from traitsui.api import View, Item
	from chaco.api import Plot, ArrayPlotData
	from chaco.tools.api import LineInspector
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
				p, = plot.plot((name+'_x',name), type='line', color=style, render_style='connectedhold')

			# virial radius marker
			p.overlays.append(LineInspector(p,is_listener=True,color='black'))
			p.index.metadata['selections'] = 1

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
			data_dict = {k: array([]) for k in plots}
			data_dict.update({k+'_x': array([]) for k in plots})

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