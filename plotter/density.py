import numpy as np
import glumpy

from util import coroutine
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

def imagedraw(data_q,num):
	fig = glumpy.figure(size=(400,400))
	data = np.zeros((num,num)).astype(np.float32)
	cmap = glumpy.colormap.Hot
	cmap.set_under(cmap.get_color(-1))
	cmap.set_over(cmap.get_color(1))

	img = glumpy.image.Image(data,
		colormap=cmap,vmin=-10,vmax=50)

	@fig.timer(10.0)
	def timer(dt):
		fig.redraw()

	@fig.event
	def on_draw():
		data[...] = data_q.get()
		img.update()

		fig.clear()
		img.draw(0,0,0,fig.width,fig.height)

	fig.show()

@coroutine
def DensityPlotter(num,size):
	# num = size/scale
	range = [[-size,size],[-size,size]]

	data_q = SimpleQueue()

	plot = Process(target=imagedraw,args=(data_q,num))
	plot.start()

	while True:
		x = (yield)

		if data_q.empty() == False:
			continue

		hist,_,_ = np.histogram2d(x[:,0],x[:,1],bins=num,range=range)
		avg = np.average(hist)
		hist = (hist - avg)/avg
		data_q.put(hist.astype(np.float32))
