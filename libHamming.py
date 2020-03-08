#! /usr/bin/python

from __future__ import division, print_function

from functools import reduce

def reduce2(function, iterable1, iterable2, initializer):
	it1 = iter(iterable1)
	it2 = iter(iterable2)
	value = initializer
	for elem1 in it1:
		value = function(value, elem1, next(it2))
	return value

import array, random

print('HAMMING start')

def _w32(i):
	j = i & 0xFFFFFFFF
	return _w16(j&0xFFFF)+_w16(j>>16)

def _w16(i):
	j = i & 0xFFFF
	return _w8(j&0xFF)+_w8(j>>8)

def _w8(i):
	j = i & 0xFF
	return _w4(j&0xF)+_w4(j>>4)

def _w4(i):
	j = i & 0xF
	return _w2(j&0x3)+_w2(j>>2)

def _w2(i):
	j = i & 0x3
	return (j&1)+(j>>1)

_weight_nbb = 16
#
_weight_len = 2**_weight_nbb
_weight_msk = _weight_len-1
_weight = array.array('B',[0 for i in range(_weight_len)])
_weight[0]=0
_weight[1]=1
for i in range(2,_weight_len):
	_weight[i] = _weight[i>>1]+(i&1)

def weight_int(i):
	"""
	"""
	w = _weight[i&_weight_msk]
	if i>=_weight_len:
		w = w+weight_int(i>>_weight_nbb)
	return w
	
def weight_vect(v):
	"""
	compte le nombre d'elements non nuls
	"""
	w = reduce(lambda value,elem: value+1 if elem else value, v, 0)
	return w

def weight(cw):
	"""
	"""
	if type(cw) is int:
		return weight_int(cw)
	else:
		return weight_vect(cw)

def dist_int(i1,i2):
	"""
	"""
	return weight_int(i1^i2)

def dist_vect(v1,v2):
	"""
	"""
	return reduce2(lambda value,elem1,elem2: value+1 if elem1!=elem2 else value, v1,v2,0)

def dist(cw1,cw2):
	"""
	"""
	if type(cw1) is int:
		return dist_int(cw1,cw2)
	else:
		return dist_vect(cw1,cw2)
	
def code_dist(c):
	"""
	c est une liste de mots (int or vect)
	"""
	dc = 1000000;
	for i in range(1,len(c)):
		for j in range(0,i):
			dij = dist(c[i],c[j])
			if dij<dc:
				dc = dij
	return dc

def int_to_01vect(i,n):
	"""
	r[i] contient le bit de poids i
	"""
	r = [0 for j in range(n)]
	ind = 0
	while i:
		r[ind] = i&1
		i = i>>1
		ind = ind+1
	return r

def int_from_01vect(v01):
	"""
	"""
	r = 0
	for b in reversed(v01):
		r = 2*r+b
	return r

def hard_decode_int(w,il):
	"""
	'il' est une liste d'entiers 
	"""
	w01 = [(1 if wi>=0.0 else 0) for wi in w]
	w_int = int_from_01vect(w01)
	dmin = 1000000
	imin = -1
	for i in il:
		d = dist_int(w_int,i)
		if d < dmin:
			dmin = d
			imin = i
	return imin

def hard_decode(cw,c):
	"""
	cw est un mot (int ou vect)
	c est un code, donc un vecteur de mots
	"""
	return hard_decode_int(cw, c)

def find_all_max(v):
	"""
	"""
	m = max(v)
	return [i for (i,x) in enumerate(v) if x==m]

def rand_code(N,K,nbes=1): # N = 2**n
	"""
	"""
	if nbes<=1:
		return [random.randrange(0,N) for i in range(0,K)]
	r = [0 for i in range(K)]
	for i in range(1,K):
		cand_l = [random.randrange(0,N) for i in range(0,nbes)]
		d_l = [min([dist(cand, rj) for rj in r[0:i]]) for cand in cand_l]
		

def next_code(N,K,d,cc): # cc=current_code
	"""
	"""
	assert len(cc)<=K
	for x in range(cc[-1]+1,N):
		is_ok = True
		for i in range(0,len(cc)-2):
			if weight(x,cc[i])<d:
				is_ok = False
				break
		if is_ok:
			cc[-1] = x
			return
	## bla

def noise(s,l):
	"""
	s = sigma
	"""
	return [random.normalvariate(0,s) for i in range(l)]

def nchoosek(n,k):
	"""
	si k est une liste, renvoie la somme des nchoosek
	"""
	if type(k) is list:
		return sum([nchoosek(n,k1) for k1 in k])
	else:
		assert type(k) is int
		assert n>=k>=0
		if k==n or k==0:
			return 1
		if n<k+k:
			k = n-k
		## k est maintenant petit
		## C 5 2 = 5*4/2*1
		r = n # /1
		for d in range(2,k+1):
			n = n-1
			r = r*n//d
		assert type(r) is int
		return r

import math

def log2_nchoosek(n,k):
	"""
	si k est une liste, renvoie la somme des nchoosek
	"""
	if type(k) is list:
		assert False # return sum([nchoosek(n,k1) for k1 in k])
	else:
		assert type(k) is int
		assert n>=k>=0
		if k==n or k==0:
			return 0 # 1
		if n<k+k:
			k = n-k
		## k est maintenant petit
		## C 5 2 = 5*4/2*1
		r = math.log2(n) # /1
		for d in range(2,k+1):
			n = n-1
			r += math.log2(n) - math.log2(d) # = r*n//d
		# assert type(r) is int
		return r

import unittest

class Test(unittest.TestCase):
	
	@staticmethod
	def true_nchoosek(n,k):
		r = math.factorial(n)/math.factorial(k)/math.factorial(n-k)
		r = round(r)
		return r
	
	def test_nchoosek(self):
		### on genere un code
		n = 10
		for k in range(n+1):
			true_nchoosek = round(Test.true_nchoosek(n,k))
			assert type(true_nchoosek) is int
			comp_nchoosek = nchoosek(n,k)
			self.assertEqual(comp_nchoosek, true_nchoosek)
		
	def test_log2_nchoosek(self):
		### on genere un code
		n = 10
		for k in range(n+1):
			true_nchoosek = round(Test.true_nchoosek(n,k))
			assert type(true_nchoosek) is int
			comp_log2_nchoosek = log2_nchoosek(n,k)
			self.assertAlmostEqual(2**comp_log2_nchoosek, true_nchoosek, delta=1e-9)
	
if __name__ == '__main__':
	unittest.main()
	
print('HAMMING end')
