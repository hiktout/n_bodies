import numpy as np
from util import dot

from . import N_bodies

class N_bodies(N_bodies):
	"""
	Hand optimised version of N_bodies class.
	See n_bodies.py for documentation
	"""

	def __init__(self,mass,position,velocity,dt,softening):
		self.n = len(position)

		self.m = np.empty(self.n)
		self.m[...] = mass
		self.mG = -self.G*self.m # precalculate to save time

		# we do it this way to make
		# sure inputs are consistent
		self.x = np.empty((self.n,3))
		self.x[...] = position
		self.v = np.empty((self.n,3))
		self.v[...] = velocity

		self.dt = dt
		self.s2 = softening**2 # we only use square
		
		# make some definitions up front to allocate
		# memory and to have a clear definition of
		# expected array shapes
		self.r = np.empty((self.n,self.n,3))
		self.F = np.empty((self.n,self.n,3))
		self.a = np.empty((self.n,3))

		# upper triangle sections
		self.i_u = np.triu_indices(self.n,1)
		self.n_u = (self.n**2-self.n)/2
		self.r_u = np.empty((self.n_u,3))
		self.r_norm2_u = np.empty((self.n_u,))
		self.F_u = np.empty((self.n_u,3))
		self.F[...] = 0
		# G*m_i
		self.mG_b = np.tile(self.mG,self.n).repeat(3).reshape(self.n,self.n,3)
		# for metrics use only!
		self.mmG_u = (self.mG[:,np.newaxis]*self.m)[self.i_u]

		# current run time in seconds
		self.t = 0

	def find_r(self):
		self.r[...] = self.x[:,np.newaxis,:]-self.x
		self.r_u[...] = self.r[self.i_u]
		self.r_norm2_u[...] = dot(self.r_u,self.r_u)

	def find_a(self):
		tmp = (self.r_norm2_u + self.s2)
		tmp = np.sqrt(tmp*tmp*tmp)
		self.F_u[...] = self.r_u/tmp[:,np.newaxis]
		# self.F_u[...] = np.nan_to_num(self.F_u)

		self.F.fill(0.0)
		self.F[self.i_u] = self.F_u
		self.F -= np.rollaxis(self.F,1) # skew-symmetrise
		self.F *= self.mG_b

		self.a[...] = np.sum(self.F,1)
