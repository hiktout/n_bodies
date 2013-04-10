import numpy
import OpenGL.GL as gl
from glumpy import figure,Trackball

from n_bodies import N_bodies
from read_file import read_file

if __name__ == '__main__':
	fig = figure(size=(400,400))
	trackball = Trackball(65, 135, 1., 2.0)

	@fig.event
	def on_mouse_drag(x, y, dx, dy, button):
		trackball.drag_to(x,y,dx,dy)
		fig.redraw()

	@fig.event
	def on_mouse_scroll(dx,dy):
		print 'yay'
		trackball.zoom_to(0,0,dx,dy)
		fig.redraw()

	@fig.event
	def on_draw():
		fig.clear()
		trackball.push()
		gl.glEnable(gl.GL_POINT_SMOOTH)
		gl.glColor(0,0,0,0.5)
		gl.glPointSize(6.0)
		gl.glBegin(gl.GL_POINTS)
		P = x/(10*149.6e9)
		for p in P:
			gl.glVertex(p[0],p[1],p[2])
		gl.glEnd()
		trackball.pop()

	@fig.event
	def on_idle(dt):
		global x
		x,_ = solar_system.leapfrog()
		fig.redraw()

	import argparse
	parser = argparse.ArgumentParser(description="Run an N body simulation")
	parser.add_argument("-t","--dt",type=int,default=86400,
						help="interval between calculations in seconds")
	parser.add_argument("file",nargs="+",
						help="files containing the mass,"
						" initial position and velocity of the bodies")
	args = parser.parse_args()

	numpy.seterr(all='ignore')

	m,x,v,names,styles = read_file(args.file)
	# change the position and velocity of the Sun so that
	# the centre of mass is stationary and at the origin
	x[0] = -numpy.sum(x[1:]*m[1:,numpy.newaxis],axis=0)/m[0]
	v[0] = -numpy.sum(v[1:]*m[1:,numpy.newaxis],axis=0)/m[0]
	solar_system = N_bodies(m,x,v,args.dt,0)
	v = solar_system.v_correction()

	fig.show()