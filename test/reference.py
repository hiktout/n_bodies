import numpy as np

def find_r(n,x):
	r = np.zeros((n,n,3))

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r[i][j] = x[i]-x[j]

	return r

def find_r_u(n,x):
	r_u = np.zeros((n,n,3))
	i_u = np.triu_indices(n,1)

	for i in xrange(n):
		for j in xrange(n):
			if j < i: continue

			r_u[i][j] = x[i]-x[j]

	return r_u[i_u]

def find_r_norm2(n,x):
	r_norm2 = np.zeros((n,n))

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r = x[i]-x[j]

			r_norm2[i][j] = r[0]*r[0]+r[1]*r[1]+r[2]*r[2]

	return r_norm2

def find_r_norm2_u(n,x):
	r_norm2_u = np.zeros((n,n))
	i_u = np.triu_indices(n,1)

	for i in xrange(n):
		for j in xrange(n):
			if j < i: continue

			r = x[i]-x[j]

			r_norm2_u[i][j] = r[0]*r[0]+r[1]*r[1]+r[2]*r[2]

	return r_norm2_u[i_u]

def find_F(n,m,x,v,s):
	F = np.zeros((n,n,3))

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r = x[i]-x[j]
			r_norm = np.linalg.norm(r)
			r_norm = (r_norm**2 + s**2)**1.5
			F[i][j] = -G*m[j]*r/r_norm

	return F

def find_F_u(n,m,x,v,s):
	F_u = np.zeros((n,n,3))
	i_u = np.triu_indices(n,1)

	for i in xrange(n):
		for j in xrange(n):
			if j < i: continue

			r = x[i]-x[j]
			r_norm = np.linalg.norm(r)
			r_norm = (r_norm**2 + s**2)**1.5
			F_u[i][j] = r/r_norm

	return F_u[i_u]

def find_a(n,m,x,v,s,G=6.67384e-11):
	a = np.zeros((n,3))

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r = x[i]-x[j]
			r_norm = np.linalg.norm(r)
			r_norm = (r_norm**2 + s**2)**1.5
			a[i] += -G*m[j]*r/r_norm

	return a

def leapfrog(m,x,v,dt,s):
	n = len(x)

	F = np.zeros((n,3))

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r = x[i]-x[j]
			r_norm = np.linalg.norm(r)
			r_norm = (r_norm**2 + s**2)**1.5
			F[i] += -G*m[i]*m[j]*r/r_norm

		v[i] += F[i]*dt/m[i]
		x[i] += v[i]*dt

	return x,v

def kinetic_energy(n,m,v):
	ke = 0.0

	for i in xrange(n):
		v2 = np.linalg.norm(v[i])**2
		ke += 0.5*m[i]*v2

	return ke

def potential_energy(n,m,x,G = 6.67384e-11):
	pe = 0.0

	for i in xrange(n):
		for j in xrange(n):
			if i == j: continue

			r = x[i]-x[j]
			r = np.linalg.norm(r)

			pe += -0.5*G*m[i]*m[j]/r

	return pe