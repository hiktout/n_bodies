from numpy import sum,sqrt,pi,newaxis

from util import dot

from n_body.fast import N_bodies

def F_sphere(R,M):
	R3 = R**3
	def F_true(n):
		# m = sum(n.m)
		true = -n.G*M*n.x/R3
		return true
	return F_true

def F_sphere_r(R,M,G=1):
	R3 = R**3
	def F_true(r):
		# m = sum(n.m)
		if r <= R:
			true = -G*M*r/R3
		if r > R:
			true = -G*M/r**2
		return true
	return F_true

def F_plummer(Rv,M):
	a2 = (Rv*3.*pi/16.)**2
	def F_true(n):
		r2 = dot(n.x,n.x)
		r_unit = n.x/sqrt(r2)[:,newaxis]
		true = -n.G*M*r_unit*((1 + a2/r2)**(-3./2.))[:,newaxis]
		return true
	return F_true

def F_plummer_r(Rv,M,G=1):
	a2 = (Rv*3.*pi/16.)**2
	def F_true(r):
		true = -G*M*r*((r**2 + a2)**(-3./2.))
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
