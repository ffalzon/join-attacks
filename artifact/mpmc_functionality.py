import csv
import copy
import random 
import hashlib
from secrets import token_bytes
import helper as h

# Implements the extended functionality of Meta's MK-PrivateID protocol 
# which includes the protocol leakage. The attacks that do not utilize 
# the leakage simply ignore the corresponding portion of the output.
class MPMCFunctionality:

	def __init__(self, P=None, query_budget=None):
		self._invocations = 0
		self._P = P
		self._query_budget = query_budget

	def set_P(self, P):
		self._P = P
		assert len(self._P) > 0

	def set_P_from_csv(self, file_path, delimiter=";"):
		self._P = h.csv_to_2Dlist(file_path, delimiter)
		assert len(self._P) > 0

	def set_query_budget(self, query_budget):
		self._query_budget = query_budget

	def invoke_C(self, C_in):
		assert(self._P is not None)
		if self._query_budget is not None and self._invocations >= self._query_budget:
			return None

		self._invocations += 1

		C = copy.deepcopy(C_in) 
		P = copy.deepcopy(self._P)
		random.shuffle(C)
		random.shuffle(P)
		for i in range(len(P)):
			random.shuffle(P[i])
		
		MC = {}
		#MP = {} # MP is not needed right now since we only simulate the functionality for party C

		UID_sampler = h.Sampler(allowRepetitions=False)
		
		matched = [False] * (len(C) + len(P))
		lmax = max([len(C[i]) for i in range(len(C))])
		for j in range(lmax):
			for i in range(len(P)):
				if matched[len(C)+i]:
					continue

				for k in range(len(C)):
					if len(C[k]) <= j or matched[k]:
						continue
					
					break_outer = False
					for l in range(len(P[i])):						
						if C[k][j] == P[i][l]:
							matched[k] = True
							matched[len(C) + i] = True
							
							r = UID_sampler.sample()
							MC[r] = C[k]
							# MP[r] = P[i]

							break_outer = True
							break
					if break_outer:
						break
		
		# Generate UIDs for unmatched records of C and P
		for i in range(len(C)):
			if not matched[i]:
				r = UID_sampler.sample()
				MC[r] = C[i]
				# MP[r] = None

		for i in range(len(P)):
			if not matched[len(C) + i]:
				r = UID_sampler.sample()
				MC[r] = None
				# MP[r] = P[i]
				
		# Protocol Leakage
		f = h.RandomFunction(injective=True)
		leakC = [[f.eval(id) for id in c] for c in C]
		leakP = [[f.eval(id) for id in p] for p in P]

		# UIDs is just the set of keys of MC since MC: UID -> C + { None }
		return MC.keys(), MC, (leakC, leakP)
	
	def leakage(self, C):
		assert(self._P is not None)
		if self._query_budget is not None and self._invocations >= self._query_budget:
			return None
		
		self._invocations += 1

		f = h.RandomFunction(injective=True)
		leakC = [[f.eval(id) for id in c] for c in C]
		leakP = [[f.eval(id) for id in p] for p in self._P]
		random.shuffle(leakC)
		random.shuffle(leakP)
		return leakC, leakP

	def leakage_sha256(self, C):
		assert(self._P is not None)
		if self._query_budget is not None and self._invocations >= self._query_budget:
			return None
		
		self._invocations += 1

		r = token_bytes(10)
		f = lambda x: hashlib.sha256(r + x.encode()).digest()
		leakC = [[f(id) for id in c] for c in C]
		leakP = [[f(id) for id in p] for p in self._P]
		random.shuffle(leakC)
		random.shuffle(leakP)
		return leakC, leakP

	def invoke_C_fast(self, C_in):
		assert(self._P is not None)
		if self._query_budget is not None and self._invocations >= self._query_budget:
			return None

		self._invocations += 1

		C = copy.deepcopy(C_in) 
		P = copy.deepcopy(self._P)
		random.shuffle(C)
		random.shuffle(P)
		for i in range(len(P)):
			random.shuffle(P[i])
		
		MC = {}
		#MP = {} # MP is not needed right now since we only simulate the functionality for party C

		UID_sampler = h.Sampler(allowRepetitions=False)
		
		matched = [False] * (len(C) + len(P))
		lmax = max([len(C[i]) for i in range(len(C))])

		col_ID_C = [{} for _ in range(lmax)]
		for i in range(len(C)):
			for j in range(len(C[i])):
				id = C[i][j]
				if id not in col_ID_C[j]:
					col_ID_C[j][id] = [i]
				else:
					col_ID_C[j][id].append(i)
			
		for j in range(lmax):
			for i in range(len(P)):
				if matched[len(C) + i]:
					continue
				
				I = set()
				for l in range(len(P[i])):
					if P[i][l] in col_ID_C[j]:
						I.update(col_ID_C[j][P[i][l]])
				if len(I) > 0:
					k = min(I)
					matched[k] = True
					matched[len(C) + i] = True

					r = UID_sampler.sample()
					MC[r] = C[k]

					# remove C[i]
					for col in range(len(C[k])):
						try: 
							col_ID_C[col][C[k][col]].remove(k)
						except:
							print("Remove error")
							pass

		
		# Generate UIDs for unmatched records of C and P
		for i in range(len(C)):
			if not matched[i]:
				r = UID_sampler.sample()
				MC[r] = C[i]
				# MP[r] = None

		for i in range(len(P)):
			if not matched[len(C) + i]:
				r = UID_sampler.sample()
				MC[r] = None
				# MP[r] = P[i]
				
		# Protocol Leakage
		f = h.RandomFunction(injective=True)
		leakC = [[f.eval(id) for id in c] for c in C]
		leakP = [[f.eval(id) for id in p] for p in P]

		# UIDs is just the set of keys of MC since MC: UID -> C + { None }
		return MC.keys(), MC, (leakC, leakP)

	def invocations(self):
		return self._invocations
	
	def reset(self):
		self._invocations = 0
