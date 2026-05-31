from random import sample
from PSU_functionality import PSU
from attacks.PSUCA_attack import PSU_CA_Intersection, prio_total, prio_pos, prio_pos_reverse

# X = []
# Y = [685, 434, 674, 161, 183, 999, 308, 138, 485, 379, 599, 400, 798, 161, 502]

# PSU_functionality = PSU(X)

# pos, neg = PSU_CA_Intersection(PSU_functionality.PSU_CA, Y)
# print("pos: ", pos)
# print("neg", neg)

N = 100
U1 = [i for i in range(1000)]
U2 = [i for i in range(1000, 2000)]


l = 500
X = sample(U1, k = l)

# for IS in range(0, l + 1):
IS = l  // 2
for diff in range(20):
	Y = sample(X, k=IS) + sample(U2, k = diff)
	
	PSU_func = PSU(Y)
	print(f"n = {len(X)}, m = {len(Y)}, |X n Y| = {IS}")
	for prio_name, prio_func in [("total", prio_total), ("positive", prio_pos), ("pos_reverse", prio_pos_reverse)]:
		invocations = 0
		for _ in range(N):
			PSU_func.reset()
			pos, neg = PSU_CA_Intersection(PSU_func.PSU_CA, X)

			
			invocations += PSU_func.invocations()

			
			assert set(pos).union(set(neg)) == set(X)
			assert set(pos) == set(X).intersection(set(Y))
			assert set(neg) == set(X).difference(set(Y))
		
		print(f"Avg. Invocations for {prio_name}: {invocations / N} ({100 * invocations / N / (len(X) + 1)})%")
	print()
