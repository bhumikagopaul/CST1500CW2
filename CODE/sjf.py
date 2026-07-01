# Non-Preemptive Shortest Job First (SJF)

import threading         # used to simulate process execution
import time              # used for sleep() to simulate burst times
import logging           # used for structured info/error messages
import pandas as pd      # used for display of results in a grid format
import streamlit as st   # used to create a web app interface for user input and output display

from typing import List, Tuple, Optional  # used for type hints to improve understanding of code

# Configuring logging
logging.basicConfig(
    level=logging.INFO,   # minimum level set as INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"   # no milliseconds
)

# Storing processes as objects rather than tuples
class Process:
    def __init__(self, pid: int, burst_time: int, arrival_time: int) -> None:   # __init__ = initialiser, runs automatically when a new object is created and sets its attributes
        self.pid: int = pid   # unique process ID
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0


##################### FUNCTIONS COMMON TO BOTH CLI AND STREAMLIT #####################

def calculate_sjf(processes: List[Process]) -> Tuple[float, float, List[Process]]:
    """Calculate and return Average Waiting Time and Average Turn Around Time for SJF Scheduling. It also returns the list order."""

    # Initialising counters
    completed: int = 0                # number of processes completed
    current_time: int = 0             # current time in the simulation
    order: List[Process] = []         # list to store the order of execution of processes

    try:
        if len(processes) != 0:  # if list is not empty
            # Continue until all processes are completed
            while completed < len(processes):
                    # Filtering to select processes that have arrived and not yet completed
                    available: List[Process] = [p for p in processes if (p.arrival_time <= current_time) and (p.completion_time == 0)]

                    if available:
                        p = min(available, key=lambda x: x.burst_time)          # Picking process with shortest burst time
                        # Updating the waiting, completion, and turnaround times of the process
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


def create_dataframe_processes(processes: List[Process]) -> pd.DataFrame:
    """Create a Pandas DataFrame where each row represents a process."""

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
            data.append(row)  # add process 'p' to the list 'data'

        # Creating dataframe
        df = pd.DataFrame(data)
        logging.info("DataFrame created for processes.")
        return df
    except Exception as e:
        logging.error(f"Error while calling create_dataframe_processes(): {e}")


##################### CLI FUNCTIONS #####################

# Validation functions
def validate_num_processes_cli(num_input: str) -> Optional[int]:
    """Validate the number of processes entered by the user (CLI Version)."""
    try:
        value: int = int(num_input)
        if value <= 0 or value > 50:
            print("Error: Number of processes must be a positive integer. (maximum 50).")
            return None
        else:
            return value
    except ValueError:
        print("Error: Number of processes must be an integer.")
        logging.warning(f"Invalid value entered by user: {num_input}")
        return None


def validate_time_cli(time_input: str, allow_zero: bool = False) -> Optional[int]:
    """Validate burst times or arrival times to allow only integers (CLI Version)."""

    try:
        value: int = int(time_input)

        if (not allow_zero and value <= 0) or (allow_zero and value < 0):
            print("Error: Value must be a positive integer.")
            return None
        else:
            return value
    except ValueError:
        print(f"Error: Value must be a positive integer.")
        logging.warning("Invalid time entered by user.")
        return None


def display_results_cli(df: pd.DataFrame, avg_waiting: float, avg_turnaround: float) -> None:
    """Display Non-Preemptive SJF Scheduling in a table format using Pandas DataFrame (CLI Version)."""

    try:
        print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")

        # Showing the results in a grid format
        print(df.to_markdown(tablefmt="grid"))

        # Displaying average waiting time and average turnaround time
        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")
    except Exception as e:
        logging.error(f"Error while calling display_results_cli(): {e}")


def run_process(process: Process, start_time: int) -> None:
    """Print Start Time and Completion Time, scaled down with time.sleep()."""

    try:
        print(f"Process {process.pid} started at time {start_time} (Arrival={process.arrival_time}, Burst={process.burst_time})")
        time.sleep(process.burst_time * 1)  # stops execution for burst_time seconds for the demo
        print(f"Process {process.pid} finished at time {process.completion_time}")
        logging.info(f"Process {process.pid} finished at time {process.completion_time}")
    except Exception as e:
        logging.error(f"Error while calling run_process(): {e}")


def simulate_execution_cli(order: List[Process]) -> None:
    """Simulate execution of processes in the order determined by SJF scheduling using threads (CLI Version)."""

    try:
        print("\n=== Simulated Execution (SJF Order with Threads) ===")
        threads: List[threading.Thread] = []
        for p in order:
            t = threading.Thread(target=run_process, args=(p, p.completion_time - p.burst_time))  # create thread
            threads.append(t)
            t.start()  # start thread
            logging.info(f"CLI: Process {p.pid} started at {p.completion_time - p.burst_time}")
            t.join()   # join thread immediately to ensure sequential execution in correct order
            logging.info(f"CLI: Process {p.pid} finished at {p.completion_time}")
    except Exception as e:
        logging.error(f"Error while calling simulate_execution_cli(): {e}")


def display_gantt_chart_cli(processes: List[Process]) -> None:
    """Display a Gantt chart for the scheduled processes (CLI Version)."""

    try:
        print("\n=== Gantt Chart (Non-Preemptive SJF Scheduling) ===\n")

        # Initialising strings to be displayed
        timeline = ""   # to store seperation bars and process names to make up the grid
        times = "0"     # timestamps below the grid

        for p in processes:
            # Appending a bar followed by the process name to the string timeline
            timeline += f"| P{p.pid} "  
            # Appending the string times with the number of spaces equal to the process name followed by the completion time
            times += f"{' '*(len(timeline)-len(times))}{p.completion_time}"   

        timeline += "|"  # append the ending bar

        print(timeline)
        print(times)
    except Exception as e:
        logging.error(f"Error while calling display_gantt_chart_cli(): {e}")


def main_cli() -> None:
    try:
        # Asking user to input the number of processes
        num_processes: Optional[int] = None
        while num_processes is None:  # keep asking until a valid value is entered
            num_processes = validate_num_processes_cli(input("\nEnter the number of processes: "))

        # Asking user to input the burst times for the processes
        processes: List[Process] = []     # empty list to store instances of Process
        for i in range(num_processes):
            burst_time: Optional[int] = None
            while burst_time is None:  # keep asking until a valid value is entered
                burst_time = validate_time_cli(input(f"Enter the burst time for process {i+1}: "))

            arrival_time: Optional[int] = None
            while arrival_time is None:  # keep asking until a valid value is entered
                arrival_time = validate_time_cli(input(f"Enter arrival time for process {i+1}: "), allow_zero=True)

            processes.append(Process(i+1, burst_time, arrival_time))  # adding the current process object to the list of processes

        # Calculating, simulating, and displaying SJF Scheduling
        avg_waiting, avg_turnaround, order = calculate_sjf(processes)
        simulate_execution_cli(order)
        display_results_cli(create_dataframe_processes(processes), avg_waiting, avg_turnaround)
        display_gantt_chart_cli(processes)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")


##################### STREAMLIT FUNCTIONS #####################

# Validation functions
def validate_num_processes_streamlit(num_input: str) -> Optional[int]:
    """Validate the number of processes entered by the user (Streamlit Version)."""
    try:
        value: int = int(num_input)
        if value <= 0 or value > 50:
            st.warning("Error: Number of processes must be a positive integer. (maximum 50).")
            return None
        else:
            return value
    except ValueError:
        st.warning("Error: Number of processes must be an integer.")
        logging.warning(f"Invalid value entered by user: {num_input}")
        return None
    

def validate_time_streamlit(time_input: str, allow_zero: bool = False) -> Optional[int]:
    """Validate burst times or arrival times to allow only integers (Streamlit Version)."""

    try:
        value: int = int(time_input)

        if (not allow_zero and value <= 0) or (allow_zero and value < 0):
            st.warning("Error: Value must be a positive integer.")
            return None
        else:
            return value
    except ValueError:
        st.warning(f"Error: Value must be a positive integer.")
        logging.warning("Invalid time entered by user.")
        return None


def display_results_streamlit(df: pd.DataFrame) -> None:
    """Display Non-Preemptive SJF Scheduling in a table format using Pandas DataFrame (Streamlit Version)."""

    try:
        # Calculating and displaying results if times for all processes are valid and the user clicks the "Run SJF Scheduling" button
        if len(processes) == num_processes and st.button("Run SJF Scheduling"):
            avg_waiting, avg_turnaround, order = calculate_sjf(processes)

            st.subheader("Non-Preemptive Shortest Job First (SJF) Scheduling Results")
            st.dataframe(df)

            st.write(f"**Average Waiting Time:** {avg_waiting:.2f}")
            st.write(f"**Average Turnaround Time:** {avg_turnaround:.2f}")

            st.session_state['order'] = order  # store order in session_state so it persists across reruns
            logging.info("Streamlit: SJF scheduling run completed.")
    except Exception as e:
        logging.error(f"Error while calling display_results_streamlit(): {e}")
        return []


def simulate_execution_streamlit(order: List[Process]) -> None:
    """Simulate execution of processes in the order determined by SJF scheduling using threads (Streamlit Version)."""

    try:
        st.subheader("Simulated Execution")
        log_area = st.empty()  # placeholder for progressive updates
        messages = ""

        for p in order:
            messages += f"\nProcess {p.pid} started at time {p.completion_time - p.burst_time} (Arrival={p.arrival_time}, Burst={p.burst_time})"
            logging.info(f"Streamlit: Process {p.pid} started at {p.completion_time - p.burst_time}")
            log_area.text(messages)
            time.sleep(p.burst_time)

            messages += f"\nProcess {p.pid} finished at time {p.completion_time}"
            logging.info(f"Streamlit: Process {p.pid} finished at {p.completion_time}")
            log_area.text(messages)
    except Exception as e:
        logging.error(f"Error while calling simulate_execution_streamlit(): {e}")


# STREAMLIT UI

# Initialise session_state
if "order" not in st.session_state:
    st.session_state["order"] = None

st.title("Non-Preemptive Shortest Job First (SJF) Scheduling")

# Asking for and validating number of processes
num_processes = st.text_input("Enter number of processes")
if num_processes:
    num_processes = validate_num_processes_streamlit(num_processes)
else:
    num_processes = None

if num_processes:
    st.warning(f"Please enter valid burst and arrival times.")
    processes = []   # initialising empty list to store processes
    for i in range(num_processes):
        # Asking for and validating burst time for each process
        burst_time = st.text_input(f"Enter burst time for process {i+1}")
        if burst_time:
            burst_time = validate_time_streamlit(burst_time)
        else:
            burst_time = None
        # Asking for and validating arrival time for each process
        arrival_time = st.text_input(f"Enter arrival time for process {i+1}")
        if arrival_time:
            arrival_time = validate_time_streamlit(arrival_time)
        else:
            arrival_time = None

        # Adding the process to the list if both times given are valid
        if burst_time is not None and arrival_time is not None:
            processes.append(Process(i+1, burst_time, arrival_time))

    display_results_streamlit(create_dataframe_processes(processes))

    # Separate button for simulation
    if "order" in st.session_state and st.button("Simulate Execution"):
        simulate_execution_streamlit(st.session_state["order"])