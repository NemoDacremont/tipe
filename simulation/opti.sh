#!/bin/sh


for A in $(seq 2.2 0.1 3.2)
do
	for V0 in $(seq 7.5 0.2 9.1)
	do
		echo Début $A, $V0
		./simu.sh $A $V0
	done
done



