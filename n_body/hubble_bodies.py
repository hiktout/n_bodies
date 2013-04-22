from .fast import N_Bodies

class Hubble_Bodies(N_Bodies):
	H = 1.18477 # naive constant Hubble parameter, for now

	def update_v(self):
		"""
		Include Hubble flow in velocity, to simulate expansion
		"""
		super(Hubble_Bodies,self).update_v()

		self.v += H*self.x
