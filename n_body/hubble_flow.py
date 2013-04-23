from .fast import N_bodies

class Hubble_Bodies(N_bodies):
	H = 75

	def __init__(self,m,x,v,dt,softening,initial_time=1e-9):
		super(Hubble_Bodies,self).__init__(m,x,v,dt,softening)

		self.t = initial_time
		# assume initial positions are in comoving coordinates
		# self.x *= self.scale_factor()
		# self.v *= self.scale_factor()

	def scale_factor(self):
		return (self.t*self.H*3/2)**(2./3.)

	def update_v(self):
		"""
		Include Hubble flow in velocity, to simulate expansion
		"""
		self.v += self.dt/self.scale_factor()

	def update_x(self):
		self.x += self.v*self.dt/self.scale_factor()**2
