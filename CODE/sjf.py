# Non-Preemptive Shortest Job First (SJF)

import threading, time

# Storing processes as objects rather than tuples
class Process:
    def __init__(self, pid, burst_time, arrival_time):   # __init__ = initialiser, runs automatically when a new object is created and sets its attributes
        self.pid = pid   # unique
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0


def calculate_sjf(processes):
    """Calculate and return Average Waiting Time and Average Turn Around Time for SJF Scheduling. It also returns the list order."""

    completed = 0      # number of processes completed
    current_time = 0   # current time in the simulation
    order = []         # list to store the order of execution of processes

# Continue until all processes are completed
    while completed < len(processes):
            # Selecting processes that have arrived and not yet completed
            available = [p for p in processes if (p.arrival_time <= current_time) and (p.completion_time == 0)]

            if available:
                p = min(available, key=lambda x: x.burst_time)          # Picking process with shortest burst time
                p.waiting_time = current_time - p.arrival_time
                current_time += p.burst_time                            # Advance current time by the burst time
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                order.append(p)                                         # Adding process to execution order
                completed += 1
            else:
                # If no process has arrived yet, increment time
                current_time += 1

    # Calculating average waiting time and average turnaround time
    avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)

    return avg_waiting, avg_turnaround, order


def display_results(processes, avg_waiting, avg_turnaround):
    """Display Non-Preemptive SJF Scheduling in a table formatwith averages."""

    print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")
    print(f"{'Process Number':^15}{'Arrival Time':^15}{'Burst Time':^15}{'Waiting Time':^15}{'Turn Around Time':^20}{'Completion Time':^20}")
    print("-" * 100)
    for p in processes:
        print(f"{p.pid:^15}{p.arrival_time:^15}{p.burst_time:^15}{p.waiting_time:^15}{p.turnaround_time:^20}{p.completion_time:^20}")
    print("-" * 100)
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")


def run_process(process, start_time):
    """Print Start Time and Completion Time, scaled down with sleep()."""

    print(f"Process {process.pid} started at time {start_time} (Arrival={process.arrival_time}, Burst={process.burst_time})")
    time.sleep(process.burst_time * 1)  # stops execution for burst_time seconds for the demo
    print(f"Process {process.pid} finished at time {process.completion_time}")


def simulate_execution(order):
    """Simulate execution of processes in the order determined by SJF scheduling using threads."""

    print("\n=== Simulated Execution (SJF Order with Threads) ===")
    threads = []
    for p in order:
        t = threading.Thread(target=run_process, args=(p, p.completion_time - p.burst_time))
        threads.append(t)
        t.start()
        t.join()   # ensure sequential execution in correct order


def main():
    # Asking user to input the number of processes
    num_processes = int(input("\nEnter the number of processes: "))

    # Asking user to input the burst times for the processes
    processes = []     # empty list to store instances of Process
    for i in range(num_processes):
        burst_time = int(input(f"Enter the burst time for process {i+1}: "))
        arrival_time = int(input(f"Enter arrival time for process {i+1}: "))
        processes.append(Process(i+1, burst_time, arrival_time))

    # Calculating, simulating, and displaying SJF Scheduling
    avg_waiting, avg_turnaround, order = calculate_sjf(processes)
    simulate_execution(order)
    display_results(processes, avg_waiting, avg_turnaround)


if __name__ == "__main__":
    main()