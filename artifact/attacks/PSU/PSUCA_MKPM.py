from collections.abc import Callable
from queue import PriorityQueue
from random import shuffle
from time import time_ns
from constants import *

def prio_PSI_pos(k : int, n_prime : int, m : int) -> float:
	return k/n_prime

def prio_PSI_neg(k : int, n_prime : int, m : int) -> float:
	return 1 - k/n_prime

def prio_PSI_tot(k : int, n_prime : int, m : int) -> float:
	return max(k, n_prime - k) / n_prime

def PSU_CA_MKPM_Intersection(F, T, priority=prio_PSI_tot, get_time=time_ns):
	if len(T) == 0:
		return [], [], {TIME_ALL: 0}
	
	elapsed = 0
	start = get_time()

	shuffle(T)
	mid = len(T) // 2
	X1 = T[:mid]
	X2 = T[mid:]
	elapsed += get_time() - start
	
	UID, _, _ = F(T)
	UID1, _, _ = F(X1)
	UID2, _, _ = F(X2)
	start = get_time()

	z = len(UID)
	z1 = len(UID1)
	z2 = len(UID2)

	m = z2 - (z - z1)	
	
	if len(T) == 1: # i.e. len(X1) == 0
		info = {TIME_ALL : elapsed + get_time() - start}
		if z2 == m:
			return [X2[0]], [], info
		else:
			return [], [X2[0]], info
	
	k1 = len(X1) + m - z1
	k2 = len(X2) + m - z2

	pos = []
	neg = []

	q = PriorityQueue(2 * len(T))
	q.put((priority(k1, len(X1), m), X1, k1))
	q.put((priority(k2, len(X2), m), X2, k2))

	while not q.empty():
		(_, X_cur, k_cur) =  q.get()
		while 0 < k_cur < len(X_cur):
			mid = len(X_cur) // 2
			left = X_cur[:mid]
			right = X_cur[mid:]

			elapsed += get_time() - start
			res = F(left)
			start = get_time()
			
			if res == None:
				process_remainder(q, pos, neg, m)
				elapsed += get_time() - start
				return pos, neg, {TIME_ALL: elapsed}
			
			UIDL, _, _ = res
			zL = len(UIDL)

			kL = len(left) + m - zL
			kR = k_cur - kL

			#zR = k_cur - zL + m
			
			pL = priority(kL, len(left), m)
			pR = priority(kR, len(right), m)

			if pL > pR:
				X_cur, k_cur = left, kL
				q.put((pR, right, kR))
			else:
				X_cur, k_cur = right, kR
				q.put((pL, left, kL))

		if k_cur == len(X_cur):
			pos += X_cur
		else:
			neg += X_cur

	info = {TIME_ALL: elapsed + get_time() - start}
	return pos, neg, info
		
def process_remainder(pq : PriorityQueue, pos : list, neg : list, m : int):
	while not pq.empty():
		(_, X, z) = pq.get()
		if z == m:
			pos += X
		elif z == m + len(X):
			neg += X
		

	