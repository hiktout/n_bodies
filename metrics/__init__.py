def dot(a,b):
	assert len(a) == len(b)
	return a[:,0]*b[:,0] + a[:,1]*b[:,1] + a[:,2]*b[:,2]
