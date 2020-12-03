import math

def chunks(l, n_chunks):
	n_in_chunk = math.ceil(float(len(l))/float(n_chunks))
	for i in range(0,len(l),n_in_chunk):
		yield l[i:i+n_in_chunk]

