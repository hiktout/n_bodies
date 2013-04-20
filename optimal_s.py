"""
Script to find optimum softening constant in N_bodies simulation.
Uses method described in Athanassoula et al (2000), 2000MNRAS.314..475A,
where the mean average square error is found for varying values of
the softening constant
"""

import numpy as np

from n_body.fast import N_bodies
from metrics.error import ase,F_sphere,F_plummer

from util.rand import random_positions,plummer_model

if __name__ == '__main__':
	# M = 2e30 # about solar mass
	# N = 500
	# M = 2e42 # total mass, about DM halo according to wikipediaNMR
	# m = M/N # individual mass
	# R = 8e21

	# use scaled units as in A+00
	# N_bodies.G = 1
	# N = 2000
	# M = 1.0/N
	# R = 38.71

	# virial units
	N = 500
	M = 1.
	m = M/N
	R = 1.

	# characteristic radius (half mass radius) for homogenous sphere
	# R_c = R/2**(1./3.)
	# half mass radius for plummer sphere
	# R_c = Rv*3.*np.pi/16.*(2**(2./3.) - 1)**(-0.5)
	# unweighted
	R_c = 1
	# MASE normalisation constant
	# C = R_c**4/M**2
	C = 1
	# number of realisations
	times = int(3e4/N)
	# function for true force
	f_true = F_sphere(R,M)
	# f_true = F_plummer(Rv,M)

	n = N_bodies(
		m*np.ones(N),
		np.zeros((N,3)),
		np.zeros((N,3)),
		1,0
	)

	# from plotter_anim import Plotter
	# plot = Plotter({'mase':'black'},axis=[0,2,0,1],position=211)
	# plot.show()

	# for information
	print '#','sphere','N',N,'M',M,'R',R,'R_c',R_c,'C',C,'times',times

	# do for many values of softening
	for softening in np.linspace(0,2,0.01):

		n.s2 = (softening*R_c)**2

		mase = 0.0

		for _ in xrange(times):
			n.x = random_positions(R,N)
			# n.x,n.v = plummer_model(Rv,N)
			mase += ase(n,f_true)

		mase /= times
		mase *= C

		print softening,mase
		# plot.send({'mase':(softening,mase)})
