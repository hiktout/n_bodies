import numpy

class Energy(object):
	def __init__(self):
		self.first = True

	def __call__(self,n):
		"""
		Calculate the energy of the system,
		and return the percent change in the
		total energy
		"""
		self.ke = self.kinetic_energy(n)
		self.pe = self.potential_energy(n)
		self.total = self.ke + self.pe
		self.virial = 2*self.ke + self.pe

		# save the initial energies
		if self.first:
			self.initial_total = self.total
			self.initial_ke = self.ke
			self.initial_pe = self.pe
			self.first = False

		self.percent_total = 100*(self.total/self.initial_total - 1)
		self.percent_ke = 100*(self.ke/self.initial_ke - 1)
		self.percent_pe = 100*(self.pe/self.initial_pe - 1)

		return self.percent_total

	def kinetic_energy(self,n):
		"""
		Find the total kinetic energy of an N bodies system.
		
		Takes an N_bodies instance.
		"""
		# align pe and ke by moving velocity a half-step
		v = n.v - 0.5*n.a*n.dt
		ke = n.m[:,numpy.newaxis]*numpy.square(v)
		return 0.5*numpy.sum(ke)

	def potential_energy(self,n):
		"""
		Find the total gravitational potential energy
		of an N bodies system.
		
		Takes an N_bodies instance
		"""
		# Potential is sum of potential of each pair of masses
		
		U = n.mG*n.m[:,numpy.newaxis]/numpy.sqrt(n.r_norm2)
		numpy.fill_diagonal(U,0) # get rid of self-potentials
		
		# pairs are repeated twice
		return 0.5*numpy.sum(U)
