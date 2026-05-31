from os.path import join
from constants import *
from statistics import mean
from math import floor, ceil
import matplotlib.pyplot as plt
import numpy as np
import helper
import csv

IMG_DPI = 300

def PlotReconstructionAttacks(data_path, out_path):
	
	keys = [EXP_NAME, EXP_LEN_T, EXP_LEN_V, EXP_MATCH_V_FRACTION, TIME_ALL, NUM_QUERIES, ATTACK_NAME]
	qb_keys = keys + [ATTACK_QB]
	
	baseline_file = join(data_path, f"{BASELINE_NAME}.csv")
	recordenum_file = join(data_path, f"{RECENUM_NAME}.csv")
	snake_file = join(data_path, f"{SNAKE_NAME}.csv")

	with open(baseline_file) as f:
		r = csv.DictReader(f, skipinitialspace=True, delimiter=';')
		baseline_measurements = [{k : row.get(k, None) for k in keys} for row in r]
		helper.parse_lists(baseline_measurements)
		helper.convert_numeric(baseline_measurements)


	with open(snake_file) as f:
		r = csv.DictReader(f, skipinitialspace=True, delimiter=';')
		snake_measurements = [{k : row.get(k, None) for k in keys} for row in r]
		helper.parse_lists(snake_measurements)
		helper.convert_numeric(snake_measurements)

	with open(recordenum_file) as f:
		r = csv.DictReader(f, skipinitialspace=True, delimiter=';')
		recordenum_measurements = [{k : row.get(k, None) for k in qb_keys} for row in r]
		recordenum_measurements = preprocess_qb_data(recordenum_measurements)
		helper.parse_lists(recordenum_measurements)
		helper.convert_numeric(recordenum_measurements)

	plot_recenum_queries(recordenum_measurements, out_path)
	plot_times([baseline_measurements, snake_measurements, recordenum_measurements], out_path)

def preprocess_qb_data(data):
	for row in data:
		row[ATTACK_QB] = int(row[ATTACK_QB])

	return extract_max_qb_per_exp(data)

def extract_max_qb_per_exp(data):
	out = []
	experiments = set([row[EXP_NAME] for row in data])
	
	for e in experiments:
		experiment_data = [row for row in data if row[EXP_NAME] == e]
		max_idx = helper.argmax([row[ATTACK_QB] for row in experiment_data])
		out.append(experiment_data[max_idx])

	return out

def plot_recenum_queries(recordenum_measurements, out_path):
	V_sizes = list(set([m[EXP_LEN_V] for m in recordenum_measurements]))
	V_sizes.sort()

	fig, axs = plt.subplots(len(V_sizes), len(V_sizes), gridspec_kw={"hspace": .3, "wspace": .3}) # for now, may have to change later
	for (i, V_size) in enumerate(V_sizes):
		T_sizes = list(set([m[EXP_LEN_T] for m in recordenum_measurements if m[EXP_LEN_V] == V_size]))
		T_sizes.sort()
		for (j, T_size) in enumerate(T_sizes):
			
			#All the same experiment with varying match rates for identifiers in V: 10% - 100%
			measurements = [m for m in recordenum_measurements if m[EXP_LEN_T] == T_size and m[EXP_LEN_V] == V_size]
			#print("plotting:", measurements)

			if j == 0:
				axs[j,i].set_title(f"n = {V_size}", fontsize=10)
			if i == 0:
				if T_size == V_size:
					label = "n = m"
				else:
					ratio = T_size / V_size
					label = f"n = {int(ratio) if ratio.is_integer() else ratio} m"
				axs[j,i].set_ylabel(label, fontsize=10, labelpad=10.0)
			
			# axs[j,i].set_ylabel("Avg. #Queries", fontsize=10)

			x = [m[EXP_MATCH_V_FRACTION] for m in measurements]
			y = [mean(m[NUM_QUERIES]) for m in measurements]
		
			min_y = floor(min(y))
			max_y = ceil(max(y))
			y_ticks = [i for i in range(min_y, max_y + 1)]
			y_labels = [f"{t}" for t in y_ticks]
			print("y_ticks:", y_ticks)
			
			axs[j,i].set_ylim([min_y-0.2, max_y+0.2])
			axs[j,i].set_yticks(y_ticks, labels=y_labels)
			axs[j,i].scatter(x, y, marker="+")

	# for m in measurements:
	# 	print(m)
	# 	#TODO: Convert csv data to int/float. Probably best write helper
	# 	print("plotting x", [m[EXP_MATCH_V_FRACTION]] * len(m[NUM_QUERIES]))
	# 	print("plotting y", m[NUM_QUERIES])
	# 	plt.scatter([m[EXP_MATCH_V_FRACTION]] * len(m[NUM_QUERIES]), m[NUM_QUERIES])
	fig.suptitle("Record Enumeration Protocol Queries per Match Rate")
	fig.savefig(join(out_path, "record_enum_queries.png"), dpi=IMG_DPI)	
	
	

def plot_times(data, out_path):
	
	V_sizes = list(set([m[EXP_LEN_V] for m in data[0]]))
	V_sizes.sort()

	fig, axs = plt.subplots(len(V_sizes), len(V_sizes), gridspec_kw={"hspace": .3, "wspace": .3}) # for now, may have to change later
	for (i, V_size) in enumerate(V_sizes):
		T_sizes = list(set([m[EXP_LEN_T] for m in data[0] if m[EXP_LEN_V] == V_size]))
		T_sizes.sort()
		for (j, T_size) in enumerate(T_sizes):
			# all_y = []
			for attack_measurements in data:
				#All the same experiment with varying match rates for identifiers in V: 10% - 100%
				measurements = [m for m in attack_measurements if m[EXP_LEN_T] == T_size and m[EXP_LEN_V] == V_size]
				#print("plotting:", measurements)
				x = [m[EXP_MATCH_V_FRACTION] for m in measurements]
				#TODO: Filter out zero times and divide accordingly!
				y = [mean(m[TIME_ALL]) for m in measurements]
				axs[j,i].scatter(x, y, marker="+", label=f"{measurements[0][ATTACK_NAME]}")

				# all_y.append(y)
				

			if j == 0:
					axs[j,i].set_title(f"m = {V_size}", fontsize=10)
			if i == 0:
				if T_size == V_size:
					label = "n = m"
				else:
					ratio = T_size / V_size
					label = f"n = {int(ratio) if ratio.is_integer() else ratio} m"
				axs[j,i].set_ylabel(label, fontsize=10, labelpad=10.0)

			# all_y = [y for d in all_y for y in d] # flatten
			# min_y = floor(min(all_y))
			# max_y = ceil(max(all_y))
			# y_ticks = [i for i in range(min_y, max_y + 1)]
			# y_labels = [f"{t}" for t in y_ticks]
			# print("y_ticks:", y_ticks)
			
			# axs[j,i].set_ylim([min_y-10, max_y+10])
			# axs[j,i].set_yticks(y_ticks, labels=y_labels)
			
	handles, labels = axs[0,0].get_legend_handles_labels()
	fig.legend(handles, labels, loc='lower center', ncols=len(data), handletextpad=0.1)		
	fig.suptitle("Runtimes per Match Rate (ns)")
	fig.savefig(join(out_path, "runtime_per_match_rate.png"), dpi=IMG_DPI)	

if __name__ == '__main__':
	PlotReconstructionAttacks("measurements/10its", "measurement_data2")

