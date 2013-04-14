import numpy

from . import dot

def angular_v(n):
	o = find_barycentre(n)
	r = o - n.x

	w = numpy.cross(r,n.v)/dot(r,r)[:,numpy.newaxis]
	w *= 1e37

	# Individual
	o = numpy.tile(o,(len(w),1))
	arrow = numpy.array((o,(o+w)))
	arrow = arrow.transpose((1,0,2)).reshape(2*len(w),3)

	# Sum
	# arrow = numpy.vstack((o,o+numpy.sum(w,axis=0)))

	return arrow