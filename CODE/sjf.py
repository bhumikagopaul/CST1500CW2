# Non-Preemptive Shortest Job First (SJF)

# List of processes - tuples in the format (pid, burst_time) - hardcoded for now
processes = [(1, 5), (2, 3), (3, 7)]

# Sorting by burst time x[1] for each tuple x
processes.sort(key=lambda x: x[1])

# Initialising 2 lists to store waiting time and turnaround time. 
# Each list has the same number of items as processes and everything is set to 0 initially. 
waiting_time = []
turnaround_time = []

for i in range(len(processes)):
    waiting_time.append(0)
    turnaround_time.append(0)

# Calculating waiting times
for i in range(1, len(processes)):
    waiting_time[i] = waiting_time[i-1] + processes[i-1][1]  # waiting time for current process = waiting time for previous process + burst time of previous process

# Calculating turnaround times
for i in range(len(processes)):
    turnaround_time[i] = waiting_time[i] + processes[i][1]   # turn around time = waiting time + burst time

# Printing results
print("\nPID\tBurst\tWaiting\tTurnaround")
for i in range(len(processes)):
    print(f"{processes[i][0]}\t{processes[i][1]}\t{waiting_time[i]}\t{turnaround_time[i]}")

# Calculating average waiting time and average turnaround time
avg_waiting = sum(waiting_time) / len(processes)
avg_turnaround = sum(turnaround_time) / len(processes)

print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
print(f"Average Turn Around Time: {avg_turnaround:.2f}\n")