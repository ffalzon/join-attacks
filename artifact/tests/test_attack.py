import sys
sys.path.append("../experiments")

from mpmc_functionality import MPMCFunctionality
from attacks.record_enumeration import RecordEnumeration
from math import log2, ceil
from helper import csv_to_2Dlist
import time

N = 1000

experiment = "experiment_data/test_power2/power2_small"
T = csv_to_2Dlist(f"{experiment}_T.csv")
V = csv_to_2Dlist(f"{experiment}_V.csv")


MPMC = MPMCFunctionality(V)

s = 0
for _ in range(N):
	recon, info = RecordEnumeration(MPMC.invoke_C_fast, T, time.time_ns)
	print("# invocations:", MPMC.invocations())
	s += MPMC.invocations()
	MPMC.reset()

print(f"Last reconstruction:")
for r in recon:
	print(r)
theoretical_bound = 1
print(info)
print(f"Avg. Invocations: {s / N}, theoretical upper bound: {theoretical_bound if theoretical_bound is not None else "Not provided"}")
