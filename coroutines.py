def coroutine(func):
	"""coroutine decorator"""
	def start(*args,**kwargs):
		cr = func(*args,**kwargs)
		cr.next()
		return cr
	return start

@coroutine
def printer():
	import sys

	try:
		while 1:
			p = []
			while 1:
				buf = (yield)
				if buf == None: break
				p.extend(buf)

			sys.stderr.write('\r')
			sys.stderr.write(' '.join(p))
			sys.stderr.flush()
	except GeneratorExit:
		sys.stderr.write('\r')
		sys.stderr.write('\n')
		sys.stderr.flush()

@coroutine
def progress_bar():
	import sys

	def print_progress(p):
		sys.stderr.write('\r')
		sys.stderr.write("[%-50s] %d%%" % ('='*(p/2), p))
		sys.stderr.flush()

	try:
		old_p = None
		while True:
			p = (yield)
			if p == old_p:
				continue
			print_progress(p)
			old_p = p
	except GeneratorExit:
		sys.stderr.write('\r')
		sys.stderr.write('\n')
		sys.stderr.flush()

@coroutine
def two_lines(target1,target2):
	import sys

	try:
		while 1:
			target1.send((yield))

			sys.stderr.write("\n")
			sys.stderr.flush()

			while 1:
				new = (yield)
				target2.send(new)
				if new == None: break

			sys.stderr.write("\033[F")
	except GeneratorExit:
		target1.close()
		target2.close()

@coroutine
def tee(target,f):
	"""
	Save output	to a file
	"""
	with open(f) as f:
		while 1:
			p = []
			while 1:
				buf = (yield)
				target.send(buf)
				if buf == None: break
				p.extend(buf)
			f.write(' '.join(p)+'\n')

@coroutine
def data_buffer(target,bufsize):
	"""
	Caches values in a fixed length buffer
	until it is full or None is sent,
	whereupon it sends on
	"""
	try:
		buf = bufsize*[None]
		while 1:
			for i in xrange(bufsize):
				buf[i] = (yield)
				if buf[i] == None:
					target.send(buf[:i])
					break
			else:
				target.send(buf)
	except GeneratorExit:
		target.close()

@coroutine
def dedup(target,**tol):
	"""
	Skip values in a sequence
	that are too similar. Values
	can be tuples, in which case
	all elements of the tuple have
	to be similar, a la numpy.allclose().
	"""
	import numpy
	
	old = numpy.NaN
	while 1:
		new = (yield)
		if new == None:
			target.send(None)
			continue
		if numpy.allclose(new,old,**tol):
			continue
		target.send(new)
		old = new