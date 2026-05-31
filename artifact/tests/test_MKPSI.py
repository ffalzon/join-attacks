from helper import csv_to_2Dlist
from mpmc_functionality import MPMCFunctionality
from attacks.mkpsi import MK_PSI, PriorityTotal 
from math import ceil

def sanitycheck(s1, s2, T):
	if len(s1.intersection(s2)) > 0:
		print("Sets are not disjoint!")
		print(f"s1: {s1}")
		print(f"s2: {s2}")
		print(f"Intersection: {s1.intersection(s2)}")
	
	ids = set([id for t in T for id in t])
	if len(s1) + len(s2) != len(ids):
		print("Not all identifiers determined")
		print(f"|s1|: {len(s1)}, |s2|: {len(s2)}, |I_T|: {len(ids)}")
	
N = 100

experiment = "small_320"
T = csv_to_2Dlist(f"data/{experiment}_T.csv")
V = csv_to_2Dlist(f"data/{experiment}_V.csv")

MPMC = MPMCFunctionality(V)

s = 0
for _ in range(N):
	pos, neg = MK_PSI(MPMC.invoke_C_fast, PriorityTotal, T)
	s += MPMC.invocations()
	MPMC.reset()
	sanitycheck(pos, neg, T)

#print(f"Last reconstruction: {recon}")
theoretical_bound = len(T)
print(f"Avg. Invocations: {s / N}, theoretical upper bound: {theoretical_bound if theoretical_bound is not None else "Not provided"}")