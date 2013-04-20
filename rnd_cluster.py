import numpy as np

from util.rand import random_positions,random_velocities

if __name__ == '__main__':
	# M = 2e30 # about solar mass
	# N = 500
	# M = 2e42
	# R = 1e22

	# day = 86400
	# year = 365*day

	# T = 14e9*year # hubble time

	N = 500
	M = 1.
	R = 1.

	m = (M/N)*np.ones(N)
	x = random_positions(R,N)
	# v = random_velocities(V,N)
	v = np.zeros((N,3))

	# bh = np.random.random_integers(0,N) # BLACK HOLE
	# m[bh] = 10*M # BLACK HOLE
	# x[bh] = [2*R,0,0] # BLACK HOLE
	# v[bh] = [0,V,0] # BLACK HOLE

	# split into four clusters
	# x[:N/4] += [2*R,0,0]
	# x[N/4:N/2] += [-2*R,0,0]
	# x[N/2:3*N/4] += [0,2*R,0]
	# x[3*N/4:] += [0,-2*R,0]

	# from dark_matter import Dark_bodies
	from n_body.fast import N_bodies
	N_bodies.G = 1
	
	# cluster = N_bodies(m,x,v,year*1e5,softening=0.595*R)
	cluster = N_bodies(m,x,v,0.01,softening=0.1)

	# from n_bodies import N_view

	# c1 = N_view(cluster,np.s_[:N/4])
	# c2 = N_view(cluster,np.s_[N/4:N/2])
	# c3 = N_view(cluster,np.s_[N/2:3*N/4])
	# c4 = N_view(cluster,np.s_[3*N/4:])

	# BLACK HOLE
	# bh_l = range(N)
	# bh_l.remove(bh)
	# c = N_view(cluster,bh_l)

	from metrics.energy_fast import Energy
	energy = Energy(cluster)

	from plotter import LinePlotter
	data_plot = LinePlotter({'Energy':'red','KE':'blue','PE':'green','Virial':'purple'},
		# axis=[0,T,-5e53,2e53],position=211)
		axis=[0,100,-6,2],position=211)
	from metrics.dist import quartiles
	data_plot.add_plot({'R_h':'blue','R':'red'},axis=[0,100,0,2],position=212)
	data_plot.show()

	# cluster.find_r()
	# V = -0.5*energy.potential_energy(cluster)/(N*np.sum(m)) # average velocity from virial
	# print V
	# v = random_velocities(V,N)
	# cluster = N_bodies(m,x,v,year,0.1*R)

	from plotter import Plotter3D
	plot = Plotter3D({
		'x':{'color':(1,1,1,0.5),'size':3.0},
		'bh':{'color':(1,0,0,1),'size':6.0},
		'w1':{'color':(0,1,0,0.5),'line':True},
		# 'w2':{'color':(0,1,0,0.5),'line':True},
	},2*R)

	# from metrics.dist import position_dist
	# from plotter import HistPlotter
	# hist = HistPlotter({'x':'red','x_fit':'red','y':'green','y_fit':'green','z':'blue','z_fit':'blue'})
	# hist = HistPlotter({'x':'red','y':'green','z':'blue'})
	# hist = HistPlotter({'r':'red','r_fit':'green'})

	# from plotter_chaco import QuiverPlotter
	# quiver = QuiverPlotter(N)

	from util.coroutines import printer
	pr = printer()

	# from metrics import angular_v
	# from metrics import find_barycentre

	# from density import density
	# d = density(30,0.3*R)

	try:
		while True:
			cluster.leapfrog()

			# a1 = angular_v(cluster)
			# a1 = angular_v(c1)
			# a2 = angular_v(c2)

			# o = np.vstack((find_barycentre(c1),find_barycentre(c2)))

			plot.send({
				'x':cluster.x,
				# 'bh':cluster.x[np.newaxis,bh],
				# 'bh':c1.x,
				# 'w1':a1,
				# 'w2':a2,
			})
			
			# d.send(cluster.x)

			# quiver.send((x[:,1],x[:,2],v[:,0:2]/V))

			# hist.send(position_dist(cluster))

			# pr.send((str(find_barycentre(cluster)),))

			energy(cluster)
			data_plot.send({
				'Energy':(cluster.t,energy.total),
				'KE':(cluster.t,energy.ke),
				'PE':(cluster.t,energy.pe),
				'Virial':(cluster.t,energy.virial),
			})
			strf = '%+.3f'
			# pr.send(['Time (Gyr):', '%.2f' % (cluster.t/(1e9*year)), '|'])
			pr.send(['Virial:', strf % energy.virial])
			pr.send([
				# 'Time:', str(cluster.t), '|',
				'Total Energy:', strf % energy.total, '|',
				'Kinetic Energy:', strf % energy.ke, '|',
				'Potential Energy:', strf % energy.pe,
			])

			q = quartiles(cluster)
			data_plot.send({
				'R_h':(cluster.t,q[1]),
				'R':(cluster.t,q[3]),
			})

			pr.send(None)
			# if cluster.t >= T:
			# 	print 'end'
			# 	break
	except KeyboardInterrupt:
		pass
		# plot.close()
		# data_plot.close()