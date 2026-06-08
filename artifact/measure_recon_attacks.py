from mpmc_functionality import MPMCFunctionality
from attacks.baseline import BaselineAttack
from attacks.record_enumeration import RecordEnumeration
from attacks.snake import Snake
from os.path import join, exists
from os import makedirs
from constants import *
import helper
import time

def MeasureReconAttacks(experiments, out_directory, chunk_index, repetitions=100, time_func=time.time):
	#experiments = helper.get_experiments(experiment_directory)
	
	# Record Enumeration and MKPSI are measured as part of query budget tests 
	attacks = [(BASELINE_NAME, BaselineAttack), (SNAKE_NAME, Snake), (RECENUM_NAME, RecordEnumeration)]
	
	for (attack_name, attack) in attacks:
		print(f"Attack: {attack_name}")

		#measurements = []
		for e in experiments:
			print(f"Experiment: {e[EXP_NAME]}")

			T = helper.csv_to_2Dlist(e[EXP_T_PATH])
			V = helper.csv_to_2Dlist(e[EXP_V_PATH])

			len_ID_T = len(helper.IDs(T))
			len_ID_V = len(helper.IDs(V))

			MPMC = MPMCFunctionality(V)

			times = {	TIME_ALL: [],
						TIME_PREPROCESS: [],
						TIME_POSTPROCESS: [],
						TIME_SUBST: [] }
			invocations = []

			for _ in range(repetitions):
				MPMC.reset()
				_, info = attack(MPMC.invoke_C_fast, T, get_time=time_func)

				helper.update_dict(times, info)
				invocations.append(MPMC.invocations())

			m = {	**e,
					EXP_LEN_ISPACE_T: len_ID_T,
					EXP_LEN_ISPACE_V: len_ID_V,
					ATTACK_NAME: attack_name,
					NUM_QUERIES: invocations,			
					**times }	
			
			#measurements.append(m)
			out_directory = join(out_directory, f"chunk{chunk_index}")
			helper.append_dicts_to_csv(m, out_directory, f"{attack_name}.csv")
	
def MeasureReconAttacksSingle(experiment, V, T, out_directory, repetitions=100, time_func=time.time, silent=False):
	attacks = [(SNAKE_NAME, Snake), (RECENUM_NAME, RecordEnumeration), (BASELINE_NAME, BaselineAttack)]
	
	for (attack_name, attack) in attacks:
		if not silent:
			print(f"Attack: {attack_name}")

		#measurements = []

		len_ID_T = len(helper.IDs(T))
		len_ID_V = len(helper.IDs(V))

		MPMC = MPMCFunctionality(V)

		times = {	TIME_ALL: [],
					TIME_PREPROCESS: [],
					TIME_POSTPROCESS: [],
					TIME_SUBST: [] }
		invocations = []

		for _ in range(repetitions):
			MPMC.reset()
			_, info = attack(MPMC.leakage_sha256, T, get_time=time_func)

			helper.update_dict(times, info)
			invocations.append(MPMC.invocations())

		m = {	**experiment,
				EXP_LEN_ISPACE_T: len_ID_T,
				EXP_LEN_ISPACE_V: len_ID_V,
				ATTACK_NAME: attack_name,
				NUM_QUERIES: invocations,			
				**times }	
		
		#measurements.append(m)
		helper.append_dicts_to_csv(m, out_directory, f"{attack_name}.csv")

if __name__ == "__main__":
	MeasureReconAttacks("experiment_data/testing3", "measurements/testing3/10its", 10, time_func=time.time_ns)
