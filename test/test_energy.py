import unittest
from numpy.testing import assert_allclose

from numpy.random import rand

from metrics.energy import Energy
from n_body import N_bodies

from reference import kinetic_energy,potential_energy

class TestEnergyFunctions(unittest.TestCase):

	def setUp(self):
		self.n = 10
		self.m = rand(self.n)
		self.x = rand(self.n,3)
		self.v = rand(self.n,3)
		self.dt = 10*rand(1)
		self.s = rand(1)

		self.n_bodies = N_bodies(self.m,self.x,self.v,self.dt,self.s)
		self.energy = Energy(self.n_bodies)

	def test_kinetic_energy(self):
		self.assertTrue(self.energy.ke)
		assert_allclose(self.energy.ke,kinetic_energy(self.n,self.m,self.v))

	def test_potential_energy(self):
		self.assertTrue(self.energy.pe)
		assert_allclose(self.energy.pe,potential_energy(self.n,self.m,self.x))

if __name__ == '__main__':
	unittest.main()