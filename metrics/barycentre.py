from numpy import sum,newaxis

def find_barycentre(n):
	"""
	Find the position of the barycentre
	of all the bodies in an N body simulation.
	
	Takes an N_bodies instance,
	Returns a position vector.
	"""
	return sum(n.x*n.m[:,newaxis],axis=0)/sum(n.m)

def find_barycentre_v(n):
	"""
	Find the velocity of the barycentre

	Takes an N_bodies instance,
	Returns a velocity vector.
	"""
	return sum(n.v*n.m[:,newaxis],axis=0)/sum(n.m)
