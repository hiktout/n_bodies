import numpy

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
	bins = 50
	x = numpy.histogram(r[:,0],bins=bins)
	y = numpy.histogram(r[:,1],bins=bins)
	z = numpy.histogram(r[:,2],bins=bins)

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
