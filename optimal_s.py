import numpy as np

from n_bodies_fast import N_bodies
from metrics.error import ase,F_sphere

from rnd_cluster import random_positions

if __name__ == '__main__':
	# M = 2e30 # about solar mass
	# R = 7e19
	# V = 1e3
	# N = 2000

	N = 2000
	M = 1.0/N
	R = 38.71

	# characteristic radius (half mass radius) for homogenous sphere
	R_c = R/2**(1./3.)
	# MASE normalisation constant
	# C = R_c**4/(M*N)**2
	C=1
	# number of realisations
	times = int(3e5/N)

	N_bodies.G = 1

	n = N_bodies(
		M*np.ones(N),
		np.zeros((N,3)),
		np.zeros((N,3)),
		1,0
	)

	# from plotter_anim import Plotter
	# plot = Plotter({'mase':'black'},axis=[0,2,0,1],position=211)
	# plot.show()

	# do for many values of softening
	for softening in np.arange(387,390,1):
		softening /= 100.0

		n.s2 = (softening)**2

		mase = 0.0

		for _ in xrange(times):
			n.x = random_positions(R,N)
			mase += ase(n,F_sphere(R))

		mase /= times
		mase *= C

		print softening,mase
		# plot.send({'mase':(softening,mase)})
