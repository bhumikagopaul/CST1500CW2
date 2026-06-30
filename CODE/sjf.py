# Non-Preemptive Shortest Job First (SJF)

import threading
import time
import logging
import pandas as pd
from tabulate import tabulate

from typing import List, Tuple, Optional

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"   # no milliseconds
)

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
                        logging.info(f"Process {p.pid} scheduled (Arrival={p.arrival_time}, Burst={p.burst_time})")
                    else:
                        # If no process has arrived yet, increment time
                        current_time += 1

            # Calculating average waiting time and average turnaround time
            avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
            avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)

            return avg_waiting, avg_turnaround, order
        else:
            logging.warning("No processes provided to calculate average times.")
            return 0, 0, []
    except Exception as e:
        logging.error(f"Error while calling calculate_sjf(): {e}")
        return 0, 0, []


def display_results(processes: List[Process], avg_waiting: float, avg_turnaround: float) -> None:
    """Display Non-Preemptive SJF Scheduling in a table format with averages using Pandas."""

    try:
        data = []   # empty list to store dictionaries representing each process
        for p in processes:
            row = {
                "Process Number": p.pid,
                "Arrival Time": p.arrival_time,
                "Burst Time": p.burst_time,
                "Waiting Time": p.waiting_time,
                "Turnaround Time": p.turnaround_time,
                "Completion Time": p.completion_time
            }
            data.append(row)

        # Creating dataframe
        df = pd.DataFrame(data)

        print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")

        # Printing table with grid lines and centered values
        print(tabulate(data, headers="keys", tablefmt="grid", stralign="center", numalign="center"))

        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")
    except Exception as e:
        logging.error(f"Error while calling display_results(): {e}")


def run_process(process: Process, start_time: int) -> None:
    """Print Start Time and Completion Time, scaled down with sleep()."""

    try:
        print(f"Process {process.pid} started at time {start_time} (Arrival={process.arrival_time}, Burst={process.burst_time})")
        time.sleep(process.burst_time * 1)  # stops execution for burst_time seconds for the demo
        print(f"Process {process.pid} finished at time {process.completion_time}")
        logging.info(f"Process {process.pid} finished at time {process.completion_time}")
    except Exception as e:
        logging.error(f"Error while calling run_process(): {e}")


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
        logging.error(f"Error while calling simulate_execution(): {e}")


def display_gantt_chart(processes: List[Process]) -> None:
    """Display a Gantt chart for the scheduled processes."""

    try:
        print("\n=== Gantt Chart (Non-Preemptive SJF Scheduling) ===\n")

        timeline = ""
        times = "0"
        current = 0

        for p in processes:
            start = p.completion_time - p.burst_time
            finish = p.completion_time
            timeline += f"| P{p.pid} "
            times += f"{' '*(len(timeline)-len(times))}{finish}"
            current = finish

        timeline += "|"
        print(timeline)
        print(times)
    except Exception as e:
        logging.error(f"Error while calling display_gantt_chart(): {e}")


def validate_num_processes(num_input: str) -> Optional[int]:
    """Validate the number of processes entered by the user."""
    try:
        value: int = int(num_input)
        if value <= 0:
            print("Error: Number of processes must be positive.")
            logging.warning(f"Invalid value entered by user: {num_input}")
            return None
        elif value > 50:  # optional cap
            print("Error: Too many processes (maximim 50).")
            logging.warning(f"Invalid value entered by user:{num_input}")
            return None
        else:
            logging.info(f"Valid number of processes entered by user: {num_input}")
            return value
    except ValueError:
        print("Error: Number of processes must be an integer.")
        logging.warning(f"Invalid value entered by user: {num_input}")
        return None
    

def validate_time(time_input: str, allow_zero: bool = False) -> Optional[int]:
    """Validate burst times or arrival times to allow only integers."""

    try:
        value: int = int(time_input)

        if not allow_zero and value <= 0:
            print("Error: Value must be a positive.")
            logging.warning(f"Invalid time entered by user: {time_input}")
            return None
        elif allow_zero and value < 0:
            print("Error: Value must be non-negative.")
            logging.warning(f"Invalid time entered by user: {time_input}")
            return None
        else:
            logging.info(f"Valid time entered by user: {time_input}")
            return value
    except ValueError:
        print(f"Error: Value must be a positive integer.")
        logging.warning("Invalid time entered by user.")
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
        display_gantt_chart(processes)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()