import unittest
from numpy.testing import assert_allclose

from numpy.random import rand

from n_body import N_bodies
from reference import *

class TestNbodiesClass(unittest.TestCase):

	def setUp(self):
		self.n = 10
		self.m = rand(self.n)
		self.x = rand(self.n,3)
		self.v = rand(self.n,3)
		self.dt = 10*rand(1)
		self.s = rand(1)

		self.n_bodies = N_bodies(self.m,self.x,self.v,self.dt,self.s)

	def test_find_r(self):
		self.n_bodies.find_r()

		assert_allclose(self.n_bodies.r,find_r(self.n,self.x))
		assert_allclose(self.n_bodies.r_norm2,find_r_norm2(self.n,self.x))

	def test_find_a(self):
		self.n_bodies.find_r()
		self.n_bodies.find_a()

		assert_allclose(self.n_bodies.F,find_F(self.n,self.m,self.x,self.v,self.s))
		assert_allclose(self.n_bodies.a,find_a(self.n,self.m,self.x,self.v,self.s))

	def test_leapfrog(self):
		for _ in xrange(100):
			self.n_bodies.leapfrog()
			x,v = leapfrog(self.m,self.x,self.v,self.dt,self.s)

			assert_allclose(self.n_bodies.x,x)
			assert_allclose(self.n_bodies.v,v)

if __name__ == '__main__':
	unittest.main()