import unittest
from numpy.testing import assert_allclose,assert_array_less

from numpy.random import rand,uniform

from numpy import dot as npdot
from numpy import zeros

from util import dot
from util.rand import spherical,random_positions

class TestMiscellaneous(unittest.TestCase):

	def test_dot_list(self):
		n = 10
		a = rand(n,3)
		b = rand(n,3)

		np = zeros(n)
		for i in xrange(n):
			np[i] = npdot(a[i],b[i])

		assert_allclose(np,dot(a,b))

	def test_dot_matrix(self):
		n = 10
		a = rand(n,n,3)
		b = rand(n,n,3)

		np = zeros((n,n))
		for i in xrange(n):
			for j in xrange(n):
				np[i,j] = npdot(a[i,j],b[i,j])

		assert_allclose(np,dot(a,b))

	def test_spherical_lim(self):
		R = uniform(0,10)
		N = uniform(0,1000)

		x = spherical(R,N)

		r = dot(x,x)

		assert_allclose(R**2,r)

	def test_random_positions_lim(self):
		R = uniform(0,10)
		N = uniform(0,1000)

		x = random_positions(R,N)
		r = dot(x,x)
		assert_array_less(r,R**2)

	def test_random_positions_lim_fraction(self):
		R = uniform(0,1)
		N = uniform(0,1000)

		x = random_positions(R,N)
		r = dot(x,x)
		assert_array_less(r,R**2)

if __name__ == '__main__':
	unittest.main()