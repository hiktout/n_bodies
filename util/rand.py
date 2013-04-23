from numpy import pi,cos,sin
from numpy import sqrt,transpose,zeros

from numpy.random import uniform

def spherical(r,N):
	theta = uniform(0,2*pi,N)
	u = uniform(-1,1,N)
	sinphi = sqrt(1-u**2)

	x = r*cos(theta)*sinphi
	y = r*sin(theta)*sinphi
	z = r*u

	x = transpose((x,y,z))

	return x

def random_positions(R,N):
	r = R*uniform(0,1,N)**(1./3.)
	
	x = spherical(r,N)

	return x

def random_velocities(V,N):
	v_x = uniform(-V,V,N)
	v_y = uniform(-V,V,N)
	v_z = uniform(-V,V,N)

	v = transpose((v_x,v_y,v_z))

	return v

def plummer_model(Rv,N):
	a = Rv*3.*pi/16. # plummer scale length

	r = (uniform(0,1,N)**(-2./3.) - 1)**(-0.5)
	x = a*spherical(r,N)

	v = plummer_q(N)*sqrt(2)*(1 + r**2)**(-0.25)
	v = spherical(v,N) / sqrt(a)

	return x,v

def plummer_q(N):
	q = zeros(N)
	g_q = zeros(N)+0.1

	for i in xrange(N):
		while g_q[i] > q[i]**2 * (1 - q[i]**2)**(7./2.):
			q[i] = uniform(0,1)
			g_q[i] = uniform(0,0.1)

	return q
