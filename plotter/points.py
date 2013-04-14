from numpy import array

from glumpy import figure,Trackball
import OpenGL.GL as gl

from coroutines import coroutine
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

def plotter3D(data_q,plots,scale):
	fig = figure(size=(400,400))
	trackball = Trackball(65,135,1.,2.)

	tri_c = [(1,0,0,1),(0,1,0,1),(0,0,1,1)]
	tri_o = array([0,0,0])
	tri = 0.1*array([[1,0,0],[0,1,0],[0,0,1]])

	@fig.event
	def on_mouse_drag(x,y,dx,dy,button):
		trackball.drag_to(x,y,dx,dy)
		fig.redraw()

	@fig.event
	def on_scroll(x,y,dx,dy):
		trackball.scroll_to(x,y,dx,dy)
		fig.redraw()

	@fig.timer(10.0)
	def timer(dt):
		fig.redraw()

	@fig.event
	def on_draw():
		d = data_q.get()

		fig.clear(0,0,0,1)
		trackball.push()

		gl.glBegin(gl.GL_LINES)
		for i in range(3):
			gl.glColor(*tri_c[i])
			gl.glVertex(*tri_o)
			gl.glVertex(*(tri[i]+tri_o))
		gl.glEnd()

		gl.glEnable(gl.GL_POINT_SMOOTH)

		for name,x in d.iteritems():
			style = plots[name]

			gl.glColor(*style['color'])
			if 'size' in style:
				gl.glPointSize(style['size'])
			if 'line' in style:
				gl.glBegin(gl.GL_LINES)
			else:
				gl.glBegin(gl.GL_POINTS)

			for i in xrange(len(x)):
				gl.glVertex(*(x[i]/scale))
			gl.glEnd()

		trackball.pop()

	fig.show()

@coroutine
def Plotter3D(plots,scale):
	data_q = SimpleQueue()

	plot = Process(target=plotter3D,args=(data_q,plots,scale))
	plot.start()

	data = {}
	try:
		while True:
			data.update((yield))
			if data_q.empty() == False:
				continue
			data_q.put(data)
	except GeneratorExit:
		pass