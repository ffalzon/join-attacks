from helper import Substitute
from string import ascii_letters, digits
from random import choices
from constants import *
import time

# leakage is leakage function, not full MPMC functionality
def Snake(leakage, T, get_time=time.time):
	info = {TIME_ALL: 0}
	time_pre_encode = get_time()

	k = -1
	lmax = max([len(t) for t in T])
	for i in range(lmax):
		if len(set([t[i] for t in T])) == len(T):
			k = i
			break
	
	if k >= 0:
		# Unique approach
		T_prime = EncodeUnique(T, k)
		time_post_encode = get_time()

		info[TIME_ALL] += time_post_encode - time_pre_encode
		info[TIME_PREPROCESS] = time_post_encode - time_pre_encode
		leakT_prime, leakV = leakage(T_prime)
		
		time_pre_recover = get_time()
		E_enc = RecoverUnique(leakT_prime, k)
	else:
		# General approach
		T_prime = EncodeGeneral(T)
		time_post_encode = get_time()

		info[TIME_ALL] += time_post_encode - time_pre_encode
		info[TIME_PREPROCESS] = time_post_encode - time_pre_encode
		leakT_prime, leakV = leakage(T_prime)
		
		time_pre_recover = get_time()
		E_enc = RecoverGeneral(leakT_prime)


	D = {}
	for i in range(len(T)):
		t = T[i]
		t_prime = E_enc[i]
		
		assert (len(t) == len(t_prime))

		for j in range(len(t)):
			D[t_prime[j]] = t[j]
	
	time_post_recover = get_time()
	time_pre_subst = time_post_recover
	info[TIME_POSTPROCESS] = time_post_recover - time_pre_recover

	recon = Substitute(leakV, D)

	time_post_subst = get_time()

	info[TIME_SUBST] = time_post_subst - time_pre_subst
	info[TIME_ALL] += time_post_subst - time_pre_recover
	
	return recon, info

def EncodeUnique(T, k):
	E = {}
	for i in range(len(T) - 1):
		id = T[i+1][k]
		T[i].append(id)
	
	# assume 123 is not a valid identifier, for simplicity
	T[-1].append("123")
	return T

def RecoverUnique(leakT, k):
	LL = {}
	loc = {}
	links = set()
	start = -1
	for i in range(len(leakT)):
		loc[leakT[i][k]] = i
		links.add(leakT[i][-1])

	for i in range(len(leakT)):
		link = leakT[i][-1]
		if link in loc.keys():
			LL[i] = loc[link]

		if leakT[i][k] not in links:
			start = i

	E = [None] * len(leakT)
	cur = start
	i = 0
	while True:
		E[i] = leakT[cur]
		i += 1

		if leakT[cur][-1] not in loc.keys():
			break

		cur = LL[cur]

	return E

def EncodeGeneral(T):
	id_len = 20 # for larger sets, we may have to choose this based on len(T)
	
	E = {}
	cur = get_id(id_len)
	links = set([cur])

	T[0] = ["0"] + T[0] + [cur]
	for i in range(1,len(T)):
		cur_new = get_id(id_len)
		while cur_new in links:
			cur_new = get_id(id_len)
		links.add(cur_new)

		T[i] = [cur] + T[i] + [cur_new]
		
		cur = cur_new
		E[i] = T[i]
	return T
	
def get_id(length):
	return ''.join(choices(ascii_letters + digits, k=length))

def RecoverGeneral(leakT):
	return RecoverUnique(leakT, 0)