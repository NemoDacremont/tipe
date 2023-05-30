
A=$1
V0=$2
HOSTNAME=$(hostname)

mkdir -p ./sim_tmp/$HOSTNAME
mkdir -p ./vitessesSimulees/$HOSTNAME

rm -f ./sim_tmp/$HOSTNAME/feux$A$V0.csv ./sim_tmp/$HOSTNAME/voitures$A$V0.csv
touch ./sim_tmp/$HOSTNAME/feux$A$V0.csv ./sim_tmp/$HOSTNAME/voitures$A$V0.csv

rm -f ./vitessesSimulees/$HOSTNAME/vitesses$A$V0.csv
touch ./vitessesSimulees/$HOSTNAME/vitesses$A$V0.csv

for i in $(seq -1 5 300)
do
	echo $i
	./main.py 5 $i $A $V0
done

