import numpy as np

from n_body.fast import N_bodies
from util.rand import plummer_model

if __name__ == '__main__':
	# use virial units
	N = 500
	M = 1./N # individual mass, total mass is 1
	Rv = 1 # virial radius
	N_bodies.G = 1

	m = M*np.ones(N)
	x,v = plummer_model(1,N)

	cluster = N_bodies(m,x,v,dt=0.01,softening=0.04)

	from plotter import Plotter3D
	plot = Plotter3D({
		'x':{'color':(1,1,1,0.5),'size':3.0},
	},4*Rv)

	from metrics.energy_fast import Energy
	energy = Energy(cluster)

	from plotter import LinePlotter
	data_plot = LinePlotter({'Energy':'red','KE':'blue','PE':'green','Virial':'purple'},
		axis=[0,100,-1,1],position=211)
	from metrics.dist import quartiles
	data_plot.add_plot({'R_h':'red'},axis=[0,100,0,2],position=212)
	data_plot.show()

	from metrics.dist import position_dist
	from plotter import HistPlotter
	hist = HistPlotter({'x':'red','y':'green','z':'blue'})

	from util.coroutines import printer
	pr = printer()

	try:
		while 1:
			cluster.leapfrog()

			plot.send({
				'x':cluster.x,
			})

			energy(cluster)
			energy.percent_change()
			data_plot.send({
				'Energy':(cluster.t,energy.total),
				'KE':(cluster.t,energy.ke),
				'PE':(cluster.t,energy.pe),
				'Virial':(cluster.t,energy.virial),
			})
			strf = '%+.3f'
			pr.send(['Virial:', strf % energy.virial])
			pr.send([
				# 'Time:', str(cluster.t), '|',
				'Total Energy:', '%+5.2f%%' % energy.percent_total, '|',
				'Kinetic Energy:', strf % energy.ke, '|',
				'Potential Energy:', strf % energy.pe,
			])

			hist.send(position_dist(cluster))

			data_plot.send({
				'R_h':(cluster.t,quartiles(cluster)[1]),
			})

			pr.send([
				'|','New Timestep:',
				strf % (0.38*np.sqrt(cluster.s2)/cluster.v.max()),
			])

			pr.send(None)
	except KeyboardInterrupt:
		pass
