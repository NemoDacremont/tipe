

for i in $(seq -1 5 300)
do
	echo $i
	./main.py 5 $i
done

