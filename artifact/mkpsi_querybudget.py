from mpmc_functionality import MPMCFunctionality
from attacks.mkpsi import MK_PSI, PriorityTotal, PriorityPos, PriorityNeg
from math import floor
from constants import *
import helper
import time

def MeasureMKPSISingle(experiment, V, T, ID_T, ID_V, intersection, unmatched_ids_T, out_directory, repetitions=100, time_func=time.time, query_budget_increment_fraction=0.05, silent=False):
	priorities = [(PRIO_TOT, PriorityTotal), (PRIO_POS, PriorityPos), (PRIO_NEG, PriorityNeg)]
	
	MPMC = MPMCFunctionality(V)
	
	for (prio_name, prio) in priorities:
		if not silent:
			print(f"Priority: ", prio_name)
		theoretical_max_queries = len(T)
		inc = max(1, floor(theoretical_max_queries * query_budget_increment_fraction))

		for qb in range(inc, len(T) + inc, inc):
			if not silent:
				print(f"query budget: {qb}")
			MPMC.set_query_budget(qb)

			data = {TIME_ALL : [],
					LEN_POS_RECOVERED: [],
					LEN_NEG_RECOVERED: [],
					NUM_QUERIES: [],
					ATTACK_SUCCESS: [] }

			for _ in range(repetitions):
				MPMC.reset()
				pos, neg, info = MK_PSI(MPMC.leakage_sha256, T, p=prio, qb=qb, get_time=time_func)
				
				if len(pos.intersection(intersection)) == len(pos) and len(neg.intersection(intersection)) == 0:
					info[ATTACK_SUCCESS] = 1

				info[NUM_QUERIES] = MPMC.invocations()
				info[LEN_POS_RECOVERED] = len(pos)
				info[LEN_NEG_RECOVERED] = len(neg)

				helper.update_dict(data, info)
			
			m = {	**experiment,
					EXP_LEN_ISPACE_T: len(ID_T),
					EXP_LEN_ISPACE_V: len(ID_V),
					ATTACK_PRIORITY: prio_name,
					ATTACK_NAME: MKPSI_NAME,
					ATTACK_QB: qb,
					LEN_POS_TRUE: len(intersection),
					LEN_NEG_TRUE: unmatched_ids_T,					
					**data }

			helper.append_dicts_to_csv(m, out_directory, f"{MKPSI_NAME}.csv")

def MeasureMkpsiRecovery(data_path, out_path, repetitions=100, query_budget_increment_fraction=0.05, time_func=time.time):
	priorities = [(PRIO_TOT, PriorityTotal), (PRIO_POS, PriorityPos), (PRIO_NEG, PriorityNeg)]
	experiments = helper.get_experiments(data_path)
	for e in experiments:
		print(f"experiment: {e[EXP_NAME]}")
		
		T = helper.csv_to_2Dlist(e[EXP_T_PATH])
		V = helper.csv_to_2Dlist(e[EXP_V_PATH])

		ID_T = helper.IDs(T)
		ID_V = helper.IDs(V)
		intersection = ID_T.intersection(ID_V)
		unmatched_ids_T = len(ID_T) - len(intersection)

		MPMC = MPMCFunctionality(V)
		
		for (prio_name, prio) in priorities:
			print(f"Priority: ", prio_name)
			theoretical_max_queries = len(T)
			inc = max(1, floor(theoretical_max_queries * query_budget_increment_fraction))

			for qb in range(inc, len(T) + inc, inc):
				print(f"query budget: {qb}")
				MPMC.set_query_budget(qb)

				data = {TIME_ALL : [],
						LEN_POS_RECOVERED: [],
						LEN_NEG_RECOVERED: [],
						NUM_QUERIES: [],
						ATTACK_SUCCESS: [] }

				for _ in range(repetitions):
					MPMC.reset()
					pos, neg, info = MK_PSI(MPMC.invoke_C_fast, T, p=prio, qb=qb, get_time=time_func)
					
					if len(pos.intersection(intersection)) == len(pos) and len(neg.intersection(intersection)) == 0:
						info[ATTACK_SUCCESS] = 1

					info[NUM_QUERIES] = MPMC.invocations()
					info[LEN_POS_RECOVERED] = len(pos)
					info[LEN_NEG_RECOVERED] = len(neg)

					helper.update_dict(data, info)
				
				m = {	**e,
						EXP_LEN_ISPACE_T: len(ID_T),
						EXP_LEN_ISPACE_V: len(ID_V),
						ATTACK_PRIORITY: prio_name,
						ATTACK_NAME: MKPSI_NAME,
						ATTACK_QB: qb,
						LEN_POS_TRUE: len(intersection),
						LEN_NEG_TRUE: unmatched_ids_T,					
						**data }

				helper.append_dicts_to_csv(m, out_path, f"{MKPSI_NAME}.csv")	

if __name__ == "__main__":
	MeasureMkpsiRecovery("experiment_data/testing3", "measurements/testing3/10its_prios", 10, time_func=time.time_ns)
