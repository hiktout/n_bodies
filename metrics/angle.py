import numpy

from . import find_barycentre

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
