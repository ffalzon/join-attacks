from PSU_functionality import PSU
from attacks.PSU.PSU_attack import PSU_Diff
from attacks.PSU.PSUCA_attack import PSU_CA_Intersection, prio_PSI_pos, prio_PSI_neg, prio_PSI_tot #prio_pos, prio_pos_reverse, prio_total
from random import sample, shuffle, seed
from time import time_ns
from constants import *
import argparse
import helper

priorities = [(PRIO_POS, prio_PSI_pos), (PRIO_NEG, prio_PSI_neg), (PRIO_TOT, prio_PSI_tot)]


def measure_PSUCA(T, V, match_rate, repetitions, out_directory, qb_increment=0.1):
	
	theoretical_upper = len(T) + 1
	inc = int(theoretical_upper * qb_increment)

	intersection = set(T).intersection(set(V))
	unmatched_T = set(T).difference(set(V))

	for qb in range(inc, theoretical_upper + inc, inc):
		print(f"QB: {qb}")
		for (prio_name, prio_func) in priorities:
			data = {
				TIME_ALL: [],
				NUM_QUERIES: [],
				LEN_POS_RECOVERED: [],
				LEN_NEG_RECOVERED: [],
				ATTACK_SUCCESS: [],
				
			}

			PSU_func = PSU(V)
			PSU_func.set_query_budget(qb)

			for _ in range(repetitions):
				PSU_func.reset()
				pos, neg, info = PSU_CA_Intersection(PSU_func.PSU_CA, T, prio_func, get_time=time_ns)
				
				success = len(pos) == len(set(pos).intersection(set(T)).intersection(set(V))) and len(set(neg).intersection(set(V))) == 0
				
				info[ATTACK_SUCCESS] = 1 if success else 0

				info[NUM_QUERIES] = PSU_func.invocations()
				info[LEN_POS_RECOVERED] = len(pos)
				info[LEN_NEG_RECOVERED] = len(neg)
				helper.update_dict(data, info)

			measurement = {
				EXP_NAME: f"T{n}V{m}_{match_rate}",
				EXP_LEN_T: len(T),
				EXP_LEN_V: len(V),
				EXP_MATCH_V_FRACTION: match_rate,
				ATTACK_NAME: PSUCA_NAME,
				ATTACK_PRIORITY: prio_name,
				LEN_POS_TRUE: len(intersection),
				LEN_NEG_TRUE: len(unmatched_T),
				ATTACK_QB: qb,
				**data }

			helper.append_dicts_to_csv(measurement, out_directory, f"{PSUCA_NAME}.csv")
		if qb >= theoretical_upper:
			break

def measure_PSU(T, V, match_rate, repetitions, out_directory):
	times = []
	successes = []
	pos_recov = []
	neg_recov = []
	
	PSU_func = PSU(V)

	intersection = set(T).intersection(set(V))
	unmatched_T = set(T).difference(set(V))

	for _ in range(repetitions):
		shuffle(T)
		PSU_func = PSU(V)

		pos, t = PSU_Diff(PSU_func.PSU, set(T))
		
		times.append(t)

		success = len(set(pos).intersection(intersection)) == len(pos) # and len(set(neg).intersection(set(V))) == 0
		successes.append(1 if success else 0)
		pos_recov.append(len(pos))
		neg_recov.append(len(T) - len(pos)) # attack is always successful, so this is technically redundant
	
	measurement = {
		EXP_NAME: f"T{n}V{m}_{match_rate}",
		EXP_LEN_T: len(T),
		EXP_LEN_V: len(V),
		EXP_MATCH_V_FRACTION: match_rate,
		LEN_POS_TRUE: len(intersection),
		LEN_NEG_TRUE: len(unmatched_T),
		TIME_ALL: times,
		ATTACK_NAME: PSU_NAME,
		ATTACK_SUCCESS: successes,
		LEN_POS_RECOVERED: pos_recov,
		LEN_NEG_RECOVERED: neg_recov
	}
	helper.append_dicts_to_csv(measurement, out_directory, f"{PSU_NAME}.csv")

def gen_sets(n, m, intersection_ratio):
	assert m >= n * intersection_ratio

	T = sample(range(0, 2*n), n)
	
	intersection_len = int(len(T) * intersection_ratio)
	V = T[:intersection_len]

	missing = m - len(V)
	V += sample(range(2*n, 2*n + 2*missing), missing)

	shuffle(V)
	assert len(T) == n and len(V) == m
	return T, V

V_size_PSU = 1_000_000
V_size_PSUCA = 10_000

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("out_directory")
	parser.add_argument("V_size_PSU")
	parser.add_argument("V_size_PSUCA")
	parser.add_argument("repetitions")
	parser.add_argument("core_id")
	args = parser.parse_args()

	out_directory = args.out_directory
	repetitions = int(args.repetitions)
	V_size_PSU = int(args.V_size_PSU)
	V_size_PSUCA = int(args.V_size_PSUCA)
	core_id = int(args.core_id)

	seed(0xCAFEBABE)

	assert 0 <= core_id <= 10
	
	ranges = [(i, i+1) for i in range(5,16)]
	
	m = V_size_PSU
	for frac in [i / 10 for i in range(0, 11)]:
		for t_frac in [i/10 for i in range(ranges[core_id][0], ranges[core_id][1])]:
			n = int(t_frac * m)
			if n * frac > m:
				break

			print(f"Experiment: PSU, n={n}, m={m}, intersection ratio={frac}")
			print("generating data")
			
			T, V = gen_sets(n, m, frac)
			
			print("running measurements")
			measure_PSU(T, V, frac, repetitions, out_directory)

	m = V_size_PSUCA
	for frac in [i / 10 for i in range(0, 11)]:
		for t_frac in [i/10 for i in range(ranges[core_id][0], ranges[core_id][1])]:
			n = int(t_frac * m)
			if n * frac > m:
				break

			print(f"Experiment: PSU-CA, n={n}, m={m}, intersection ratio={frac}")
			print("generating data")
			
			T, V = gen_sets(n, m, frac)
			
			print("running measurements")
			measure_PSUCA(T, V, frac, repetitions, out_directory)