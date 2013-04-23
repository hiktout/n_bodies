import numpy as np
from util import dot

from .fast import N_bodies

class Hubble_Bodies(N_bodies):
	Omega0 = 1.
	H0 = 75.

	def __init__(self,m,x,v,dt,softening,initial_time=1e-9):
		super(Hubble_Bodies,self).__init__(m,x,v,dt,softening)

		self.t = initial_time

		# create comoving coordinates
		# assume initial positions are in comoving coordinates
		self.x_c = self.x.copy()
		self.v_c = self.v.copy()
		# correct physical coordinates
		self.x *= self.scale()
		self.v *= self.scale()
		self.v += self.hubble()*self.x

	def scale(self):
		return (self.t*self.H0*3./2.)**(2./3.)

	def hubble(self):
		return 2./(3.*self.t)

	def find_r(self):
		self.r[...] = self.x_c[:,np.newaxis,:]-self.x_c
		self.r_u[...] = self.r[self.i_u]
		self.r_norm2_u[...] = dot(self.r_u,self.r_u)

	def find_a(self):
		super(Hubble_Bodies,self).find_a()

		self.a += 0.5*self.Omega0*self.x_c*self.H0**2
		self.a /= self.scale()**2

	def update_v(self):
		"""
		Include Hubble flow in velocity, to simulate expansion
		"""
		self.v_c += (self.a - self.hubble()*self.v_c)*self.dt

	def update_x(self):
		self.x_c += self.v_c*self.dt/self.scale()

	def leapfrog(self):
		super(Hubble_Bodies,self).leapfrog()

		# convert to physical coordinates
		self.x = self.scale()*self.x_c
		self.v = self.v_c + self.hubble()*self.x
