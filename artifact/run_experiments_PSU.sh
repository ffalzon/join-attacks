#! /bin/bash

for i in {0..10}
do
	l1=$((i + 16))
	l2=$((l1 + 64))
	tmux new-session -d -s PSU$i "echo '${l1} ${l2}' && taskset -c ${l1},${l2} python3 measure_PSU.py measurements/PSU_1M_50its_shufT_all_finegrained 50 ${i}"
done
