# CPU Scheduling Algorithms

This project implements basic CPU scheduling algorithms:

* FCFS (First Come First Served)
* SJF (Non-preemptive)
* SJF Preemptive (SRTF)
* Round Robin
* Priority Scheduling (Non-preemptive & Preemptive)

## Features

* Load processes from CSV file
* Display Gantt chart
* Show:

  * Waiting time
  * Turnaround time
  * Response time

## Input format (.csv)

```
id,arrival,burst,priority
1,0,8,2
2,1,4,1
```

## Run

```
python main.py
```

## Note

* Smaller number = Higher Priority
* Quantum for Round Robin
