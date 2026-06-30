# Non-Preemptive Shortest Job First (SJF)

import threading, time

from typing import List, Tuple, Optional

# Storing processes as objects rather than tuples
class Process:
    def __init__(self, pid: int, burst_time: int, arrival_time: int) -> None:   # __init__ = initialiser, runs automatically when a new object is created and sets its attributes
        self.pid: int = pid   # unique
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0


def calculate_sjf(processes: List[Process]) -> Tuple[float, float, List[Process]]:
    """Calculate and return Average Waiting Time and Average Turn Around Time for SJF Scheduling. It also returns the list order."""

    completed: int = 0      # number of processes completed
    current_time: int = 0   # current time in the simulation
    order: List[Process] = []         # list to store the order of execution of processes

    try:
        if len(processes) != 0:
            # Continue until all processes are completed
            while completed < len(processes):
                    # Selecting processes that have arrived and not yet completed
                    available: List[Process] = [p for p in processes if (p.arrival_time <= current_time) and (p.completion_time == 0)]

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
    except Exception as e:
        print(f"Error while calculating average times: {e}")
        return 0, 0, []


def display_results(processes: List[Process], avg_waiting: float, avg_turnaround: float) -> None:
    """Display Non-Preemptive SJF Scheduling in a table formatwith averages."""

    try:
        print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")
        print(f"{'Process Number':^15}{'Arrival Time':^15}{'Burst Time':^15}{'Waiting Time':^15}{'Turn Around Time':^20}{'Completion Time':^20}")
        print("-" * 100)
        for p in processes:
            print(f"{p.pid:^15}{p.arrival_time:^15}{p.burst_time:^15}{p.waiting_time:^15}{p.turnaround_time:^20}{p.completion_time:^20}")
        print("-" * 100)
        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")
    except Exception as e:
        print(f"Error while displaying results: {e}")


def run_process(process: Process, start_time: int) -> None:
    """Print Start Time and Completion Time, scaled down with sleep()."""

    try:
        print(f"Process {process.pid} started at time {start_time} (Arrival={process.arrival_time}, Burst={process.burst_time})")
        time.sleep(process.burst_time * 1)  # stops execution for burst_time seconds for the demo
        print(f"Process {process.pid} finished at time {process.completion_time}")
    except Exception as e:
        print(f"Error running process {process.pid}: {e}")


def simulate_execution(order: List[Process]) -> None:
    """Simulate execution of processes in the order determined by SJF scheduling using threads."""

    try:
        print("\n=== Simulated Execution (SJF Order with Threads) ===")
        threads: List[threading.Thread] = []
        for p in order:
            t = threading.Thread(target=run_process, args=(p, p.completion_time - p.burst_time))
            threads.append(t)
            t.start()
            t.join()   # ensure sequential execution in correct order
    except Exception as e:
        print(f"Error while simulating execution: {e}")

def validate_num_processes(num_input: str) -> Optional[int]:
    """Validate the number of processes entered by the user."""
    try:
        value: int = int(num_input)
        if value <= 0:
            print("Error: Number of processes must be positive.")
            return None
        elif value > 50:  # optional cap
            print("Error: Too many processes (maximim 50).")
            return None
        else:
            return value
    except ValueError:
        print("Error: Number of processes must be an integer.")
        return None
    
def validate_time(time_input: str, allow_zero: bool = False) -> Optional[int]:
    """Validate burst times or arrival times to allow only integers."""

    try:
        value: int = int(time_input)

        if not allow_zero and value <= 0:
            print("Error: Value must be a positive.")
            return None
        elif allow_zero and value < 0:
            print("Error: Value must be non-negative.")
            return None
        else:
            return value
    except ValueError:
        print("Error: Value must be a positive integer.")
        return None



def main() -> None:
    try:
        # Asking user to input the number of processes
        num_processes: Optional[int] = None
        while num_processes is None:
            num_processes = validate_num_processes(input("\nEnter the number of processes: "))

        # Asking user to input the burst times for the processes
        processes: List[Process] = []     # empty list to store instances of Process
        for i in range(num_processes):
            burst_time: Optional[int] = None
            while burst_time is None:
                burst_time = validate_time(input(f"Enter the burst time for process {i+1}: "))

            arrival_time: Optional[int] = None
            while arrival_time is None:
                arrival_time = validate_time(input(f"Enter arrival time for process {i+1}: "), allow_zero=True)

            processes.append(Process(i+1, burst_time, arrival_time))

        # Calculating, simulating, and displaying SJF Scheduling
        avg_waiting, avg_turnaround, order = calculate_sjf(processes)
        simulate_execution(order)
        display_results(processes, avg_waiting, avg_turnaround)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()