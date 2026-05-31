from mpmc_functionality import MPMCFunctionality
from attacks.record_enumeration import RecordEnumeration
from math import floor, ceil, log2
from os.path import join, exists
from os import makedirs
from csv import DictWriter
from constants import *

import helper
import time


def MeasureRecEnumSuccProb(data_path, out_path, repetitions=100, query_budget_increment_fraction=0.05, time_func=time.time):
	#measurements = []

	experiments = helper.get_experiments(data_path)
	for e in experiments:
		print(f"experiment: {e[EXP_NAME]}")

		T = helper.csv_to_2Dlist(e[EXP_T_PATH])
		V = helper.csv_to_2Dlist(e[EXP_V_PATH])

		MPMC = MPMCFunctionality(V)
		
		theoretical_max_queries = ceil(log2(len(T))) + 3
		inc = max(1, floor(theoretical_max_queries * query_budget_increment_fraction))

		for qb in range(inc, theoretical_max_queries + inc, inc):
			print(f"query budget: {qb}")
			MPMC.set_query_budget(qb)

			data = {TIME_ALL: [],
					TIME_FIND_ID: [],
					TIME_PREPROCESS: [],
					TIME_POSTPROCESS: [],
					TIME_SUBST: [],
					ATTACK_SUCCESS: [],
					NUM_QUERIES: [] }
			
			for _ in range(repetitions):
				MPMC.reset()
				_, info = RecordEnumeration(MPMC.invoke_C_fast, T, qb=qb, get_time=time_func)
				
				info[NUM_QUERIES] = MPMC.invocations()
				helper.update_dict(data, info)
			

			m = {	**e,
					ATTACK_NAME: RECENUM_NAME,
					ATTACK_QB: qb,
					**data }

			#measurements.append(m)
			helper.append_dicts_to_csv(m, out_path, f"{RECENUM_NAME}.csv")


if __name__ == "__main__":
	MeasureRecEnumSuccProb("experiment_data/small", "measurements/small/10its", 10, time_func=time.time_ns)




