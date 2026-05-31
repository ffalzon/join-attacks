import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add parent directory to sys.path
sys.path.append(parent_dir)

from random import sample
from PSU_functionality import PSU
from attacks.PSU.PSU_attack import PSU_Diff

U = [i for i in range(10000)]
U_neg = [i for i in range(10000, 20000)]


for l in range(1000):
	Y_lst = sample(U, k = l)
	Y = set(Y_lst)
	for IS in range(0, l + 1):
		for diff in range(20):
			X = set(sample(Y_lst, k=IS) + sample(U_neg, k = diff))

			PSU_func = PSU(X)
			
			pos = PSU_Diff(PSU_func.PSU, Y)

			assert set(pos) == set(X).intersection(set(Y))


		