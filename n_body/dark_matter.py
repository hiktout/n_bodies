import numpy as np

from n_bodies_fast import N_bodies

from metrics import find_barycentre

class Dark_bodies(N_bodies):
	rho = (4.*np.pi/3.)*N_bodies.G*6.25e-22 # dark matter density*G*4pi/3

	def __init__(self,m,x,v,dt,s):
		super(Dark_bodies,self).__init__(m,x,v,dt,s)

		# transform to an inertial frame
		# o = find_barycentre(self)
		# print o
		# self.x -= o

		# offset dark matter halo
		self.o = np.array([-1e14,0,0])

	def find_a(self):
		super(Dark_bodies,self).find_a()

		# spherical volume of dark matter centred around barycentre
		# a = -G * 4pi/3 r^3 * density / r^2
		self.a -= self.rho*(self.o-self.x)
