import unittest
from numpy.testing import assert_allclose

from numpy.random import rand

from numpy import dot as npdot
from numpy import zeros

from util import dot
from util.rand import spherical

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

		np = zeros(n,n)
		for i in xrange(n):
			for j in xrange(n):
				np[i,j] = npdot(a[i,j],b[i,j])

		assert_allclose(np,dot(a,b))

	def test_spherical_lim(self):
		x = spherical(1,100)

		r = dot(x,x)

		assert_allclose(1,r)

if __name__ == '__main__':
	unittest.main()