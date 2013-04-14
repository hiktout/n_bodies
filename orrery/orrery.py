#!/usr/bin/python

import numpy

from n_bodies_fast import N_bodies
from read_file import read_file
from plotter_anim import Plotter
from metrics_fast import Energy
from metrics import Angle
from coroutines import printer
from coroutines import progress_bar
from coroutines import two_lines

if __name__ == "__main__":
	import signal,sys
	def clean_exit(signal,frame):
		if not (args.progress or (pr != None)):
			print
		sys.exit(0)
	signal.signal(signal.SIGINT, clean_exit)
	import argparse

	parser = argparse.ArgumentParser(description="Run an N body simulation")

	parser.add_argument("--progress",action="store_const",const=progress_bar(),
						help="show a progress bar")
	parser.add_argument("--graph",action="store_true",
						help="plot orbits")
	# default dt is one si day
	parser.add_argument("-t","--dt",type=int,default=86400,
						help="interval between calculations in seconds")
	# default run time is one common year
	parser.add_argument("-T","--time",type=int,default=365,
						help="time to run for in units dt")
	parser.add_argument("--softening",type=int,default=0,
						help="softening constant")
	# parser.add_argument("-o","--outfile",type=argparse.FileType('w'),
						# help="save results to file, '-' is stdout")
	parser.add_argument("--energy",action="store_const",const=Energy(),
						help="calculate and plot the energy of the system")
	parser.add_argument("--period",type=int,metavar="i",nargs="?",const=1,
						help="calculate and output the orbtal period of body i")
	parser.add_argument("--maxpoints",type=int,
						help="maximum plotted line length in data points")
	parser.add_argument("file",nargs="+",
						help="files containing the mass,"
						" initial position and velocity of the bodies")
	args = parser.parse_args()

	m,x,v,names,styles = read_file(args.file)
	# change the position and velocity of the Sun so that
	# the centre of mass is stationary and at the origin
	x[0] = -numpy.sum(x[1:]*m[1:,numpy.newaxis],axis=0)/m[0]
	v[0] = -numpy.sum(v[1:]*m[1:,numpy.newaxis],axis=0)/m[0]
	solar_system = N_bodies(m,x,v,args.dt,args.softening)
	v = solar_system.v_correction()

	dt = args.dt
	t = args.time
	
	pr = None
	# pr = printer() # for solar velocity print out

	if args.graph:
		plot = Plotter(dict(zip(names,styles)),axis=[-9e11,9e11,-9e11,9e11],position=111)
			# maxpoints=args.maxpoints,bufsize=100,rtol=0,atol=1e7)
	# if args.energy:
		# plot.add_subplot({'Energy %':'r','KE %':'b','PE %':'g'},
		# 	position=[0.2,0.1,0.6,0.2],axis=[0,t*dt/86400,-7.5e35,4e35],bufsize=183)
	# if args.energy:
		# plot = Plotter({'Energy %':'red','KE %':'blue','PE %':'green'},
			# position=211,axis=[0,t*dt/86400,-7.5e35,4e35])
	if args.period:
		angle=Angle(solar_system,args.period)
	if args.period or args.energy:
		pr = printer()
	if pr and args.progress:
		two = two_lines(args.progress,pr)
		args.progress = two
		pr = two
	
	# from time import sleep
	# sleep(7)

	# main execution loop
	for n in xrange(t):
		x,v = solar_system.leapfrog()
		
		if args.progress: args.progress.send(100*n/(t-1))

		# pr.send(['Solar Velocity:',
			# '%+.3e , %+.3e' % tuple(solar_system.v[0][0:2].tolist())])
		# pr.send(['Force on Sun:',
			# '%+.3e , %+.3e' % tuple(solar_system.a[0][0:2].tolist())])
		# pr.send(['Centre of Mass Velocity:',
			# '%+.3e , %+.3e' % tuple(find_barycentre_v(solar_system)[0:2])])

		if args.graph: plot.send(dict(zip(names,x[:,0:2].tolist())))
		if args.energy:
			args.energy(solar_system)
			strf = '%+.3e'
			pr.send([
				"Time:",str(solar_system.t),
				"KE: %",strf % args.energy.ke,
				"PE: %",strf % args.energy.pe,
				"Energy %:",strf % args.energy.total,
				# "Virial:", strf % args.energy.virial
				])
			# plot.send({
			# 	'KE %':(n*dt/86400,args.energy.ke),
			# 	'PE %':(n*dt/86400,args.energy.pe),
			# 	'Energy %':(n*dt/86400,args.energy.total)
			# 	})
		if args.period:
			theta = angle(solar_system)
			# if theta > 90: break
			pr.send([
				"Angle:",'%03d' % theta,
				# period in days
				"Period:",'%06.2f' % (angle.period/86400)
				])
		if pr: pr.send(None)
