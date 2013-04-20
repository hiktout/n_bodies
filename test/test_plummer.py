import unittest
from numpy.testing import assert_allclose,assert_array_less

from numpy import ones,sort,sqrt
from numpy.random import rand

from reference import kinetic_energy,potential_energy
from util import dot

from util.rand import plummer_model,plummer_q

class TestPlummerModel(unittest.TestCase):

	def setUp(self):
		self.N = 500
		self.rtol = 0
		self.atol = 1./sqrt(self.N)

		self.x,self.v = plummer_model(1,self.N)

	def test_plummer_q(self):
		q = plummer_q(self.N)

		assert_array_less(q,1)
		assert_array_less(0,q)

	def test_plummer_quartiles(self):
		r = dot(self.x,self.x)
		r = sort(r)
		r_1 = sqrt(r[round(self.N/4) - 1])
		r_2 = sqrt(r[round(self.N/2) - 1])
		r_3 = sqrt(r[round(3*self.N/4) - 1])
		r_4 = sqrt(r[self.N])

		# print r_1,r_2,r_3
		assert_allclose(0.4778,r_1,self.rtol,self.atol)
		assert_allclose(0.7686,r_2,self.rtol,self.atol)
		assert_allclose(1.2811,r_3,self.rtol,self.atol)

	def test_plummer_energy(self):
		m = 1./self.N*ones(self.N)

		times = 5
		E = ones(times)

		for i in xrange(times):
			ke = kinetic_energy(self.N,m,self.v)
			pe = potential_energy(self.N,m,self.x,G=1)
			E[i] = ke + pe
			# print ke,pe,E[i]
			self.x,self.v = plummer_model(1,self.N)

		assert_allclose(-0.25,E.mean(),self.rtol,self.atol)

if __name__ == '__main__':
	unittest.main()