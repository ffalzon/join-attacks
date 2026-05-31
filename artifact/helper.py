import random
import csv
import ast
from os import listdir, makedirs
from os.path import join, isfile, exists
from constants import *

# class to sample random integers from some range with/without repetitions
class Sampler:
	# Default sampling range at the moment is 0 to max 32-bit int value
	# not even a group at the moment, may change later but strictly speaking it shouldn't matter
	def __init__(self, allowRepetitions=True, min=0, max=100000000):
		if not allowRepetitions:
			self.allowRepetitions = allowRepetitions
			self._sampled_elements = set()
			self.min = min
			self.max = max

	def sample(self):

		if self.allowRepetitions:
			return random.randint(self.min, self.max)
		
		r = random.randint(self.min, self.max)
		while r in self._sampled_elements:
			r = random.randint(self.min, self.max)
		
		self._sampled_elements.add(r)
		return r

# basic implementation of a lazily sampled random function	
class RandomFunction:
	def __init__(self,injective = False):
		self._memo = {}
		self.injective = injective

		if injective:
			self.sampler = Sampler(allowRepetitions=False)

	def eval(self, x):
		if x in self._memo:
			return self._memo[x]
		
		
		r = self.sampler.sample()
		self._memo[x] = r
		return r

def csv_to_2Dlist(path, delimiter=";", skip_header=True):
	with open(path, 'r') as f:
		csv_reader = csv.reader(f, delimiter=delimiter)
		L = list(csv_reader)
	if skip_header:
		L = L[1:]

	for i in range(len(L)):
		for j in range(len(L[i])):
			L[i][j] = L[i][j].strip()
	return L

def Substitute(leakV, D):
	recon = [[D[e] for e in v if e in D.keys()] for v in leakV]
	return recon

def argmin(lst):
	min = lst[0]
	min_idx = 0
	for i in range(1, len(lst)):
		if lst[i] < min:
			min = lst[i]
			min_idx = i
	return min_idx

def argmax(lst):
	max = lst[0]
	max_idx = 0
	for i in range(1, len(lst)):
		if lst[i] > max:
			max = lst[i]
			max_idx = i
	return max_idx

def get_experiments(data_path):
	experiments_file = join(data_path, "experiments.csv")
	with open(experiments_file) as exp_f:
		r = csv.DictReader(exp_f, skipinitialspace=True, delimiter=";")
		experiments = list(r)

	for e in experiments:
		e[EXP_T_PATH] = join(data_path, e[EXP_T_PATH])
		e[EXP_V_PATH] = join(data_path, e[EXP_V_PATH])
		e[EXP_LEN_T] = int(e[EXP_LEN_T])
		e[EXP_LEN_V] = int(e[EXP_LEN_V])
		e[EXP_MATCH_V_FRACTION] = float(e[EXP_MATCH_V_FRACTION])
	
	return experiments
	"""
	# convention: file name should be of the form '<experiment_name>_(T|V).csv'
	data_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
	used = [False for _ in range(len(data_files))]

	# Find matching target and victim csv files and store them as pairs
	# Read files only later when using them, since they may be quire large
	sets = []
	for i in range(len(data_files)):
		if used[i]:
			continue

		for j in range(len(data_files)):
			if used[j]:
				continue

			if i != j and data_files[i][:-6] == data_files[j][:-6]:
				used[i] = True
				used[j] = True
				
				if data_files[i][-6:] == "_T.csv":
					T_path = join(data_path, data_files[i])
					V_path = join(data_path, data_files[j])
				elif data_files[i][-6] == "_V.csv":
					T_path = join(data_path, data_files[j])
					V_path = join(data_path, data_files[i])
				else:
					print(f"Incorrect file name formats: {data_files[i]}, {data_files[j]}")
					continue
				sets.append({EXP_T_PATH: T_path, 
							EXP_V_PATH: V_path, 
							EXP_NAME: data_files[i][:-6]})
				
	return sets"""

def dicts_to_csv(dict_list, out_path, out_filename):
	max_dict_idx = argmax([len(d.keys()) for d in dict_list])
	dir = out_path
	if not exists(dir):
		makedirs(dir)

	with open(join(dir, out_filename), "w") as f:
		w = csv.DictWriter(f, dict_list[max_dict_idx].keys(), delimiter=";")
		w.writeheader()
		w.writerows(dict_list)

def append_dicts_to_csv(dicts : dict | list[dict], out_path, out_filename):
	if not exists(out_path):
		makedirs(out_path)

	file_path = join(out_path, out_filename)
	writeHeader = False
	if not exists(file_path):
		writeHeader = True

	if not isinstance(dicts, list):
		dicts = [dicts]

	with open(file_path, "a") as f:
		w = csv.DictWriter(f, dicts[0].keys(), delimiter=";")
		if writeHeader:
			w.writeheader()
		
		w.writerows(dicts)

def IDs(X):
	return set([id for x in X for id in x])

def dict_bin_op(d1, d2, op):
	for k in d1.keys():
		if k not in d2.keys():
			continue
		
		if not isinstance(d1[k], (int, float)) or not isinstance(d2[k], (int, float)):
			continue

		d1[k] = op(d1[k], d2[k])
	return d1

def dict_unary_op(d1, op):
	for k in d1.keys():
		if not isinstance(d1[k], (int, float)):
			continue

		d1[k] = op(d1[k])
	return d1

def parse_lists(data, tryConvertNumeric=True):
	for dic in data:
		for k in dic.keys():
			if not isinstance(dic[k], str) or dic[k].strip()[0] != '[':
				continue

			dic[k] = listrepresentation_to_list(dic[k], toNumeric=tryConvertNumeric)
			
def convert_numeric(dicts):
	for d in dicts:
		for key in d.keys():
			val = d[key]
			if isinstance(val, list):
				continue
			
			d[key] = try_to_num(val)

def try_to_num(x):
		try:
			return int(x)
		except:
			try:
				return float(x)
			except:
				if x == '':
					return 0
				return x

def listrepresentation_to_list(list_str, toNumeric=True):
	lst = ast.literal_eval(list_str)
	
	if not toNumeric:
		return lst
	
	for i in range(len(lst)):
		lst[i] = try_to_num(lst[i])
	
	return lst

def update_dict(d1, d2):
	for k in d1:
		if k in d2.keys():
			d1[k].append(d2[k])
		else: 
			print(k)
			d1[k].append('')

def DIV_CONST(c):
	return lambda x: x / c

BIN_ADD = lambda x, y: x + y 


# Helper functions for data generation

# http://pynative.com/python-count-number-of-lines-in-file/
def line_numbers_in_file(file_path):
	def _count_generator(reader):
		b = reader(1024 * 1024)
		while b:
			yield b
			b = reader(1024 * 1024)

	with open(file_path, 'rb') as fp:
		c_generator = _count_generator(fp.raw.read)
		# count each \n
		count = sum(buffer.count(b'\n') for buffer in c_generator)
		return count

def parse_fancy_int(size):
	mag = size[-1]
	fac = 1

	if mag == "K" or mag == "k":
		fac = 1000
	elif mag == "M" or mag == "m":
		fac = 10**6
	else:
		try:
			return int(size)
		except ValueError:
			return -1
	
	try:
		s = int(size[:-1])
		return s * fac
	except ValueError:
		return -1
	
def gen_fresh_ID(ID_store):
	selection = '0123456789abcdef'
	i = 0
	ok = False
	while not ok and i <= 10:
		i += 1
		ID_1 = [random.choice(selection) for _ in range(8)]
		ID_2 = [random.choice(selection) for _ in range(4)]
		ID_3 = [random.choice(selection) for _ in range(4)]
		ID_4 = [random.choice(selection) for _ in range(4)]
		ID_5 = [random.choice(selection) for _ in range(12)]
		ID = f"{"".join(ID_1)}-{"".join(ID_2)}-{"".join(ID_3)}-{"".join(ID_4)}-{"".join(ID_5)}"

		if ID not in ID_store:
			ID_store.add(ID)
			return ID

	return -1

def list_to_csv(header, lst, filename):
	with open(filename, 'w') as out_file:
		c_writer = csv.writer(out_file, delimiter=";")
		c_writer.writerow(header)
		c_writer.writerows(lst)