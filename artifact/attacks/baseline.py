# Attack strategy: Pack all identifiers in target set into a single record.
# Corresponding Google Doc section: OPTIMIZATION: Same goal but different method
# This implementation differs from the google doc in that it performs a partial set reconstruction 
# instead of just deciding whether a given identifier is contained in P
from constants import *
import helper as h
import time

# leakage is leakage function, not full MPMC functionality
def BaselineAttack(leakage, T, get_time=time.time):
	elapsed = 0
	start = get_time()
	time_pre_encode = start
	# flatten T into one-record C and keep track of original indices
	r = list(set([id for t in T for id in t]))
	time_post_encode = get_time()

	elapsed += time_post_encode - start
	leakT_prime, leakV = leakage([r])
	start = get_time()

	time_pre_reconstruct = start
	re = leakT_prime[0]
	D = {}

	for i in range(len(re)):
		D[re[i]] = r[i]
	time_post_reconstruct = get_time()

	time_pre_subst = time_post_reconstruct
	recon = h.Substitute(leakV, D)
	time_post_subst = get_time()

	elapsed += time_post_subst - start

	info = {TIME_ALL: elapsed,
			TIME_PREPROCESS: time_post_encode - time_pre_encode,
			TIME_POSTPROCESS: time_post_reconstruct - time_pre_reconstruct,
			TIME_SUBST: time_post_subst - time_pre_subst }

	return recon, info
