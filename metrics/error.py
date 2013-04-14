from numpy import sum

from . import dot

from n_bodies_fast import N_bodies

def F_sphere(R):
	R3 = R**3
	def F_true(n):
		m = sum(n.m)
		true = -n.G*m*n.x/R3
		return true
	return F_true

def ase(n,f_true):
	n.find_r()
	n.find_a()

	# use function f_true 
	# to find true force
	true = f_true(n)

	mase = n.a - true
	mase = dot(mase,mase)
	mase = sum(mase)/n.n

	return mase
