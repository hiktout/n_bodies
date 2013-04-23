import numpy as np

from n_body.hubble_flow import Hubble_Bodies

from util.rand import random_positions

if __name__ == '__main__':
	# Hubble units
	N = 500
	M = 10**12 # h^-1 M_sun
	Rv = 0.163 # h^-1 Mpc
	tH = 1./75 # Mpc (km/s)^-1 # Hubble time
	Hubble_Bodies.G = 2.42e-9 # h^-2 Mpc M_sun^-1 (km/s)^2

	m = (M/N)*np.ones(N)
	x = random_positions(Rv,N)
	v = np.zeros((N,3))

	print x

	cluster = Hubble_Bodies(m,x,v,1e-3*tH,softening=0.1,initial_time=2.8e-7) # Mpc (km/s)^-1 # initial time, from Gunn & Gott

	# from plotter import Plotter3D
	# plot = Plotter3D({
	# 	'x':{'color':(1,1,1,0.0),'size':3.0},
	# },4*Rv)

	from metrics.energy_fast import Energy
	energy = Energy(cluster)

	from plotter import LinePlotter
	data_plot = LinePlotter({'Energy':'red','KE':'blue','PE':'green','Virial':'purple'},
		axis=[0,1,-2e16,2e16],position=211)
	from metrics.dist import quartiles
	data_plot.add_plot({'R_h':'blue','R_3/4':'green','R':'red'},
		axis=[0,1,0,5],position=212)
	data_plot.show()

	from util.coroutines import printer
	pr = printer()

	# for _ in range(100):
	# 	cluster.leapfrog()

	# 	print cluster.a
	# 	print cluster.v
	# 	print cluster.x
	# 	print 80*'-'

	try:
		while 1:
			cluster.leapfrog()

	# 		plot.send({
	# 			'x':cluster.x,
	# 		})

			energy(cluster)
	# 		energy.percent_change()
			data_plot.send({
				'Energy':(cluster.t/tH,energy.total),
				'KE':(cluster.t/tH,energy.ke),
				'PE':(cluster.t/tH,energy.pe),
				'Virial':(cluster.t/tH,energy.virial),
			})
			strf = '%+.3e'
			pr.send(['Time (Gyr):', '%.2f' % (cluster.t*978),'|'])
			pr.send(['Scale factor:',str(cluster.scale_factor())])
			# pr.send([
			# 	'Virial:', strf % energy.virial, '|',
			# 	'Total Energy:', strf % energy.total, '|',
			# 	'Kinetic Energy:', strf % energy.ke, '|',
			# 	'Potential Energy:', strf % energy.pe,
			# ])

			q = quartiles(cluster)
			data_plot.send({
				'R_h':(cluster.t/tH,q[1]/Rv),
				'R_3/4':(cluster.t/tH,q[2]/Rv),
				'R':(cluster.t/tH,q[3]/Rv),
			})
			pr.send([
				'R_h:',str(q[1]/Rv), '|',
				'R_3/4:',str(q[2]/Rv), '|',
				'R:',str(q[3]/Rv),
			])

	# 		pr.send([
	# 			'|','New Timestep:',
	# 			strf % (0.38*np.sqrt(cluster.s2)/cluster.v.max()),
	# 		])

			pr.send(None)
	except KeyboardInterrupt:
		pass
