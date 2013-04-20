"""
Find bias and varience using method from Zhan (2006)
"""

import numpy as np

from n_body.fast import N_bodies
from util.rand import plummer_model
from util import dot
from metrics.barycentre import find_barycentre
from metrics.error import F_plummer_r

if __name__ == '__main__':
	N = 2000
	M = 1.
	m = M/N
	Rv = 1.
	N_bodies.G = 1

	dr = 0.01

	# bin values of radius to nearest dr
	bins = np.arange(0,10*Rv+dr,dr)

	times = int(6e4/N)
	f_true = F_plummer_r(Rv,M)

	print '#','plummer','N',N,'M',M,'R',Rv,'dr',dr,'times',times
	print '#','softening','radius','true acceleration','radial acceleration','bias','variance'

	# do for different values of softening
	for s in np.arange(0,1+dr,dr):
		binned_a = [[] for _ in range(len(bins))]
		binned_x = [[] for _ in range(len(bins))]

		for _ in xrange(times):
			x,v = plummer_model(Rv,N)
			n = N_bodies(m*np.ones(N),x,v,dt=1,softening=s)
			n.x -= find_barycentre(n)
			n.find_r()
			n.find_a()

			# bin according to radius
			ind = np.digitize(np.sqrt(dot(n.x,n.x)),bins)
			for i,bin in enumerate(ind):
				binned_a[bin-1].append(n.a[i])
				binned_x[bin-1].append(n.x[i])

		for i,r in enumerate(bins):
			if not binned_a[i] and not binned_x[i]: continue
			a = np.array(binned_a[i])
			x = np.array(binned_x[i])
			# true = -f_true(0.5*(r+dr))
			true = -f_true(r)
			# radial acceleration
			# r_unit = -x/dot(x,x)[:,np.newaxis]
			# a_r = dot(a,r_unit)
			a_r = np.sqrt(dot(a,a))
			a_r = np.mean(a_r)
			# a_2 = np.mean(a,axis=0)
			# a_2 = dot(a_2,a_2)
			bias = a_r - true
			# variance = np.mean(dot(a,a)) - a_2
			variance = np.var(a)

			print s,r,true,a_r,bias,variance
