import numpy

def find_barycentre(n):
	"""
	Find the position of the barycentre
	of all the bodies in an N body simulation.
	
	Takes an N_bodies instance,
	Returns a position vector.
	"""
	return numpy.sum(n.x*n.m[:,numpy.newaxis],axis=0)/numpy.sum(n.m)

def find_barycentre_v(n):
	"""
	Find the velocity of the barycentre

	Takes an N_bodies instance,
	Returns a velocity vector.
	"""
	return numpy.sum(n.v*n.m[:,numpy.newaxis],axis=0)/numpy.sum(n.m)

class Angle:
	"""
	Find the angle the vector from the barycentre
	to body i sweeps out. The initial vector is stored
	when this class is instantiated, and a calls to
	the istance will find the angle between the
	initial vector and the new vector.

	The positions are read from an N_bodies instance.
	"""
	def __init__(self,n,i):
		"""
		Create an instance of an Angle accumulator.

		Takes an N_bodies instance and the index of
		the body we wish to track.
		"""
		self.i = i
		self.angle = 0
		self.p = 0
		self.period = 0
		self.turns = 0
		self.interval = 0

		self.r0_unit = n.x[self.i] - find_barycentre(n)
		self.r0_unit /= numpy.linalg.norm(self.r0_unit)

	def __call__(self, n):
		"""
		Find the angle swept out from the initial vector,
		in degrees.

		Takes an N_bodies instance.
		Returns an angle in degrees.
		"""
		self.r1_unit = n.x[self.i] - find_barycentre(n)
		self.r1_unit /= numpy.linalg.norm(self.r1_unit)

		self.angle += self.find_angle()

		if (self.angle % 360) != self.angle:
			self.angle %= 360
			self.turns += 1

			# find mean period
			self.p += n.t - self.interval
			self.period = self.p/float(self.turns)

			self.interval = n.t

		self.r0_unit = self.r1_unit

		return self.angle

	def find_angle(self):
		"""
		Calculate the angle between two vectors in degrees
		"""
		cos = numpy.dot(self.r0_unit,self.r1_unit)
		angle = numpy.degrees(numpy.arccos(cos))

		# edge cases where r0 and r1 are
		# parallel or antiparallel
		if numpy.isnan(angle):
			print angle,self.r0_unit,self.r1_unit
			if (self.r0_unit==self.r1_unit).all():
				return 0.0
			else:
				return 180
		return angle

class Energy(object):
	def __init__(self):
		self.first = True

	def __call__(self,n):
		"""
		Calculate the energy of the system,
		and return the percent change in the
		total energy
		"""
		self.ke = self.kinetic_energy(n)
		self.pe = self.potential_energy(n)
		self.total = self.ke + self.pe
		self.virial = 2*self.ke + self.pe

		# save the initial energies
		if self.first:
			self.initial_total = self.total
			self.initial_ke = self.ke
			self.initial_pe = self.pe
			self.first = False

		self.percent_total = 100*(self.total/self.initial_total - 1)
		self.percent_ke = 100*(self.ke/self.initial_ke - 1)
		self.percent_pe = 100*(self.pe/self.initial_pe - 1)

		return self.percent_total

	def kinetic_energy(self,n):
		"""
		Find the total kinetic energy of an N bodies system.
		
		Takes an N_bodies instance.
		"""
		# align pe and ke by moving velocity a half-step
		v = n.v - 0.5*n.a*n.dt
		ke = n.m[:,numpy.newaxis]*numpy.square(v)
		return 0.5*numpy.sum(ke)

	def potential_energy(self,n):
		"""
		Find the total gravitational potential energy
		of an N bodies system.
		
		Takes an N_bodies instance
		"""
		# Potential is sum of potential of each pair of masses
		
		U = n.mG*n.m[:,numpy.newaxis]/numpy.sqrt(n.r_norm2)
		numpy.fill_diagonal(U,0) # get rid of self-potentials
		
		# pairs are repeated twice
		return 0.5*numpy.sum(U)

def dot(a,b):
	assert len(a) == len(b)
	return a[:,0]*b[:,0] + a[:,1]*b[:,1] + a[:,2]*b[:,2]

def angular_v(n):
	o = find_barycentre(n)
	r = o - n.x

	w = numpy.cross(r,n.v)/dot(r,r)[:,numpy.newaxis]
	w *= 1e22

	o = numpy.tile(o,(len(w),1))
	arrow = numpy.array((o,(o+w)))
	arrow = arrow.transpose((1,0,2)).reshape(2*len(w),3)

	# arrow = numpy.vstack((o,o+numpy.sum(w,axis=0)))

	return arrow

A = 500/numpy.sqrt(2*numpy.pi)

def gaussF(x,a,s):
	return a*numpy.exp(-0.5*(x/s)**2)

gauss = numpy.vectorize(gaussF)

## TODO
# def einastoF(x,a):
# 	return a*numpy.exp(-x**0.17)

def position_dist(n):
	o = find_barycentre(n)
	r = o - n.x
	# r = numpy.apply_along_axis(numpy.linalg.norm,-1,r)
	# r_h = numpy.histogram(r,bins=30)
	x = numpy.histogram(r[:,0],bins=30)
	y = numpy.histogram(r[:,1],bins=30)
	z = numpy.histogram(r[:,2],bins=30)

	# v = numpy.linspace(r.min(),r.max(),1000)
	# r_s = numpy.std(r)
	# r_fit = gauss(v,r_h[0].max(),r_s)
	# x_s = numpy.std(r[:,0])
	# y_s = numpy.std(r[:,1])
	# z_s = numpy.std(r[:,2])
	# x_fit = gauss(v,x_s)
	# y_fit = gauss(v,y_s)
	# z_fit = gauss(v,z_s)

	# return {'x':x,'x_fit':(x_fit,v),'y':y,'y_fit':(y_fit,v),'z':z,'z_fit':(z_fit,v)}
	return {'x':x,'y':y,'z':z}
	# return {'x_fit':(x_fit,v),'y_fit':(y_fit,v),'z_fit':(z_fit,v)}
	# return {'r':r_h,'r_fit':(r_fit,v)}
