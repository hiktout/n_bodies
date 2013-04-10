import numpy

def read_file(paths):
	"""
	Read and process files that contain
	the initial variables for an N bodies simulation.

	Reads the masses, positions, velocities,
	name and plotting style,
	in the order specified by cols.

	Takes a list of paths
	Returns m a numpy array
			x a numpy array
			v a numpy array
			name a list
			style a list
	"""
	cols = ('m','x','v','name','style')

	# read lines into a dictionary as per cols
	files = (open(path) for path in paths)
	lines = [line.split() for f in files for line in f]
	data = (dict(zip(cols,line)) for line in lines)
	
	def field_map(dictseq,name,func):
		# From dabeaz.com/generators-uk/
		for d in dictseq:
			d[name] = func(d[name])
			yield d
	read_vector = lambda l: map(float,l.split(','))
	
	# do some data conversions
	data = field_map(data,'m',float)
	data = field_map(data,'x',read_vector)
	data = field_map(data,'v',read_vector)
	
	# append to lists since
	# numpy.append is a Bad Idea
	out = [[] for _ in range(len(cols))]
	out = dict(zip(cols,out))
	for d in data:
		for k in d:
			out[k].append(d[k])

	out['m'] = numpy.array(out['m'])
	out['x'] = numpy.array(out['x'])
	out['v'] = numpy.array(out['v'])

	# return lists in order of
	# the column specification	
	return [out[k] for k in cols]