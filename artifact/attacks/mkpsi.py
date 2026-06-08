from queue import PriorityQueue
from random import shuffle
from time import time
from helper import IDs
from constants import *
import copy

# Prioritizes maximizing the fraction of identifiers of T with determined membership status
def PriorityTotal(c, n):
	s = sum([max(x, n - x) for x in c])
	return s / (len(c) * n)

# Prioritizes maximizing len(pos)
def PriorityPos(c, n):
	s = sum([x for x in c])
	return s / (len(c) * n)

# Prioritizes maximizing len(neg)
def PriorityNeg(c, n):
	s = sum([n - x for x in c])
	return s / (len(c) * n)

# leakage is leakage function, not full MKPM functionality
def MK_PSI(leakage, T, p=PriorityTotal, qb=None, get_time=time):
	T = copy.deepcopy(T) 
	shuffle(T)

	elapsed = 0
	start = get_time()
	I = len(IDs(T))
	pos = set()
	neg = set()
	
	elapsed += get_time() - start
	res = leakage(T)
	start = get_time()
	if res is None:
		return pos, neg, {TIME_ALL: elapsed + get_time() - start}
	leakT, leakV = res

	q = PriorityQueue()
	q.put((1, colCA(leakT, leakV), T))

	while not q.empty():
		(_, cX, X) = q.get()
		while not all([(c == 0 or c == len(X)) for c in cX]) and len(neg) + len(pos) < I:
			mid = len(X) // 2
			L = X[:mid]
			R = X[mid:]
			
			elapsed += get_time() - start
			res = leakage(L)
			start = get_time()
			if res is None:
				incorporate_singletons(q, pos, neg)
				return pos, neg, { TIME_ALL: elapsed + get_time() - start }
			leakTL, leakV = res

			cL = colCA(leakTL, leakV)
			cR = col_diff(cX, cL)

			pR = p(cR, len(L))
			pL = p(cL, len(R))
			
			if pR > pL:
				q.put((pL, cL, L))
				X = R
				cX = cR
			else:
				q.put((pR, cR, R))
				X = L
				cX = cL

		for i in range(len(T[0])):
			if cX[i] == 0:
				neg.update([x[i] for x in X])
			else:
				pos.update([x[i] for x in X])
		
		if  len(neg) + len(pos) >= I:
			break
			
	return pos, neg, {TIME_ALL: elapsed + get_time() - start }

def colCA(leakT, leakV):
	IV = set([id for v in leakV for id in v])
	c = [sum([1 if t[i] in IV else 0 for t in leakT]) for i in range(len(leakT[0]))]
	return c

def col_diff(c1, c2):
	return [x - y for (x,y) in zip(c1, c2)]

# adds all remaining single sets in queue to pos / neg, since no protocol invocation is necessary for that.
# For PriorityTotal, this shouldn't make a large difference, since priority of these sets is 1
def incorporate_singletons(queue : PriorityQueue, pos : set, neg: set):
	while not queue.empty():
		(_, cX, X) = queue.get()
		if len(X) != 1:
			continue

		for (i, c) in enumerate(cX):
			if c > 0:
				pos.add(X[0][i])
			else:
				neg.add(X[0][i])


