
a=$1

rm -f ./sim_tmp/feux$a.csv ./sim_tmp/voitures$a.csv
touch ./sim_tmp/feux$a.csv ./sim_tmp/voitures$a.csv

rm -f ./vitessesSimulees/vitesses$a.csv
touch ./vitessesSimulees/vitesses$a.csv

for i in $(seq -1 5 300)
do
	echo $i
	./main.py 5 $i $a
done

