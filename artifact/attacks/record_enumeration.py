from helper import Substitute, argmin, argmax, IDs
from math import log2, ceil
from random import shuffle, choice
from constants import *
import time

# leakage is leakage function, not full MPMC functionality
def RecordEnumeration(leakage, T, get_time=time.time):
	info = { TIME_ALL: 0 }
	time_pre_encode = get_time()

	encode_len = ceil(log2(len(T)))
	is_power_two = ceil(log2(len(T))) == log2(len(T))

	# id and id can be selected arbitrarily
	id0 = "a"
	id1 = "b"
	id2 = "c"

	E = {}
	T_enc = []
	for i in range(len(T)):
		t = T[i]
		E[i] = t
		s = Encode(i, encode_len, id0, id1)
		s.extend(t)
		T_enc.append(s)

	if is_power_two:
		# Break ties between (id0, ..., id0) and (id1, ..., id1) 
		# with third identifier id2 for last encoding: (id1, ..., id1, id1) -> (id1, ...,id1,id2)
		T_enc[-1][encode_len - 1] = id2

	time_post_encode = get_time()
	time_diff = time_post_encode - time_pre_encode
	info[TIME_ALL] += time_diff
	info[TIME_PREPROCESS] = time_diff

	leakT, leakV = leakage(T_enc)

	time_pre_reconstruction = get_time()

	# There are at most three possible tiebreakers: (0,...,0,1), (1,...1 0) and (1,...,1,2) 
	# and one for which all_same=True: (0,...,0)
	# => after five iterations we surely found a "normal" and "mixed" encoding
	# => With very high probability, this will terminate after the first iteration
	for i in range(min(5, len(leakT))):
		all_same, maybe_tiebreaker, _ = check_encoding_and_decode(leakT[i][:encode_len], "dummy_e1")
		if all_same or maybe_tiebreaker:
			continue
			
		ids = list(set([e for e in leakT[i][:encode_len]]))
		e0_cand = ids[0]
		e1_cand = ids[1]
		break

	indices = {}
	deferred_records = []
	
	for i in range(len(T)):
		encoding = leakT[i][:encode_len]
		all_same, maybe_tiebreaker, possible_indices = check_encoding_and_decode(encoding, e1_candidate=e1_cand)
		
		if all_same:
			if encoding[0] == e0_cand:
				decode_idx = 0
				indices[i] = [0, -1]
			else:
				decode_idx = 1
				indices[i] = [-1, 0]
		elif maybe_tiebreaker and is_power_two:
			deferred_records.append(i)
		else:
			indices[i] = possible_indices

	# At most three records (the three potentially tiebreaking records)
	for i in deferred_records: 
		encoding = leakT[i][:encode_len]
		if encoding[-1] != e0_cand and encoding[-1] != e1_cand:
			idxs = [-1, -1]
			idxs[decode_idx] = len(T) - 1	
		else:
			_, _, idxs = check_encoding_and_decode(encoding, e1_candidate=e1_cand)

		indices[i] = idxs

	D = {}
	for (i, idxs) in indices.items():
		t_prime = leakT[i]
		t_idx = idxs[decode_idx]

		#print("t_idx", t_idx, idxs, leakT[i][:encode_len])
		t = T_enc[t_idx]
		for j in range(len(t)):
			if t_prime[j] in D.keys() and D[t_prime[j]] != t[j]:
				print(f"Collision on elements {D[t_prime[j]]} and {t[j]} with ctxt {t_prime[j]}")
			else:
				D[t_prime[j]] = t[j]

	#print()
	time_post_reconstruction = get_time()
	time_diff = time_post_reconstruction - time_pre_reconstruction
	info[TIME_ALL] += time_diff
	info[TIME_POSTPROCESS] = time_diff
	time_pre_subst = get_time()
	
	recon = Substitute(leakV, D)
	
	time_post_subst = get_time()
	time_diff = time_post_subst - time_pre_subst
	info[TIME_ALL] += time_diff
	info[TIME_SUBST] = time_diff


	return recon, info

# Takes a list of elements and a candidate for the encrypted id1,
# returns two booleans: 
# 	- all_same is true if all identifiers in s are the same 
# 	- maybe_tiepreaker is true if all but last elements are the same and last element is different
# and two indices: 
# 	- idx_true, corresponding to the decoding of s where an occurrence of e1 is interpreted as 1 and everything else as 0
#	- idx_flip, corresponding to the decoding of s where an occurrence of e1 is interpreted as 0 and everything else as 1
def check_encoding_and_decode(s, e1_candidate="not an identifier"):
	id = s[0]
	all_same = True

	idx_true = 0
	idx_flip = 0
	for (i,e) in enumerate(s[:-1]):
		e = s[i]
		if e != id:
			all_same = False
		
		if e == e1_candidate:
			idx_true += 2**(len(s) - i - 1)
		else:
			idx_flip += 2**(len(s) - i - 1)
		
	if s[-1] == e1_candidate:
		idx_true += 1
	else:
		idx_flip += 1

	maybe_tiebreaker = all_same and s[-1] != id
	all_same = all_same and s[-1] == id
	return all_same, maybe_tiebreaker, [idx_true, idx_flip]


def RecordEnumeration_old(F, T, qb=None, get_time=time.time):
	start = get_time()

	# need at least two queries
	if qb is not None and qb < 3:
		return [], {TIME_ALL: get_time() - start,
					ATTACK_SUCCESS: 0}

	info = {}
	encode_len = ceil(log2(len(T)))

	info[TIME_ALL] = get_time() - start
	if qb is not None:
		# Need one query for rest of attack
		id0, id1, is_certain, findID_time = FindIDs(F, T, qb - 1, get_time)
	else:
		id0, id1, is_certain, findID_time = FindIDs(F, T, encode_len + 20, get_time) # encode_len + 3 should suffice
	
	info[TIME_FIND_ID] = findID_time
	info[TIME_ALL] += findID_time
	
	pre_encode_time = get_time()

	E = {}
	T_enc = []
	for (i,t) in enumerate(T):
		E[i] = t
		s = Encode(i, encode_len, id0, id1)
		s.extend(t)
		T_enc.append(s)
	post_encode_time = get_time()

	info[TIME_PREPROCESS] = post_encode_time - pre_encode_time
	info[TIME_ALL] += post_encode_time - pre_encode_time

	_, _, (leakT, leakV) = F(T_enc)

	pre_reconstruction_time = get_time()

	# Encoding of either leakT[0] or leakT[1] must be heterogeneous, if findIDs was successful
	idx_e0, idx_e1 = _extract_ids_from_record(leakT[0][:encode_len], leakV)
	record_idx = 0
	if idx_e0 == -1 or idx_e1 == -1:
		idx_e0, idx_e1 = _extract_ids_from_record(leakT[1][:encode_len], leakV)
		record_idx = 1

		if idx_e0 == -1 or idx_e1 == -1:
			info[TIME_ALL] += get_time() - pre_reconstruction_time
			info[ATTACK_SUCCESS] = 0
			return [], info
	
	# Encoding certainly is heterogeneous from here on, 
	# but id0 and id1 may have been flipped when choosing ids randomly due to limited query budget 
	info[ATTACK_SUCCESS] = 1
	e0 = leakT[record_idx][idx_e0]
	e1 = leakT[record_idx][idx_e1]
	
	D = {}
	retry_swap = False
	for t_prime in leakT:
		idx = Decode_old(t_prime[:encode_len], e1)

		try:
			t = E[idx]
		except KeyError:
			retry_swap = True
			break

		for i in range(len(t_prime[encode_len:])):
			D[t_prime[encode_len + i]] = t[i]
	
	# id retry_swap is true, then id0 and id1 surely have been guessed and mostlikely are reversed,
	# i.e., id0 is in V and id1 is not.
	# Therefore, switch the two and try to recover again
	if not is_certain and retry_swap:
		e0, e1 = e1, e0
		D = {}

		for t_prime in leakT:
			idx = Decode_old(t_prime[:encode_len], e1)

			try:
				t = E[idx]
			except KeyError:
				# this shouldn't happen since encoding should be heterogenous at this point
				print("WARNING: record enumeration reconstruction failed even with heterogenous encoding")
				info[TIME_ALL] += get_time() - pre_reconstruction_time
				info[ATTACK_SUCCESS] = 0
				
				return [], info

			for i in range(len(t_prime[encode_len:])):
				D[t_prime[encode_len + i]] = t[i]

	post_reconstruction_time = get_time()
	info[TIME_POSTPROCESS] = pre_reconstruction_time - post_reconstruction_time

	pre_subst_time = get_time()
	recon = Substitute(leakV, D)
	post_subst_time = get_time()

	info[TIME_SUBST] = post_subst_time - pre_subst_time
	info[TIME_ALL] += post_subst_time - pre_reconstruction_time

	return recon, info


def FindIDs(F, T_in, qb, get_time):
	elapsed = 0
	start = get_time()
	T = T_in

	elapsed += get_time() - start
	_, _, (leakT, leakV) = F(T)
	start = get_time()
	qb -= 1

	if qb == 0:
		id0, id1 = _pick_most_likely(T, leakT, leakV)
		return id0, id1, False, elapsed + get_time() - start

	k = _num_het(leakT, leakV)
	while len(T) > 1 and qb > 0:
		mid = len(T) // 2
		shuffle(T)
		T1 = T[:mid]
		T2 = T[mid:]
		
		elapsed += get_time() - start
		_, _, (leakT, leakV) = F(T1)
		start = get_time()
		qb -= 1

		k1 = _num_het(leakT, leakV)
		k2 = k - k1

		if len(T1) == k1:
			T = [T1[0]]
		elif len(T2) == k2:
			T = [T2[0]]
		elif k1 / len(T1) >= k2 / len(T2):
			T = T1
			k = k1
		else:
			T = T2
			k = k2
	
	# query budget is used up, pick one id from most likely column
	if qb == 0 and len(T) > 0:
		# pick most likely record from T1 since we only have a leakage for T1 available
		id0, id1 = _pick_most_likely(T1, leakT, leakV)
		return id0, id1, False, elapsed + get_time() - start
	
	# len(T) = 1 and therefore len(leakT) = 1
	t = T[0]	

	# no need to run protocol again if T1 was chosen in last iteration
	if T != T1:
		elapsed += get_time() - start
		_, _, (leakT, leakV) = F(T)
		start = get_time()
	
	t_prime = leakT[0]

	# This should never return -1 since we selected T to contain a heterogeneous record
	# However, may fail if original T contains no heterogeneous record
	idx0, idx1 = _extract_ids_from_record(t_prime, leakV)
	if idx0 == -1 or idx1 == -1:
		return t[0], t[1], False, elapsed + get_time() - start
	
	elapsed += get_time() - start

	return t[idx0], t[idx1], True, elapsed

def _extract_ids_from_record(t, leakV):
	ID_leakV = IDs(leakV)
	
	matched_idx = -1
	unmatched_idx = -1
	for i in range(len(t)):
		if t[i] not in ID_leakV:
			unmatched_idx = i
			break

	for i in range(len(t)):
		if t[i] in ID_leakV:
			matched_idx = i
			break
		
	return unmatched_idx, matched_idx

def _pick_most_likely(T, leakT, leakV):
	IDV = IDs(leakV)
	k = len(leakT[0])
	col_matches = [sum(1 if t[i] in IDV else 0 for t in leakT) for i in range(k)]
	min_idx = argmin(col_matches)
	max_idx = argmax(col_matches)
	id0 = choice([t[min_idx] for t in T])
	id1 = choice([t[max_idx] for t in T])

	return id0, id1

# Notation 'H' in writeup
def _num_het(leakT, leakV):
	ID_leakV = IDs(leakV)
	
	ctr = 0
	for t in leakT:
		pos = False
		neg = False
		for e in t:
			if e in ID_leakV:
				pos = True
				if neg:
					ctr += 1
					break
			else:
				neg = True
				if pos:
					ctr += 1
					break
	return ctr


def Encode(i, l, id0, id1):
	fstr = f'{{0:0{l}b}}'
	b = fstr.format(i)
	s = []
	for i in range(l):
		s.append(id0 if b[i] == "0" else id1)
		
	return s

def Decode_old(sequence, e1):
	c = 0
	for i in range(len(sequence)):
		if sequence[i] == e1:
			c += 2**(len(sequence) - i - 1)
	return c

def TheoreticalMaxQueries(n):
	return ceil(log2(n)) + 3