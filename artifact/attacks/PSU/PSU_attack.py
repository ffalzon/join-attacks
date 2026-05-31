from collections.abc import Callable
from time import time_ns

def PSU_Diff(PSU: Callable[[set | list], set], T: set, get_time=time_ns) -> set:
	start = get_time()
	
	T_list = list(T)
	mid = len(T) // 2
	T1 = T_list[:mid]
	T2 = T_list[mid:]

	elapsed = get_time() - start
	Z1 = PSU(T1) # Z1 = T1 \cup Y
	Z2 = PSU(T2) # Z1 = T2 \cup Y
	
	start = get_time()
	Y = Z1.intersection(Z2)
	I = T.intersection(Y)
	elapsed += get_time() - start
	return I, elapsed
