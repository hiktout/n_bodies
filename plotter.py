import numpy

import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

from coroutines import coroutine,data_buffer,dedup

class Plotter(animation.TimedAnimation):
	"""
	A coroutine like layer above pyplot.
	Draws a graph as and when data arrives,
	so it will be animated
	"""
	def __init__(self,plots=None,axis=None,**pipeargs):
		"""
		Create the main plot. Each line required
		must be declared upfront here, in the form
		of a dictionary, plots. plots.keys() are the
		labels for each line, and plots.values() are
		the style of the line, in the matplot
		abbreviated form. The range of data values
		must also be declared in a tuple axis, where
		axis = [xmin,xmax,ymin,ymax], as in pyplot.

		There are also various options
		controlling how the data is handled.
		"""

		# pyplot.ion() # enable animations

		self.fig = pyplot.figure()

		self.ax = self.fig.add_subplot(1,1,1) # fill figure

		self.l = self.ax.plot(*self.read_args(plots),markevery=(-1,1))
		self.lines = self.add_pipeline(self.l,**pipeargs)
		self.lines = dict(zip(plots.keys(),self.lines))

		self.ax.axis(axis)
		self.ax.set_aspect('equal') # ensure circles appear circular

		# pyplot.draw()

		# needed for later
		# self.count = 0
		# self.bufsize = pipeargs['bufsize']

	def start_anim(self):
		animation.TimedAnimation.__init__(self,self.fig,interval=50,blit=True)
		pyplot.show()

	def _draw_frame(self,ignore):
		self.flush()
		self._drawn_artists = self.l
		print 'drawn'

	def new_frame_seq(self):
		from itertools import count
		return count()

	def add_subplot(self,subplots,axis,position,**pipeargs):
		"""
		Add a floating subplot to the pyplot figure.
		The function call form is similar to that of
		the Plotter constructor, with the addition of
		the list position, which defines the position
		and size of the subplot, in units from 0 to 1,
		such that position = [bottom,left,width,height]
		"""
		subax = self.fig.add_axes(position)

		sublines = subax.plot(*self.read_args(subplots))
		
		sublines = self.add_pipeline(sublines,**pipeargs)
		sublines = zip(subplots.keys(),sublines)
		self.lines.update(sublines)

		subax.axis(axis)

		return subax

	def send(self,d):
		"""
		This adds data to the lines in the plot.
		Data should be passed in the form of a
		dictionary, with values having keys
		corresponding to the keys defined at
		instantiation. The name of this method
		is send, to allow it to be used as a
		consumer in a coroutine pipeline
		"""
		for key,value in d.iteritems():
			self.lines[key].send(value)

		# # redraw after bufsize calls
		# self.count += 1
		# if self.count == 100:
		# 	self.flush()
		# 	self.count = 0
		# 	pyplot.draw()


	def flush(self):
		"""
		Add any data currently residing
		in pipelines to plot lines by
		flushing buffers
		"""
		for line in self.lines.values():
				line.send(None)

	@staticmethod
	def add_pipeline(lines,maxpoints=None,bufsize=100,**tol):
		"""
		Helper method to add a reciever and a pipeline
		for each plot line. The pipeline created depends
		on the options given
		"""
		# this actually adds the data to a line
		lines = [Plotter.line_consumer(l,maxpoints) for l in lines]
		if bufsize: # if we want buffered data
			lines = [data_buffer(l,bufsize) for l in lines]
		if tol: # if we want to discard similar values
			lines = [dedup(l,**tol) for l in lines]

		return lines

	@staticmethod
	@coroutine
	def line_consumer(line,maxpoints=None):
		"""
		This helper coroutine does the actual
		work of adding data to the pyplot
		Line2D object for each line; one per
		line is created in __init__ and
		associated with the line labels
		"""
		while 1:
			data = line.get_xydata()
			new = (yield)
			if len(new) == 0: continue
			if maxpoints:
				lim = maxpoints - len(new)
				data = data[-lim:]
			new = numpy.append(data,new,0)
			line.set_data(new[:,0],new[:,1])

	@staticmethod
	def read_args(args):
		"""
		Helper function to read the line specification
		dictionary into a form useable by pyplot.plot()
		"""
		args = [(None,None,style) for (name,style) in args.iteritems()]
		args = [item for tup in args for item in tup] # flatten
		return args

	# def __del__(self):
	# 	"""
	# 	Define a destructor that will
	# 	leave the plot showing
	# 	at the end of the program
	# 	"""
	# 	self.flush()

	# 	pyplot.ioff()
	# 	pyplot.show()