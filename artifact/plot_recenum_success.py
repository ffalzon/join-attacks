from os.path import join
from constants import *
import matplotlib.pyplot as plt
from statistics import mean
import helper
import csv

def PlotRecEnumSuceess(data_path, out_path):
	recenum_path = join(data_path, f"{RECENUM_NAME}.csv")
	with open(recenum_path) as f:
		r = csv.DictReader(f, skipinitialspace=True, delimiter=';')
		measurements = list(r)
		helper.parse_lists(measurements)
		helper.convert_numeric(measurements)

	V_sizes = list(set([m[EXP_LEN_V] for m in measurements]))
	V_sizes.sort()
	V_size = V_sizes[-1]

	measurements = [m for m in measurements if m[EXP_LEN_T] == V_size and m[EXP_LEN_V] == V_size]
	match_rates = list(set(m[EXP_MATCH_V_FRACTION] for m in measurements))
	match_rates.sort()

	for rate in match_rates:
		rate_measurements = [m for m in measurements if m[EXP_MATCH_V_FRACTION] == rate]
		x = []
		y = []
		
		for m in rate_measurements:
			x.append(m[ATTACK_QB])
			y.append(mean(m[ATTACK_SUCCESS]))
		plt.plot(y, label=f"{int(rate*100)}%") #scatter(x, y, marker="+", label=f"{int(rate*100)}%")
	
	plt.legend(ncols=len(match_rates)//2 - 1, loc="upper center", bbox_to_anchor=(0.4, 1.06), handletextpad=0.1)
	plt.ylabel("Success Probability")
	plt.xlabel("Query Budget")
	plt.title(f"Record Enumeration Success Probability with n = m = {V_size}", pad=20)
	
	save_path = join(data_path, "recenum_success_prob.png")
	plt.savefig(save_path, dpi=300)

if __name__ == '__main__':
	PlotRecEnumSuceess("measurements/10its", "measurements/10its")
