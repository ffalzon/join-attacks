#! /bin/bash

for i in {0..49}
do
	l2=$((i + 64))
	tmux new-session -d -s mpmc-chunk$i "echo '${i} ${l2}' && taskset -c ${i},${l2} python3 run_experiments.py experiment_data/paper measurements/large 50 ${i}"
done

for i in {50..60}
do
	l2=$((i + 64))
	cid=$((i - 50))
	tmux new-session -d -s PSU$i "echo '${i} ${l2}' && taskset -c ${i},${l2} python3 measure_PSU.py measurements/large 50 ${cid}"
done