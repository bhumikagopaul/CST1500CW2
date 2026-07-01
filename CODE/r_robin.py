from collections import deque
import pandas as pd  # Connected to print our final grid neatly


class Process:
    """
    Represents an individual program/task inside the Operating System.
    This acts as our custom Process Control Block (PCB).
    """

    def __init__(self, pid: int, burst_time: int, arrival_time: int = 0) -> None:
        self.pid: int = pid
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time

        # Core dynamic state variables
        self.remaining_time: int = burst_time
        self.completion_time: int = 0
        self.turnaround_time: int = 0
        self.waiting_time: int = 0

    def execute(self, time_slice: int) -> None:
        """Simulates CPU execution by reducing the remaining burst time."""
        self.remaining_time -= time_slice

    def is_finished(self) -> bool:
        """Returns True if the process has no work left to do."""
        return self.remaining_time == 0


class RoundRobinScheduler:
    """
    The central CPU engine that manages the ready queue, controls clock cycles,
    and runs the preemption loop.
    """

    def __init__(self, time_quantum: int) -> None:
        self.time_quantum: int = time_quantum
        self.ready_queue: deque = deque()
        self.clock: int = 0

    def schedule(self, processes: list[Process]) -> None:
        """Executes the Round Robin scheduling logic on a list of Process objects."""

        # Load all processes into the ready queue initially
        # (Assuming baseline arrival time = 0 for now)
        for p in processes:
            self.ready_queue.append(p)

        print(
            f"--- Execution Timeline (Time Quantum = {self.time_quantum}) ---")

        # Core Scheduler Loop
        while len(self.ready_queue) > 0:
            # Dispatch next process from the front of the queue
            current_process = self.ready_queue.popleft()

            # Calculate slice: min(Quantum, Remaining)
            slice_time = min(self.time_quantum, current_process.remaining_time)

            print(
                f"Clock {self.clock:2d} -> {self.clock + slice_time:2d}: Process {current_process.pid} runs")

            # Execute the process using its own internal object method
            current_process.execute(slice_time)
            self.clock += slice_time

            # Preemption state handling
            if current_process.is_finished():
                # Record metrics directly onto the object attributes
                current_process.completion_time = self.clock
                current_process.turnaround_time = current_process.completion_time - \
                    current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - \
                    current_process.burst_time
            else:
                # Still has work left! Append back to the tail of the queue
                self.ready_queue.append(current_process)


def display_results(processes: list[Process]) -> None:
    """Formats and prints execution results using pure Python string formatting."""
    print("\n" + "="*77)
    print(f"{'OOP ROUND ROBIN SIMULATION RESULTS':^77}")
    print("="*77)

    # 1. Print Header Row with explicit column spacing
    header = f"| {'Process ID':<10} | {'Arrival Time':<12} | {'Burst Time':<10} | {'Completion':<10} | {'Turnaround':<10} | {'Waiting':<8} |"
    print(header)
    print("-" * len(header))

    total_wt = 0
    total_tat = 0

    # 2. Loop through each process object and format its attributes into a row
    for p in processes:
        row = (
            f"| {p.pid:<10} | "
            f"{p.arrival_time:<12} | "
            f"{p.burst_time:<10} | "
            f"{p.completion_time:<10} | "
            f"{p.turnaround_time:<10} | "
            f"{p.waiting_time:<8} |"
        )
        print(row)

        total_tat += p.turnaround_time
        total_wt += p.waiting_time

    print("="*77)

    # 3. Compute and display the missing averages required by your specification sheet
    num_proc = len(processes)
    avg_tat = total_tat / num_proc if num_proc > 0 else 0
    avg_wt = total_wt / num_proc if num_proc > 0 else 0

    print(f"Average Turnaround Time : {avg_tat:.2f}")
    print(f"Average Waiting Time    : {avg_wt:.2f}")
    print("="*77)


# --- Main Driver Script Execution ---
if __name__ == "__main__":
    # Create instances of our Process objects exactly from the baseline spec sheet
    process_list = [
        Process(pid=1, burst_time=5),
        Process(pid=2, burst_time=3),
        Process(pid=3, burst_time=7),
        Process(pid=4, burst_time=2)
    ]

    # Initialize our Scheduler object with a Time Quantum of 2
    rr_engine = RoundRobinScheduler(time_quantum=2)

    # Run the engine
    rr_engine.schedule(process_list)

    # Display performance metrics
    display_results(process_list)