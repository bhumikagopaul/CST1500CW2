from collections import deque
import threading
import time
import pandas as pd


class Process(threading.Thread):
    """
    Represents an individual process that runs in its own thread
    Acts as an active process control block to keep the execution values.
    """

    def __init__(self, pid, burst_time, arrival_time=0):
        super().__init__()
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time

        # Variables used to track turnaround, waiting and completion times.
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

        # Thread signals mathc executions with the main scheduler
        # A trigger to let the following thread rin
        self.resume_signal = threading.Event()
        # A trigger for when the thread is done with a tick
        self.pause_signal = threading.Event()
        self.running = True

    def run(self):
        """The main life cycle loop of an inidividual process thread."""
        while self.remaining_time > 0 and self.running:
            # Wait until the program tells that trhread to resume
            self.resume_signal.wait()
            self.resume_signal.clear()

            # To simulate a clock tick
            time.sleep(0.01)
            self.remaining_time -= 1

            # Tell the main scheduler thread this burts cycle is done
            self.pause_signal.set()


class RoundRobin:
    """
    The main scheduler controller that manages the system clock,
    the ready queue and process preemption.
    """

    def __init__(self, time_quantum: int):
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.clock = 0

    def schedule(self, processes: list[Process]) -> None:
        """
        Executesd the round robin simulatio on the process threads.
        Handle arrival times.
        """
        # Sort processes by their arrival time firs to make sure they are in chronological order
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        n = len(sorted_processes)
        # Index to track which process which process has arrived
        p_index = 0
        # To track how many threads are done
        completed = 0

        # Start background threads so that they wwait for an execution signal
        for p in sorted_processes:
            p.start()

        print(
            f"\n--- Threaded Execution Timeline (Time Quantum = {self.time_quantum}s) ---")

        # Simulated loop until all the processes are done
        while completed < n:
            # Add any process that arrives at or before the current clock to the queue
            while p_index < n and sorted_processes[p_index].arrival_time <= self.clock:
                self.ready_queue.append(sorted_processes[p_index])
                p_index += 1
            # If the queue is empty but there are still tasks left, we advance the clock
            if not self.ready_queue:
                print(
                    f"Clock {self.clock:2d}: CPU Idle (Waiting for processes)...")
                time.sleep(0.01)
                self.clock += 1
                continue

            # Send the next process thread from the front of the ready queue
            current_process = self.ready_queue.popleft()

            # Find the time execution window
            current_slice = min(self.time_quantum,
                                current_process.remaining_time)
            print(
                f"Clock {self.clock:2d} -> {self.clock + current_slice:2d}: Process {current_process.pid} running on Thread ID: {current_process.name}")

            # Run the process thread step by step for the duration of it's clock time
            for _ in range(current_slice):
                # Wake up the process thread
                current_process.resume_signal.set()

                # Wait for the process thread to finish its single task
                current_process.pause_signal.wait()
                current_process.pause_signal.clear()

                # Increment system time frame
                self.clock += 1

                # Get the background arrivals that happened for this specific execution second
                while p_index < n and sorted_processes[p_index].arrival_time <= self.clock:
                    self.ready_queue.append(sorted_processes[p_index])
                    p_index += 1

            # Check if the process is done
            if current_process.remaining_time == 0:
                # Calculate the values and sotre them in the process object
                current_process.completion_time = self.clock
                current_process.turnaround_time = current_process.completion_time - \
                    current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - \
                    current_process.burst_time
                completed += 1
                # Terminate the completed thread
                current_process.join()
            else:
                # If it's a prempted process then the worker still has work left so we need
                # to append back to the tail of the ready queue
                self.ready_queue.append(current_process)


def display_results(processes: list[Process]) -> None:
    """Format and print the fina values using a Pandas."""
    print()
    print("--------ROUND ROBIN RESULTS--------")
    print()
    print()

    # Collect the attributes into a dictionary format for pandas
    data = []
    for p in processes:
        data.append({
            "Process ID": p.pid,
            "Arrival Time": p.arrival_time,
            "Burst Time": p.burst_time,
            "Completion Time": p.completion_time,
            "Turnaround Time": p.turnaround_time,
            "Waiting Time": p.waiting_time
        })

    # Create a DataFrame and sort by process ID
    df = pd.DataFrame(data)
    df = df.sort_values(by="Process ID").reset_index(drop=True)

    # Output the table with the data
    print(df.to_string(index=False))

    # Calcualte the performance averages using Pandas
    avg_tat = df["Turnaround Time"].mean()
    avg_wt = df["Waiting Time"].mean()

    print(f"Average Turnaround Time : {avg_tat:.2f}")
    print(f"Average Waiting Time    : {avg_wt:.2f}")


# Main and Validation programs to ensure no crash happens from user input
if __name__ == "__main__":

    # Input validation to ensure the user inputs only positive integers greater than zero
    def get_positive_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print(
                        "[Invalid Input] Value must be greater than zero. Try again.")
                    continue
                return value
            except ValueError:
                print("[Invalid Input] Please enter a valid integer numeric value.")

    # Input validation to ensur ethe user inputs only positive integers greater or equal to zero
    def get_non_negative_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value < 0:
                    print("[Invalid Input] Value cannot be negative. Try again.")
                    continue
                return value
            except ValueError:
                print("[Invalid Input] Please enter a valid integer numeric value.")

    print("--------ROUND ROBIN SET UP--------")
    print()
    print()

    # User input using CLI doe custom values
    use_custom = input(
        "Use custom interactive input? (y/n, default 'n' uses spec sheet values): ").strip().lower() == 'y'
    process_list = []

    if use_custom:
        tq = get_positive_int("Enter Time Quantum (must be > 0): ")
        num_processes = get_positive_int(
            "Enter total number of processes (must be > 0): ")

        for i in range(num_processes):
            print(f"\n--- Process Configuration {i+1}/{num_processes} ---")

            # Input validation to ennsure that the process ID isn't left empty
            pid = ""
            while not pid.strip():
                pid = input("Enter Process ID/Name: ")
                if not pid.strip():
                    print("[Invalid Input] Process ID cannot be empty.")

            arrival = get_non_negative_int(
                f"Enter Arrival Time for Process {pid} (must be >= 0): ")
            burst = get_positive_int(
                f"Enter Burst Time for Process {pid} (must be > 0): ")

            process_list.append(Process(pid, burst, arrival))
    else:
        # automatically input values directly if user doesnt want to input custom values
        process_list = [
            Process(pid=1, burst_time=5, arrival_time=0),
            Process(pid=2, burst_time=3, arrival_time=0),
            Process(pid=3, burst_time=7, arrival_time=0),
            Process(pid=4, burst_time=2, arrival_time=0)
        ]
        # set time quantum to 2 seconds
        tq = 2
        print("\n-> Running engine with assignment specification baseline values.")

    # Set up the scheduler
    scheduler = RoundRobin(time_quantum=tq)
    # Run the simulation
    scheduler.schedule(process_list)
    # Print the table
    display_results(process_list)
