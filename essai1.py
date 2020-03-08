from libHamming import nchoosek, weight_int
from math import ceil, floor, fsum, log2
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

p = 0.1
q = 1-p
H = -p*log2(p) -q*log2(q)
n = 1024
N = 2**n
if False:
	wl = [weight_int(m) for m in range(N)]
	pl = sorted((p**w*q**(n-w) for w in wl), reverse=True)
	fig = plt.figure()
	plt.plot(pl)

ckn = [nchoosek(n,w) for w in range(n+1)]
pl = [p**w*q**(n-w) for w in range(n+1)]
spectre = [x*y for x,y in zip(ckn,pl)]

fig = plt.figure()
plt.plot(spectre)

epsilon = 0.05
pcumul = 0.9
for ln in range(0,11): ## 12 : overflow sur int->float(x) dans x*y
	n = 2**ln
	# print(n)
	ckn = [nchoosek(n,w) for w in range(n+1)]
	assert sum(ckn) == 2**n
	pl = [p**w*q**(n-w) for w in range(n+1)]
	spectre = [x*y for x,y in zip(ckn,pl)]
	assert abs(fsum(spectre) - 1) < 1e-6
	## verif loi des grands nombres
	assert 0 < epsilon < p
	kr1 = ceil((p-epsilon)*n); kr2 = floor((p+epsilon)*n)
	foo = fsum(spectre[w] for w in range(kr1,kr2+1))
	print('{} : {}'.format(n,foo))
	## verif hamming
	xl = sorted(enumerate(pl),key = itemgetter(1), reverse=True)
	cumul_of_p = cumul_of_nb = 0
	for i,p1 in xl:
		old_cumul_of_nb = cumul_of_nb
		cumul_of_nb += ckn[i]
		old_cumul_of_p = cumul_of_p
		cumul_of_p += p1 * ckn[i]
		if cumul_of_p > pcumul:
			break
	delta_p = pcumul - old_cumul_of_p
	assert delta_p < p1 * ckn[i]
	delta_nb = delta_p/p1
	nb = old_cumul_of_nb + delta_nb
	assert nb <= cumul_of_nb
	print('{} : {}'.format(n,nb/2**n))
	
###