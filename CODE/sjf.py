# Non-Preemptive Shortest Job First (SJF)

import threading, time

# Storing processes as objects rather than tuples
class Process:
    def __init__(self, pid, burst_time):   # __init__ = initialiser, runs automatically when a new object is created and sets its attributes
        self.pid = pid
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0


# Lock ensures only one thread prints at a time
lock = threading.Lock()


def calculate_sjf(processes):
    """Calculate and return Average Waiting Time, Average Turn Around Time for SJF Scheduling."""

    # Sorting processes by burst time
    processes.sort(key=lambda p: p.burst_time)

    # Calculating waiting and turnaround times
    for i in range(len(processes)):
        if i > 0:
            processes[i].waiting_time = processes[i-1].waiting_time + processes[i-1].burst_time  # waiting time for current process = waiting time for previous process + burst time of previous process
        processes[i].turnaround_time = processes[i].waiting_time + processes[i].burst_time       # turn around time = waiting time + burst time

    # Calculating average waiting time and average turnaround time
    avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)

    return avg_waiting, avg_turnaround


def display_results(processes, avg_waiting, avg_turnaround):
    """Display Non-Preemptive SJF Scheduling in a table format."""

    print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")
    print(f"{'Process Number':^15}{'Burst Time':^15}{'Waiting Time':^15}{'Turn Around Time':^20}")
    print("-" * 65)
    for p in processes:
        print(f"{p.pid:^15}{p.burst_time:^15}{p.waiting_time:^15}{p.turnaround_time:^20}")
    print("-" * 65)
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")


def run_process(process):
    """Simulate running a process with synchronisation."""

    with lock:   # ensures clean printing, no overlapping text
        print(f"Process {process.pid} started. (Burst time = {process.burst_time})")
    time.sleep(process.burst_time * 1)   # pauses execution for burst time seconds
    with lock:
        print(f"Process {process.pid} finished.")


def main():
    # Asking user to input the number of processes
    num_processes = int(input("\nEnter the number of processes: "))

    # Asking user to input the burst times for the processes
    processes = []     # empty list to store instances of Process
    for i in range(num_processes):
        burst_time = int(input(f"Enter the burst time for process {i+1}: "))
        processes.append(Process(i+1, burst_time))

    # Demonstrating sequential execution with threads
    print("\n=== Simulated Execution with threads ===")

    # Creating and starting a thread for each process
    threads = []
    for p in processes:
        t = threading.Thread(target=run_process, args=(p,))   # each process runs in its own thread
        threads.append(t)
        t.start()
        t.join()   # waits for the thread to finish before continuing

    # Calculating SJF and displaying table
    avg_waiting, avg_turnaround = calculate_sjf(processes)
    display_results(processes, avg_waiting, avg_turnaround)


if __name__ == "__main__":
    main()