from attacks.PSU.PSUCA_MKPM import PSU_CA_MKPM_Intersection, prio_PSI_tot, prio_PSI_pos, prio_PSI_neg
from mpmc_functionality import MPMCFunctionality
from constants import *
from math import floor
from time import time_ns
import argparse
import helper

def Measure_PSUCA_MKPSI_Single(experiment, V, T, out_directory, repetitions=100, time_func=time_ns, query_budget_increment_fraction=0.1):
	priorities = [(PRIO_TOT, prio_PSI_tot), (PRIO_POS, prio_PSI_pos), (PRIO_NEG, prio_PSI_neg)]
	
	true_pos, true_neg = matched_records(T, V)

	MPMC = MPMCFunctionality(V)
	
	for (prio_name, prio) in priorities:
		print(f"Priority: ", prio_name)
		theoretical_max_queries = len(T) + 1
		inc = max(1, floor(theoretical_max_queries * query_budget_increment_fraction))

		for qb in range(inc, theoretical_max_queries + inc, inc):
			print(f"query budget: {qb}")
			MPMC.set_query_budget(qb)

			data = {TIME_ALL : [],
					LEN_POS_RECOVERED: [],
					LEN_NEG_RECOVERED: [],
					NUM_QUERIES: [] }

			for _ in range(repetitions):
				MPMC.reset()
				pos, neg, info = PSU_CA_MKPM_Intersection(MPMC.invoke_C_fast, T, prio, get_time=time_func)
				
				# for t in pos:
				# 	if t not in true_pos:
				# 		print(f"{t} in pos but not true_pos")
				# for t in neg:
				# 	if t not in true_neg:
				# 		print(f"{t} in neg but not true_neg")
				# if len(pos) != len(true_pos) or len(neg) != len(true_neg):
				# 	print(f"length mismatch: |pos|: {len(pos)}, |true_pos|: {len(true_pos)}, |neg|: {len(neg)}, |true_neg|: {len(true_neg)}")
				# print(f"pos     : {pos}")
				# print(f"true_pos: {true_pos}")

				info[NUM_QUERIES] = MPMC.invocations()
				info[LEN_POS_RECOVERED] = len(pos)
				info[LEN_NEG_RECOVERED] = len(neg)

				helper.update_dict(data, info)
			
			m = {	**experiment,
					ATTACK_PRIORITY: prio_name,
					ATTACK_NAME: PSUCA_MKPM_NAME,
					ATTACK_QB: qb,
					LEN_POS_TRUE: len(true_pos),
					LEN_NEG_TRUE: len(true_neg),					
					**data }

			#measurements.append(m)
			helper.append_dicts_to_csv(m, out_directory, f"{PSUCA_MKPM_NAME}.csv")

def matched_records(T, V):
	pos = []
	neg = []

	IDV = helper.IDs(V)
	for t in T:
		found = False
		for e in t:
			is_element = e in IDV
			if is_element:
				pos.append(t)
				found = True
				break
		if not found:
			neg.append(t)
	return pos, neg

experiment_distribution = [(500, 600, 700), (800, 900), (1000, 1000), (1100, 1100), (1200, 1200), (1300, 1300), (1400, 1400), (1500, 1500)]

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("experiment_directory")
	parser.add_argument("out_directory")
	parser.add_argument("repetitions")
	parser.add_argument("core_id")
	args = parser.parse_args()

	experiment_directory = args.experiment_directory
	out_directory = args.out_directory
	repetitions = int(args.repetitions)
	core_id = int(args.core_id)

	experiments = helper.get_experiments(experiment_directory)
	for experiment in experiments:

		if experiment[EXP_LEN_T] < experiment_distribution[core_id][0] or experiment[EXP_LEN_T] > experiment_distribution[core_id][1]:
			continue

		# if experiment[EXP_MATCH_V_FRACTION] in [i/10 for i in range(1, 11, 1)] + [f"i/10" for i in range(1, 11, 1)]:
		# 	print(f"skipping experiment {experiment[EXP_NAME]}")
		# 	continue

		print(f"running experiment: {experiment[EXP_NAME]}")
		T = helper.csv_to_2Dlist(experiment[EXP_T_PATH])
		V = helper.csv_to_2Dlist(experiment[EXP_V_PATH])

		Measure_PSUCA_MKPSI_Single(experiment, V, T, out_directory, repetitions, time_func=time_ns, query_budget_increment_fraction=0.1)