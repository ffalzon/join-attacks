# This file contains the implementation of the basic partial set reconstruction attack
# that is based on padding each record in the target set to a unique length.
# Corresponding Google Doc Section: "GENERALIZATION: Partial set recovery"

import mpmc_functionality as mpmc_func
import helper as h
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-T", help="Path to CSV file containing the target set T")
parser.add_argument("-P", help="Path to CSV file containing the victim set P")
parser.add_argument("-d", "--delimiter", help="CSV delimiter")

args = parser.parse_args()

DEFAULT_T = "csv/1_T.csv"
DEFAULT_P = "csv/1_P.csv"

t_path = args.T if args.T != None else DEFAULT_T
p_path = args.P if args.P != None else DEFAULT_P
delimiter = args.delimiter if args.delimiter != None else ";"

# setup functionality once
MPMC = mpmc_func.MPMCFunctionality()
MPMC.set_P_from_csv(p_path, delimiter=delimiter)


# actual attack starts here
T = h.csv_to_2Dlist(t_path, delimiter=delimiter)

# sorting is not strictly necessary but potentially reduces the amount of padding added
T.sort(key=lambda c: len(c)) 

R = {}

ctr = 1
for i in range(len(T)):
	if len(T[i]) < ctr:
		T[i] += [0] * (ctr - len(T[i]))
	ctr = len(T[i]) + 1
	
	R[len(T[i])] = T[i]

UID, MC, lenP, intersection_size, G = MPMC.invoke_C(T)

P_recon = {}

for (e, e_data) in G.edges.items():
	vc, vp, _ = e
	j = e_data['c_idx']
	
	if vp not in P_recon:
		P_recon[vp] = []

	len_vc = len(G.nodes[vc]['enc_record'])
	P_recon[vp].append(R[len_vc][j])

print("Partial reconstruction of P:")
for (k, v) in P_recon.items():
	print(v)


