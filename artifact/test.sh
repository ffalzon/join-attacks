#! /bin/bash

# check that relevant cores exist and processes can be assigned to them
all_cores_available=1
for i in {0..60}
do
	l2=$((i + 64));
	if ! taskset -c ${i},${l2} echo "testing cores ${i}, ${l2}"; then
		echo "failed for cores ${i}, ${l2}";	
		all_cores_available=0;
	fi
done

if [ $all_cores_available -eq 1 ]; then
	echo "All cores available";
else
	echo "The command 'taskset -c <i>, <i+64> echo \"testing cores <i>, <i+64>\"' has failed for some cores. Please make sure this succeeds for i=0..60";
	exit 1;
fi

# test that tmux works
if ! tmux new-session -d -s artifact-tmux-test "echo 'tmux test'"; then
	echo "The command  tmux new-session -d -s artifact-tmux-test \"echo 'tmux test'\"  failed. Please make sure that tmux is functional";
	exit 1;
fi

# Test if data generation works. It's not detrimental if this fails, 
# since we provide our data sets for the large experiments
echo 'generating small data sets'

rm -r experiment_data/small > /dev/null 2>&1
if ! python3 gen_MKPID_data.py --silent experiment_data/small 2 100; then
	echo "data set generation failed, is the Faker package installed?"
	exit 0
fi

# do test run with one iteration on small data sets, this should not take long.
echo 'Testing attacks against MK-PrivateID'
for i in {0..49}
do
	l2=$((i + 64))
	echo "cores ${i}, ${l2}"
	# tmux new-session -d -s mpmc-chunk$i "echo '${i} ${l2}' && taskset -c ${i},${l2} python3 run_experiments.py --silent experiment_data/small measurements/small 1 ${i}"
	taskset -c $i,$l2 python3 run_experiments.py --silent experiment_data/small measurements/small 1 $i
done

echo 'Testing attacks against PSU / PSU-CA'
for i in {50..60}
do
	l2=$((i + 64))
	cid=$((i - 50))
	echo "cores ${i}, ${l2}"
	taskset -c $i,$l2 python3 measure_PSU.py --silent measurements/small 100 100 1 $cid
done
