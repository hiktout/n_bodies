import numpy as np
from metrics import Energy

class Energy(Energy):
	def kinetic_energy(self,n):
		"""
		Find the total kinetic energy of an N bodies system.
		
		Takes an N_bodies instance.
		"""
		# align pe and ke by moving velocity a half-step
		v = n.v - 0.5*n.a*n.dt
		ke = n.m[:,np.newaxis]*np.square(v)
		return 0.5*np.sum(ke)

	def potential_energy(self,n):
		"""
		Find the total gravitational potential energy
		of an N bodies system.
		
		Takes an N_bodies instance
		"""
		# Potential is sum of potential of each pair of masses
		
		U = n.mmG_u/np.sqrt(n.r_norm2_u)
		return np.sum(U)
