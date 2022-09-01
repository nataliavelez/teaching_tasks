SUB=$1
START=${2:-1}

# main task
for RUN in $(seq $START 10)
do
	python teaching_task.py --sub=$SUB --run=$RUN
done
