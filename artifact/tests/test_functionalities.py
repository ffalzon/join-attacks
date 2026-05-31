# little script to test whether the two implemented functionalities (naive and optimized) yield identical outputs
from mpmc_functionality import MPMCFunctionality
from attacks.baseline import BaselineAttack
from math import log2, ceil
from constants import *
import helper
import random
import time

def cmp_1D_lists(l1, l2):
	if len(l1) != len(l2):
		return False

	for i in range(len(l1)):
		if l1[i] != l2[i]:
			return False

	return True

def cmp_2D_lists(l1, l2):
	if len(l1) != len(l2):
		return False

	for i in range(len(l1)):
		if not cmp_1D_lists(l1[i], l2[i]):
			return False
	
	return True

def cmp_dicts(d1, d2):
	if len(d1.keys()) != len(d2.keys()):
		return False

	for k in d1.keys():
		# original T is not changed, comparing pointers should be fine
		if d1[k] != d2[k]:
			return False
		
	return True

def cmp_collection(c1, c2):
	if len(c1) != len(c2):
		return False

	for v in c1:
		if v not in c2:
			return False
		
	return True

data_dir ="data"
experiments = helper.get_experiments(data_dir)

seeds = [0xF00BAA, 0xCAFEBABE, 0xDEADBEEF, 0XF0CCAC1A, 0xABBACAFE]

for experiment in experiments:	
	print(f"Experiment: {experiment[EXP_NAME]}")
	T = helper.csv_to_2Dlist(experiment[EXP_T_PATH])
	V = helper.csv_to_2Dlist(experiment[EXP_V_PATH])

	MPMC = MPMCFunctionality(V)
	for seed in seeds:
		print("Invkoing naive functionality")
		random.seed(seed)

		start = time.time()
		UID1, MC1, (leakT1, leakV1) = MPMC.invoke_C(T)
		print(f"time: {time.time() - start}")

		print("Invoking fast functionality")
		random.seed(seed)
		start = time.time()
		UID2, MC2, (leakT2, leakV2) = MPMC.invoke_C_fast(T)
		print(f"time: {time.time() - start}")

		cmp_UIDs = cmp_collection(UID1, UID2)
		cmp_MCs = cmp_dicts(MC1, MC2)
		cmp_leakTs = cmp_2D_lists(leakT1, leakT2)
		cmp_leakVs = cmp_2D_lists(leakV1, leakV2)
		ok = cmp_UIDs and cmp_MCs and cmp_leakTs and cmp_leakVs

		print(f"Comparison: {"ok" if ok else "failed"}")
		if not ok:
			print(f"Experiment: {experiment["experiment"]}")
			print(f"Seed: {seed}")
			print(f"UIDs: {cmp_collection(UID1, UID2)}")
			print(f"MCs:  {cmp_dicts(MC1, MC2)}")
			print(f"leakT: {cmp_2D_lists(leakT1, leakT2)}")
			print(f"leakV: {cmp_2D_lists(leakV1, leakV2)}")
			print()
			
			print("UIDs")
			print(UID1)
			print(UID2)

			print("MCs")
			print(MC1)
			print(MC2)

			print("leakT")
			print(leakT1)
			print(leakT2)

			print("leakV")
			print(leakV1)
			print(leakV2)
		print()
		print()

