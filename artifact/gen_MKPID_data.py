import argparse
import random
from os.path import join, exists
from os import makedirs
from math import sqrt, floor
from faker import Faker
from helper import gen_fresh_ID, list_to_csv, IDs
import csv
import sys
from constants import *

def get_unique_id(idx, faker, ID_store):
	match idx:
		case 0: #email
			id = faker.unique.email()
		case 1: # phone
			id = faker.unique.phone_number()
		case 2: # device ID
			id = gen_fresh_ID(ID_store)
		case 3: # IP
			id = faker.unique.ipv4_public()
	return id

def GenDataSet(exp: dict, directory, match_frac_T=True, silent=False):
	
	name = exp[EXP_NAME]
	n = exp[EXP_LEN_T]
	m = exp[EXP_LEN_V]
	match_V_fraction = exp[EXP_MATCH_V_FRACTION]
	max_id_replication = exp[EXP_MAX_ID_REPL]

	if (not match_frac_T and max_id_replication * n < m) or (match_frac_T and max_id_replication * m < n):
		print(f"Choice of n, m, match rate and max_id_replication not permissible for achieving the match rate in {'T' if match_frac_T else 'V'}:")
		print(f"""n:{n},
					m:{m},
					match rate: {match_V_fraction},
					max_id_replication: {max_id_replication}""")

		raise ValueError()

	if not exists(directory):
		makedirs(directory)
	
	faker = Faker()
	ID_store = set()

	T = [[None] * 4 for _ in range(n)]
	V = [[None] * 4 for _ in range(m)]


	if match_frac_T:
		V, T = T, V
		m, n = n, m
	
	col_matches = [int(m * match_V_fraction)] * 4

	if 0 < match_V_fraction < 1: # randomize number of matched ids per column	
		num_its = random.randint(0, 300)
		skipped = 0
		for _ in range(num_its):
			i = random.randint(0,3)
			j = random.randint(0,3)
			if i == j 	or (col_matches[i] == m and col_matches[j] == m) \
						or (col_matches[i] == 0 and col_matches[j] == 0) \
						or n * max_id_replication < col_matches[i] \
						or n * max_id_replication < col_matches[j]:
				skipped += 1
				continue
				
			if col_matches[j] == m or col_matches[i] == 0:
				i,j = j,i

			col_matches[i] -= 1
			col_matches[j] += 1
		# print(col_matches)
		# print(f"skipped: {100 * (skipped/num_its) if num_its > 0 else 0}%, iterations: {num_its}")

	for i in range(4):
		ids = []
		if col_matches[i] <= n: # easy, can fill however we want, there's enough space in  set anyways
			num_added_ids = 0
			while col_matches[i] > num_added_ids:
				x = random.randint(1, min(max_id_replication, col_matches[i]-num_added_ids))
				id = get_unique_id(i, faker, ID_store)
				ids.append(id)

				ctr = 0
				for k in range(m):
					if V[k % m][i] == None:
						V[k % m][i] = id
						ctr += 1
					if ctr == x:
						break
				num_added_ids += ctr

		else: # need to make sure that the number of distinct identifiers we pick here can fit in a column of the other set
			pattern = [max_id_replication] * n
			matches = n * max_id_replication
			while matches > col_matches[i]:
				idx = random.randint(0, n - 1)
				if pattern[idx] == 0:
					continue

				pattern[idx] -= 1
				matches -= 1
			
			pattern = [p for p in pattern if p > 0]
			for p in pattern:
				id = get_unique_id(i, faker, ID_store)
				ids.append(id)

				ctr = 0
				for k in range(m):
					if V[k % m][i] == None:
						V[k % m][i] = id
						ctr += 1
					if ctr == p:
						break

		# add ids to i-th column of T
		for j, id in enumerate(ids):
			T[j][i] = id

	# fill rest of both sets with unique identifiers
	for k in range(n):
		for l in range(4):
			if T[k][l] == None:
				num = random.randint(1,max_id_replication)
				id = get_unique_id(l, faker, ID_store)
				c = 0
				for i in range(len(T)):
					idx = (k+i) % len(T)
					if T[idx][l] == None:
						T[idx][l] = id
						c += 1
					if c == num:
						break

	for k in range(m):
		for l in range(4):
			if V[k][l] == None:
				num = random.randint(1,max_id_replication)
				id = get_unique_id(l, faker, ID_store)
				c = 0
				for i in range(len(V)):
					idx = (k+i) % len(V)
					if V[idx][l] == None:
						V[idx][l] = id
						c += 1
					if c == num:
						break
	check_match_rates(V, T, match_V_fraction, silent=silent)
	

	random.shuffle(T)
	random.shuffle(V)

	if match_frac_T:
		V, T = T, V
		m, n = n, m

	T_name = f"{name}_T.csv"
	V_name = f"{name}_V.csv"

	T_path = join(directory, T_name)
	V_path = join(directory, V_name)
	list_to_csv(['email', 'phone', 'device_id', 'ip'], T, T_path)
	list_to_csv(['email', 'phone', 'device_id', 'ip'], V, V_path)
	exp[EXP_T_PATH] = T_name
	exp[EXP_V_PATH] = V_name

# Checks that the percentage of matched records in <primary> is mr
def check_match_rates(primary, secondary, mr, silent=False):
	IDS = IDs(secondary)

	pos = 0
	tot = 0
	for p in primary:
		for id in p:
			tot += 1
			if id in IDS:
				pos +=1
	ok = pos / tot == mr
	if not ok and not silent:
		print(f"Sanity check failed for |V|={len(secondary)}, |T|={len(primary)}")
		print(f"Expected: {mr}, measured: {pos/tot}")
	return ok

v_sizes = [1000]
t_fracs = [i / 10 for i in range(5, 16)]
max_id_replication = 1

if __name__ == '__main__':

	Faker.seed(0xCAFEBABE)
	random.seed(0xF0CCAC1A)

	parser = argparse.ArgumentParser()
	parser.add_argument("directory")
	parser.add_argument("max_id_replication")
	parser.add_argument("V_size")
	parser.add_argument("-s", "--silent", action="store_true")

	args = parser.parse_args()
	directory = args.directory
	max_id_replication = int(args.max_id_replication)
	V_size = int(args.V_size)
	silent = args.silent
	
	if not exists(directory):
		makedirs(directory)

	experiments = []

	for frac in t_fracs:
		t_size = int(V_size * frac)
		for mr in [i / 10 for i in range(0, 11)]:
			if not silent: 
				print(f"Generating: |V| = {V_size}, |T| = {t_size}, MR = {mr}")
			exp_params = {	EXP_NAME : f"T{t_size}V{V_size}_{mr}", 
							EXP_LEN_T: t_size, 
							EXP_LEN_V: V_size, 
							EXP_MAX_ID_REPL: max_id_replication, 
							EXP_MATCH_V_FRACTION: mr}
			try:
				GenDataSet(exp_params, directory, silent=silent)
			except ValueError:
				if not silent:
					print(f"skipping |V|={V_size}, |T|={t_size}, MR={mr}")
				continue
			experiments.append(exp_params)

	if len(experiments) > 0:
		exp_file = join(directory, "experiments.csv")
		with open(exp_file, "w") as exp_f:
			w = csv.DictWriter(exp_f, experiments[0].keys(), delimiter=";")
			w.writeheader()
			w.writerows(experiments)
