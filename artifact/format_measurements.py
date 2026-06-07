from statistics import mean
from csv import DictReader
from os.path import join
import argparse
from constants import *
import helper

def FormatPSUTimingData(measurement_directory, out_directory):
	source_file = join(measurement_directory, f"{PSU_NAME}.csv")
	PSU_data = get_measurement_data(source_file)

	# time over n
	all_data = {}
	fill_dict(	PSU_data, 
		   		all_data,
				inner_key_name=EXP_LEN_T,
				data_key=TIME_ALL,
				outer_key_func=lambda r: (r[EXP_LEN_V], r[EXP_MATCH_V_FRACTION]),
				col_header_func=lambda r: f"{PSU_NAME}")

	for ((m, mr), data) in all_data.items():
		data2 = dict_to_list(data, EXP_LEN_T, sort=True)
		filename = f"V{m}MR{mr}.csv"
		out_path = join(out_directory, "PSU_time_over_n")
		helper.dicts_to_csv(data2, out_path, filename)

	# time over match rate
	all_data = {}
	fill_dict(	PSU_data, 
		   		all_data,
				inner_key_name=EXP_MATCH_V_FRACTION,
				data_key=TIME_ALL,
				outer_key_func=lambda r: (r[EXP_LEN_V], r[EXP_LEN_T]),
				col_header_func=lambda r: f"{PSU_NAME}")
	
	for ((m, n), data) in all_data.items():
		data2 = dict_to_list(data, EXP_MATCH_V_FRACTION, sort=True)
		filename = f"V{m}T{n}.csv"
		out_path = join(out_directory, "PSU_time_over_mr")
		helper.dicts_to_csv(data2, out_path, filename)

def FormatReconTimingData(measurement_directory, out_directory):
	baseline_file = join(measurement_directory, f"{BASELINE_NAME}.csv")
	recenum_file = join(measurement_directory, f"{RECENUM_NAME}.csv")
	snake_file = join(measurement_directory, f"{SNAKE_NAME}.csv")

	baseline_data = get_measurement_data(baseline_file)	
	recenum_data = get_measurement_data(recenum_file)
	snake_data = get_measurement_data(snake_file)

	# dictionary indexed by (|V|, |T|) pairs. 
	# Each item contains data for one subplot as dictionary of dictionaries index by match rate
	all_data = {}
	fill_time_MR_dict(baseline_data, all_data)
	fill_time_MR_dict(recenum_data, all_data)
	fill_time_MR_dict(snake_data, all_data)

	for ((m, n),data) in all_data.items():
		data = dict_to_list(data, EXP_MATCH_V_FRACTION, sort=True)
		filename = f"V{m}T{n}.csv"
		out_path = join(out_directory, "recon_time_over_MR")
		helper.dicts_to_csv(data, out_path, filename)

	all_data = {}
	fill_time_n_dict(baseline_data, all_data)
	fill_time_n_dict(recenum_data, all_data)
	fill_time_n_dict(snake_data, all_data)
	for ((m, mr),data) in all_data.items():
		data = dict_to_list(data, EXP_LEN_T, sort=True)
		
		filename = f"V{m}MR{mr}.csv"
		out_path = join(out_directory, "recon_time_over_n")
		helper.dicts_to_csv(data, out_path, filename)

	del baseline_data
	del recenum_data
	del snake_data
	
def FormatMKPSIQueryData(measurement_directory, out_directory):
	
	mkpsi_file = join(measurement_directory, f"{MKPSI_NAME}.csv")
	mkpsi_data = get_measurement_data(mkpsi_file)
	
	format_mkpsi_recovery_over_QB(mkpsi_data, out_directory)
	
	mkpsi_max_qb = filter_max_qb(mkpsi_data)
	format_mkpsi_queries_over_n(mkpsi_max_qb, out_directory)
	format_mkpsi_queries_over_MR(mkpsi_max_qb, out_directory)

def FormatMKPSITimingData(measurement_directory, out_directory):
	mkpsi_file = join(measurement_directory, f"{MKPSI_NAME}.csv")
	mkpsi_data = get_measurement_data(mkpsi_file)
	
	mkpsi_max_qb = filter_max_qb(mkpsi_data)
	format_mkpsi_time_over_n(mkpsi_max_qb, out_directory)
	format_mkpsi_time_over_MR(mkpsi_max_qb, out_directory)

def format_mkpsi_time_over_n(mkpsi_data, out_directory):
	all_data = {}
	fill_dict(	mkpsi_data, 
		   		all_data,
				inner_key_name=EXP_LEN_T,
				data_key=TIME_ALL,
				outer_key_func=lambda r: r[EXP_LEN_V],
				col_header_func=lambda r: f"time{r[EXP_MATCH_V_FRACTION]}_{r[ATTACK_PRIORITY]}")

	for (m, data) in all_data.items():
		data = dict_to_list(data, EXP_LEN_T, sort=True)
		filename = f"V{m}.csv"
		out_path = join(out_directory, "mkpsi_time_over_n")
		helper.dicts_to_csv(data, out_path, filename)

def format_mkpsi_time_over_MR(mkpsi_data, out_directory):
	all_data = {}
	fill_dict(	mkpsi_data,
		   		all_data,
				inner_key_name=EXP_MATCH_V_FRACTION,
				data_key=TIME_ALL,
				outer_key_func=lambda r: r[EXP_LEN_V],
				col_header_func=lambda r: f"time{r[EXP_LEN_T]}_{r[ATTACK_PRIORITY]}")
	#fill_time_MR_dict(mkpsi_data, all_data)

	for (m, data) in all_data.items():
		data = dict_to_list(data, EXP_MATCH_V_FRACTION, sort=True)
		filename = f"V{m}.csv"
		out_path = join(out_directory, "mkpsi_time_over_MR")
		helper.dicts_to_csv(data, out_path, filename)

def format_mkpsi_recovery_over_QB(mkpsi_data, out_directory):
	all_data = {}			
	for r in mkpsi_data:
		key = (r[EXP_LEN_V], r[EXP_LEN_T])
		if key not in all_data:
			all_data[key] = {}

		if r[ATTACK_QB] not in all_data[key]:
			all_data[key][r[ATTACK_QB]] = {}

		col_key_pos = f"pos{r[EXP_MATCH_V_FRACTION]}_{r[ATTACK_PRIORITY]}"
		col_key_neg = f"neg{r[EXP_MATCH_V_FRACTION]}_{r[ATTACK_PRIORITY]}"
		col_key_tot = f"tot{r[EXP_MATCH_V_FRACTION]}_{r[ATTACK_PRIORITY]}"

		if r[LEN_POS_TRUE] == 0:
			all_data[key][r[ATTACK_QB]][col_key_pos] = 1
		else:
			all_data[key][r[ATTACK_QB]][col_key_pos] = sum(r[LEN_POS_RECOVERED])/(r[LEN_POS_TRUE] * len(r[LEN_POS_RECOVERED]))
		
		
		if r[LEN_NEG_TRUE] == 0:
			all_data[key][r[ATTACK_QB]][col_key_neg] = 1
		else:
			all_data[key][r[ATTACK_QB]][col_key_neg] = sum(r[LEN_NEG_RECOVERED])/(r[LEN_NEG_TRUE] * len(r[LEN_NEG_RECOVERED]))
		
		# Remove the following comment once new measurements 
		# that include EXP_LEN_ISPACE_T and EXP_LEN_ISPACE_V
		# have been done (already included in measurement scripts)

		all_data[key][r[ATTACK_QB]][col_key_tot] = (sum(r[LEN_POS_RECOVERED]) + sum(r[LEN_NEG_RECOVERED]))/(r[EXP_LEN_ISPACE_T] * len(r[LEN_NEG_RECOVERED]))

	for ((m, n), data) in all_data.items():
		data = dict_to_list(data, ATTACK_QB, sort=True)
		
		filename = f"V{m}T{n}.csv"
		out_path = join(out_directory, "mkpsi_recovery_over_QB")
		helper.dicts_to_csv(data, out_path, filename)

def format_mkpsi_queries_over_n(mkpsi_max_qb_data, out_directory):
	all_data = {}
	fill_mkpsi_queries_n_dict(mkpsi_max_qb_data, all_data)
	
	for (m, data) in all_data.items():
		data = dict_to_list(data, EXP_LEN_T, sort=True)
		filename = f"V{m}.csv"
		out_path = join(out_directory, "mkpsi_queries_over_n")
		helper.dicts_to_csv(data, out_path, filename)

def format_mkpsi_queries_over_MR(mkpsi_max_qb_data, out_directory):
	all_data = {}
	fill_dict(mkpsi_max_qb_data, all_data,
		   		inner_key_name=EXP_MATCH_V_FRACTION,
				data_key=NUM_QUERIES,
				outer_key_func=lambda r: (r[EXP_LEN_V], r[EXP_LEN_T]),
				col_header_func=lambda r: f"{NUM_QUERIES}_{r[ATTACK_PRIORITY]}")
	for ((m, n), data) in all_data.items():
		data = dict_to_list(data, EXP_MATCH_V_FRACTION, sort=True)
		filename = f"V{m}T{n}.csv"
		out_path = join(out_directory, "mkpsi_queries_over_mr")
		helper.dicts_to_csv(data, out_path, filename)


# For every combination of |V|, |T| and match rate, get maximum query budget
def filter_max_qb(data):
	max_qbs = {}
	for r in data:
		key = (r[EXP_LEN_T], r[EXP_LEN_V], r[EXP_MATCH_V_FRACTION], r[ATTACK_PRIORITY])
		if key not in max_qbs or r[ATTACK_QB] > max_qbs[key][ATTACK_QB]:
			max_qbs[key] = r
	return [r for (_,r) in max_qbs.items()]

def fill_mkpsi_queries_n_dict(data, dict):
	fill_dict(	data,
		   		dict,
				inner_key_name=EXP_LEN_T,
				data_key=NUM_QUERIES,
				outer_key_func=lambda r: r[EXP_LEN_V],
				col_header_func= lambda r: f"queries{r[EXP_MATCH_V_FRACTION]}_{r[ATTACK_PRIORITY]}")

def fill_time_MR_dict(data, dict):
	fill_dict(	data, 
		   		dict, 
				inner_key_name=EXP_MATCH_V_FRACTION, 
				data_key=TIME_ALL, 
				outer_key_func=lambda r: (r[EXP_LEN_V], r[EXP_LEN_T]))
	
def fill_time_n_dict(data, dict):
	fill_dict(	data, 
		   		dict, 
				inner_key_name=EXP_LEN_T, 
				data_key=TIME_ALL, 
				outer_key_func=lambda r: (r[EXP_LEN_V], r[EXP_MATCH_V_FRACTION]))

def fill_dict(data, dict, inner_key_name, data_key, outer_key_func, col_header_func=lambda r: f"{r[ATTACK_NAME]}"):
	for r in data:
		key = outer_key_func(r)
		if key not in dict:
			dict[key] = {}

		if r[inner_key_name] not in dict[key]:
			dict[key][r[inner_key_name]] = {}

		dict[key][r[inner_key_name]][col_header_func(r)] = mean(r[data_key])


# transforms dictionary of dictionaries to list of dictionaries, adding outer key as column
def dict_to_list(dict, key_name, sort=True):
	out = []
	for (k, data) in dict.items():
		data[key_name] = k
		out.append(data)

	if sort:
		out.sort(key=lambda x: x[key_name])
	return out
		

def get_measurement_data(filename):
	with open(filename) as f:
		r = DictReader(f, delimiter=";")
		data = list(r)
		helper.parse_lists(data)
		helper.convert_numeric(data)
	return data


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("source_directory")

	args = parser.parse_args()
	source_dir = args.experiments_directory
	dst_dir = join(source_dir, "formatted")

	FormatPSUTimingData(source_dir, dst_dir)
	FormatReconTimingData(source_dir, dst_dir)
	FormatMKPSIQueryData(source_dir, dst_dir)
	FormatMKPSITimingData(source_dir, dst_dir)