from numpy import append

import matplotlib.animation as animation

from util import coroutine
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

class LinePlotterProcess(Process):
	def __init__(self,data_q):
		super(LinePlotterProcess,self).__init__()

		self.data_q = data_q

		self.lines = {}
		self.args = []

	def add_plot(self,plots,axis,position,equal=False):
		self.args.append((plots,axis,position,equal))

		# return ax

	def update(self,*args):
		d = self.data_q.get()

		for k,v in d.iteritems():
			l = self.lines[k]
			old = l.get_xydata()
			new = append(old,(v,),0)
			l.set_data(new[:,0],new[:,1])

	def run(self):
		import matplotlib.pyplot as plt

		self.fig = plt.figure()

		for (plots,axis,position,equal) in self.args:
			ax = self.fig.add_subplot(position)
			ax.axis(axis)

			# crossing time
			ax.axvline(x=0.7)
			if equal:
				ax.set_aspect('equal')

			l = ax.plot(*self.read_args(plots),markevery=(-1,1))
			l = zip(plots.keys(),l)

			self.lines.update(l)

		anim = animation.FuncAnimation(self.fig,self.update,interval=20)
		plt.show()

	@staticmethod
	def read_args(args):
		"""
		Helper function to read the line specification
		dictionary into a form useable by pyplot.plot()
		"""
		args = [(None,None,style) for (name,style) in args.iteritems()]
		args = [item for tup in args for item in tup] # flatten
		return args

class LinePlotter:
	def __init__(self,*args,**kwargs):
		self.data_q = SimpleQueue()
		self.data = {}

		self.plot = LinePlotterProcess(self.data_q)
		self.plot.add_plot(*args,**kwargs)

	def show(self):
		self.plot.start()

	def add_plot(self,*args,**kwargs):
		self.plot.add_plot(*args,**kwargs)

	def send(self,data):
		if data == GeneratorExit:
			self.plot.join()

		self.data.update(data)
		if self.data_q.empty() != False:
			self.data_q.put(data)
