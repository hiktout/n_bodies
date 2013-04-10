import numpy

class N_bodies(object):
	"""
	Simulates the time evolution of a system
	of N particles which interact with each
	other through gravitational forces.

	After creating a N_bodies simulation,
	step forward using N_bodies.leapfrog()
	"""
	G = 6.67384e-11 # gravitational constant

	def __init__(self,mass,position,velocity,dt,softening):
		"""
		Create the simulation, giving initial values
		of particle masses, positions and velocities.

		Masses can be a 1D array or a scalar; if a scalar
		all particles will have the same mass. Position
		and velocity must be numpy arrays of the same shape;
		normally the last axis will have length 3, to give a
		list of vectors. Each particle is defined by the same
		index across all three arrays.

		dt is the time step in seconds between each simulation
		step.
		softening is a constant that reduces the gravitational
		force for particles close to each other.
		"""
		self.n = len(position)

		self.m = np.empty(self.n)
		self.m[...] = mass
		self.mG = -self.G*self.m # precalculate to save time

		# we do it this way to make
		# sure inputs are consistent
		self.x = np.empty((self.n,3))
		self.x[...] = position
		self.v = np.empty((self.n,3))
		self.v[...] = velocity
		
		self.dt = dt
		self.s2 = softening**2 # we only use square
		
		# make some definitions up front to allocate
		# memory and to have a clear definition of
		# expected array shapes
		self.r = numpy.empty((self.n,self.n,3))
		self.r_norm2 = numpy.empty((self.n,self.n))
		self.F = numpy.empty((self.n,self.n,3))
		self.a = numpy.empty((self.n,3))

		# current run time in seconds
		self.t = 0
	
	def find_r(self):
		"""
		Creates a matrix with ij elements x_i - x_j;
		ie a matrix of displacement vectors between
		particles i and j
		"""
		# x[:,numpy.newaxis,:] transposes and extends x;
		# put another way x.shape is changed from
		# (n,3) to (n,newaxis,3), and then the subtraction
		# of x broadcasts newaxis to have size n
		self.r[...] = self.x[:,numpy.newaxis,:]-self.x
		# magnitude of each displacement vector
		# self.r_norm[...] = numpy.apply_along_axis(numpy.linalg.norm,2,self.r)
		# or this: ugly but fast
		# don't sqrt since we square in F
		self.r_norm2[...] = self.r[:,:,0]*self.r[:,:,0]+self.r[:,:,1]*self.r[:,:,1]+self.r[:,:,2]*self.r[:,:,2]

	def find_a(self):
		"""
		Creates an array of acceleration vectors for each particle
		""" 
		# simple Newtonian gravitational force
		self.F[...] = self.r*(self.mG/(self.r_norm2 + self.s2)**1.5)[:,:,numpy.newaxis]
		# tmp = (self.r_norm2 + self.s2)
		# tmp = numpy.sqrt(tmp*tmp*tmp)
		# self.F[...] = (self.mG/tmp)[:,:,numpy.newaxis]
		# self.F *= self.r
		# self.F[...] = numpy.nan_to_num(self.F) # div by zero gives NaN
		# F not true force since does not include m_i
		# sum 'forces' to get acceleration
		self.a[...] = numpy.sum(self.F,1)

	def update_v(self):
		"""
		Update the velocities using the accelerations found
		"""
		self.v += self.a*self.dt

	def update_x(self):
		"""
		Update the positions using the velocities found
		"""
		self.x += self.v*self.dt

	def v_correction(self):
		"""
		Helper function to get the positions and velocities
		1/2 dt out of time with each other. The leapfrog
		algorithm requires this
		"""
		self.find_r()
		self.find_a()
		self.v -= self.a*self.dt/2.0

	def leapfrog(self):
		"""
		Use the leapfrog algorith to step the state of the
		simulation dt seconds forward in time. This is the
		primary function of the N_bodies class
		"""
		self.find_r()
		self.find_a()
		self.update_v()
		self.update_x()

		self.t += self.dt

class N_view(object):
	def __init__(self,n,index):
		self.n = n
		self.idx = index

	def __getattribute__(self,name):
		n = object.__getattribute__(self,'n')
		index = object.__getattribute__(self,'idx')
		d = getattr(n,name)
		if isinstance(d,numpy.ndarray) and len(d) == n.n:
			return d[index]
		else:
			raise AttributeError
