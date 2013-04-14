import numpy as np

def random_positions(R,N):
	r = np.random.uniform(0,R,N)
	theta = np.random.uniform(0,2*np.pi,N)
	u = np.random.uniform(-1,1,N)
	sinphi = np.sqrt(1-u**2)

	x = r*np.cos(theta)*sinphi
	y = r*np.sin(theta)*sinphi
	z = r*u

	x = np.transpose((x,y,z))

	return x

def random_velocities(V,N):
	v_x = np.random.uniform(-V,V,N)
	v_y = np.random.uniform(-V,V,N)
	v_z = np.random.uniform(-V,V,N)

	v = np.transpose((v_x,v_y,v_z))

	return v

if __name__ == '__main__':
	M = 2e30 # about solar mass
	R = 7e19
	V = 1e3
	N = 500

	day = 86400
	year = 365*day

	T = 3e11*year

	m = M*np.ones(N)
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
	from n_bodies_fast import N_bodies
	
	cluster = N_bodies(m,x,v,year*1e8,softening=0.2)

	# from n_bodies import N_view

	# c1 = N_view(cluster,np.s_[:N/4])
	# c2 = N_view(cluster,np.s_[N/4:N/2])
	# c3 = N_view(cluster,np.s_[N/2:3*N/4])
	# c4 = N_view(cluster,np.s_[3*N/4:])

	# BLACK HOLE
	# bh_l = range(N)
	# bh_l.remove(bh)
	# c = N_view(cluster,bh_l)

	from metrics_fast import Energy
	energy = Energy()

	from plotter_anim import Plotter
	data_plot = Plotter({'Energy':'red','KE':'blue','PE':'green'},
		axis=[0,T,-4e36,2e37],position=211)
	data_plot.show()

	# cluster.find_r()
	# V = -0.5*energy.potential_energy(cluster)/(N*np.sum(m)) # average velocity from virial
	# print V
	# v = random_velocities(V,N)
	# cluster = N_bodies(m,x,v,year,0.1*R)

	from plotter3D import Plotter3D
	plot = Plotter3D({
		'x':{'color':(1,1,1,0.5),'size':3.0},
		'bh':{'color':(1,0,0,1),'size':6.0},
		'w1':{'color':(0,1,0,0.5),'line':True},
		# 'w2':{'color':(0,1,0,0.5),'line':True},
	},4*R)

	# from metrics import position_dist
	# from plotter_chaco import HistPlotter
	# hist = HistPlotter({'x':'red','x_fit':'red','y':'green','y_fit':'green','z':'blue','z_fit':'blue'})
	# hist = HistPlotter({'x':'red','y':'green','z':'blue'})
	# hist = HistPlotter({'r':'red','r_fit':'green'})

	# from plotter_chaco import QuiverPlotter
	# quiver = QuiverPlotter(N)

	from coroutines import printer
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
				'PE':(cluster.t,energy.pe)
			})
			strf = '%+.3e'
			pr.send(['Time (yr):', str(cluster.t/year), '|'])
			pr.send(['Virial:', strf % energy.virial])
			pr.send([
				# 'Time:', str(cluster.t), '|',
				'Total Energy:', strf % energy.total, '|',
				'Kinetic Energy:', strf % energy.ke, '|',
				'Potential Energy:', strf % energy.pe,
			])

			pr.send(None)
			# if cluster.t >= T:
			# 	print 'end'
			# 	break
	except KeyboardInterrupt:
		pass
		# plot.close()
		# data_plot.close()