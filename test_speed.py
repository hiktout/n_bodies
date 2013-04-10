import numpy
import cProfile

import n_bodies

m = 1e10
r_scale = 1e10
v_scale = 1e4

for N in range(100):
	x = r_scale*numpy.random.rand(N,3)
	v = v_scale*numpy.random.rand(N,3)

