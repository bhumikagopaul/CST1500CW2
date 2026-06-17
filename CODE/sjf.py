# Non-Preemptive Shortest Job First (SJF)

def calculate_sjf(processes):
    """Calculate  and return Waiting Time, Turn Around Time, Average Waiting Time, Average Turn Around Time for SJf Scheduling"""

    # Sorting by burst time x[1] for each tuple x
    processes.sort(key=lambda x: x[1])

    # Initialising 2 lists to store waiting time and turnaround time. 
    # Each list has the same number of items as processes and all items are set to 0 initially. 
    waiting_time = [0] * len(processes)
    turnaround_time = [0] * len(processes)

    # Calculating waiting and turnaround times
    for i in range(len(processes)):
        if i > 0:
            waiting_time[i] = waiting_time[i-1] + processes[i-1][1]  # waiting time for current process = waiting time for previous process + burst time of previous process
        turnaround_time[i] = waiting_time[i] + processes[i][1]       # turn around time = waiting time + burst time

    # Calculating average waiting time and average turnaround time
    avg_waiting = sum(waiting_time) / len(processes)
    avg_turnaround = sum(turnaround_time) / len(processes)

    return waiting_time, turnaround_time, avg_waiting, avg_turnaround


def display_results(processes, waiting_time, turnaround_time, avg_waiting, avg_turnaround):
    """Display SJF Scheduling in a table format"""

    print("\n--- SJF Scheduling Results ---")
    print(f"{'Process Number':^15}{'Burst Time':^15}{'Waiting Time':^15}{'Turn Around Time':^20}")
    for i in range(len(processes)):
        print(f"{processes[i][0]:^15}{processes[i][1]:^15}{waiting_time[i]:^15}{turnaround_time[i]:^20}")

    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")


def main():
    # Asking user to input the number of processes
    num_processes = int(input("\nEnter the number of processes: "))

    # Asking user to input the burst times for the processes
    processes = []     # empty list to store processes in the format tuple (PID, burst time)
    for i in range(num_processes):
        burst_time = int(input(f"Enter the burst time for process {i+1}: "))
        processes.append((i+1, burst_time))

    # SJF Scheduling calculation
    waiting_time, turnaround_time, avg_waiting, avg_turnaround = calculate_sjf(processes)

    # Displaying results
    display_results(processes, waiting_time, turnaround_time, avg_waiting, avg_turnaround)


if __name__ == "__main__":
    main()