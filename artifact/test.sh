#! /bin/bash

# check that relevant cores exist and processes can be assigned to them
cores_available=1
for i in {0..64}
do
	l2=$((i + 64));
	if ! taskset -c ${i},${l2} echo "testing cores ${i}, ${l2}"; then
		echo "failed for cores ${i}, ${l2}";	
		cores_available=0;
	fi
done

if [ $cores_available -eq 1 ]; then
	echo "All cores available";
else
	echo "The command 'taskset -c <i>, <i+64> echo \"testing cores <i>, <i+64>\"' has failed for some cores. Please make sure this succeeds for i=0..60";
	exit 1;
fi

# Test if data generation works. It's not detrimental if this fails, 
# since we provide our data sets for the large experiments
echo 'generating small data sets'

rm -r experiment_data/small > /dev/null 2>&1
if ! python3 gen_MKPID_data.py --silent experiment_data/small 2 100; then
	echo "data set generation failed, are the right packages installed?"
fi

# do test run with one iteration on small data sets, this should not take long.
echo 'running measurements on small data'
for i in {0..49}
do
	l2=$((i + 64))
	tmux new-session -d -s mpmc-chunk$i "echo '${i} ${l2}' && taskset -c ${i},${l2} python3 run_experiments.py experiment_data/small measurements/small 1 ${i}"
done

for i in {50..60}
do
	l2=$((i + 64))
	tmux new-session -d -s PSU$i "echo '${i} ${l2}' && taskset -c ${i},${l2} python3 measure_PSU.py measurements/small 100 1 ${i}"
done

echo 'tests complete'