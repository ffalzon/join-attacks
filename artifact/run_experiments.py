from os import makedirs
from os.path import join, exists
from constants import *
from math import ceil
import time
import argparse
import traceback
import helper

from measure_recon_attacks import MeasureReconAttacksSingle
from mkpsi_querybudget import MeasureMKPSISingle
 

def do_run(experiments, out_directory, repetitions):
	for experiment in experiments:
		print(f"running experiment: {experiment[EXP_NAME]}")
		T = helper.csv_to_2Dlist(experiment[EXP_T_PATH])
		V = helper.csv_to_2Dlist(experiment[EXP_V_PATH])

		MeasureReconAttacksSingle(experiment, V, T, out_directory, repetitions, time_func=time.time_ns)
		
		ID_T = helper.IDs(T)
		ID_V = helper.IDs(V)
		intersection = ID_T.intersection(ID_V)
		unmatched_ids_T = len(ID_T) - len(intersection)
		MeasureMKPSISingle(experiment, V, T, ID_T, ID_V, intersection, unmatched_ids_T, out_directory, repetitions, time_func=time.time_ns, query_budget_increment_fraction=0.1)
	
# assign experiments to cores 0..50 in a way that should distribute the load more or less evenly
def assign_experiments(experiments, core_id):
	if 45 <= core_id <= 48:
		idx1 = core_id % 45 + 1
		idx2 = core_id % 45 + 6
		return [experiments[5*11 + idx1], experiments[5*11 + idx2]]		
	
	if 40 <= core_id <= 44:
		lower_chunk = core_id % 40
		upper_chunk = 10 - lower_chunk
		
		return [experiments[lower_chunk * 11 + 5], experiments[upper_chunk * 11 + 5]]
	
	if core_id == 49:
		return [experiments[5*11+5]] + [experiments[i * 11] for i in range(11)] + [experiments[i*11 + 10] for i in range(11)]

	core_group = core_id // 8
	lower_chunk = core_group
	upper_chunk = 10 - core_group

	lower_idx = core_id % 8 + 1
	if lower_idx >= 5:
		lower_idx += 1

	upper_idx = ((core_id % 8) + 6) % 10 
	if upper_idx <= 4:
		upper_idx += 1

	return [experiments[lower_chunk * 11 + lower_idx], experiments[upper_chunk * 11 + upper_idx]]

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("experiments_directory")
	parser.add_argument("out_directory")
	parser.add_argument("repetitions")
	parser.add_argument("core_id")
	parser.add_argument("-e", "--experiment", required=False)

	args = parser.parse_args()
	experiments_directory = args.experiments_directory
	out_directory = args.out_directory
	repetitions = int(args.repetitions)
	
	experiments = helper.get_experiments(experiments_directory)
	
	if args.experiment is not None:
		experiment = None
		for e in experiments:
			if e[EXP_NAME] == args.experiment:
				experiment = e
				break

		if experiment is None:
			print(f"Experiment {args.experiment} not found")
			quit()

		out_directory = join(out_directory, f"experiment_{args.experiment}")
		if not exists(out_directory):
			makedirs(out_directory)

		do_run([experiment], out_directory, repetitions)
		quit()
	
	
	core_id = int(args.core_id)
	assert  0 <= core_id <= 60

	# out_directory = join(out_directory, f"core{core_id}")
	# if not exists(out_directory):
	# 	makedirs(out_directory)
		
	experiments = assign_experiments(experiments, core_id)
	print(f"Core {core_id} running experiments: ", [e[EXP_NAME] for e in experiments])
	do_run(experiments, out_directory, repetitions)



		

