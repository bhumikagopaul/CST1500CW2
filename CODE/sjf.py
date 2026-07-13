# Non-Preemptive Shortest Job First (SJF)

import threading                  # used to simulate process execution
import time                       # used for sleep() to simulate burst times
import logging                    # used for structured info/error messages
import os                         # used to be able to run the Streamlit web app from the CLI menu

import pandas as pd               # used for display of results in a grid format
import matplotlib.pyplot as plt   # used for Grantt chart visualisation
import streamlit as st            # used for the Streamlit web app

from typing import List, Tuple, Optional  # used for type hints to improve understanding of code

# Configuring logging
logging.basicConfig(
    level=logging.INFO,   # minimum level set as INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"   # timestamp with no milliseconds
)

# Storing processes as objects rather than tuples
class Process:
    """Represents a process with its attributes for SJF Scheduling."""
    def __init__(self, pid: int, burst_time: int, arrival_time: int) -> None:   # __init__ = initialiser, runs automatically when a new object is created and sets its attributes
        self.pid: int = pid   # unique process ID
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        # Initialising the below to 0. They are calculated during SJF scheduling. 
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0


################################################### FUNCTIONS COMMON TO BOTH CLI AND STREAMLIT ########################################################

def validate_num_processes(num_input: str) -> tuple[Optional[int], Optional[str]]:
    """Validate the number of processes entered by the user. Returns a tuple in the format (value, message)."""

    try:
        value: int = int(num_input)
        if value <= 0 or value > 50:
            return None, "Error: Number of processes must be a positive integer. (Max 50)."
        return value, None
    except ValueError:   # to handle non-numeric input
        return None, "Error: Number of processes must be a positive integer. (Max 50)."


def validate_time(num_input: str, allow_zero: bool = False) -> tuple[Optional[int], Optional[str]]:
    """Validate the burst time and arrival time entered by the user. Returns a tuple in the format (value, message)."""

    try:
        value: int = int(num_input)
        # validating burst time, must be > 0
        if (not allow_zero and value <= 0):      
            return None, "Error: Time must be a positive integer."
        # validating arrival time, must be >= 0
        if (allow_zero and value < 0):         
            return None, "Error: Time must be 0 or a positive integer." 
        return value, None
    except ValueError:   # to handle non-numeric input
        return None, "Error: Time must be an integer."


def calculate_sjf(processes: List[Process]) -> Tuple[float, float, List[Process]]:
    """Calculate and return Average Waiting Time and Average Turn Around Time for SJF Scheduling. It also returns the list ordered_processes."""

    # If no processes provided
    if not processes:
        logging.warning("No processes provided.")
        return 0, 0, []
    
    # Resetting processes to prevent reuse bugs
    for p in processes:
        p.waiting_time = 0
        p.turnaround_time = 0
        p.completion_time = 0

    # Initialising counters
    completed: int = 0                        # number of processes completed
    current_time: int = 0                     # current time in the simulation
    ordered_processes: List[Process] = []     # list to store the processes in the order to be executed

    try:
        # Looping until all processes are scheduled and completed
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
                    ordered_processes.append(p)                             # Adding process to ordered_processes
                    completed += 1
                else:
                    # If no process has arrived yet, increment time
                    current_time += 1

        # Calculating average waiting time and average turnaround time
        avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
        avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)

        # Returning average waiting time, average turnaround time and the ordered list
        return avg_waiting, avg_turnaround, ordered_processes
    except Exception as e:
        logging.error(f"Error while calling calculate_sjf(): {e}")
        return 0, 0, []


def create_dataframe_processes(processes: List[Process]) -> pd.DataFrame:
    """Create a Pandas DataFrame using the list 'processes' where each row represents a process."""

    try:
        data: List[dict[str, int]] = []   # empty list to store dictionaries representing each process
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
        df = pd.DataFrame(data).reset_index(drop=True)  # dropping default index
        logging.info("DataFrame created for processes.")

        # Returning the dataframe
        return df
    except Exception as e:
        logging.error(f"Error while calling create_dataframe_processes(): {e}")
        return pd.DataFrame()  # returning empty DataFrame on error


########################################################### CLI ONLY FUNCTIONS ####################################################################

def display_results_cli(df: pd.DataFrame, avg_waiting: float, avg_turnaround: float) -> None:
    """Display Non-Preemptive SJF Scheduling in a table format using Pandas DataFrame (CLI Version)."""

    try:
        print("\n=== Non-Preemptive Shortest Job First (SJF) Scheduling Results ===\n")

        # Showing the results in a grid format
        print(df.to_markdown(
            index=False,                              # hiding the column index
            tablefmt="grid",                          # grid format
            colalign=["center"] * len(df.columns)     # centering all columns
            ))

        # Displaying average waiting time and average turnaround time
        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}\n")
    except Exception as e:
        logging.error(f"Error while calling display_results_cli(): {e}")


def run_process(process: Process, start_time: int) -> None:
    """Print Start Time and Completion Time using time.sleep() to simulate execution."""

    try:
        # Printing message when process starts
        print(f"Process {process.pid} started at time {start_time} (Arrival={process.arrival_time}, Burst={process.burst_time})")
        # Stops execution for burst_time seconds to simulate the process running
        time.sleep(process.burst_time)  
        # Printing message when process finishes
        print(f"Process {process.pid} finished at time {process.completion_time}")
    except Exception as e:
        logging.error(f"Error while calling run_process(): {e}")


def simulate_execution_cli(ordered_processes: List[Process]) -> None:
    """Simulate execution of processes in the order determined by SJF scheduling using threads (CLI Version)."""

    try:
        print("\n=== Simulated Execution (SJF ordered with Threads) ===")
        # Looping through the ordered process list
        for p in ordered_processes:
            # Creating a new thread which runs the function run_process()
            t = threading.Thread(target=run_process, args=(p, p.completion_time - p.burst_time))
            # Starting the thread, which begins executing run_process
            t.start() 
            # Waiting for the current thread to finish before moving to the next process in the list
            # join thread immediately to ensure sequential execution in correct order
            t.join()   
    except Exception as e:
        logging.error(f"Error while calling simulate_execution_cli(): {e}")


def display_gantt_chart_cli(ordered_processes: List[Process]) -> None:
    """Display a Gantt chart for the scheduled processes (CLI Version)."""

    try:
        print("\n=== Gantt Chart (Non-Preemptive SJF Scheduling) ===\n")

        # Initialising strings to be output for the Gantt chart
        timeline: str = ""   # will hold the ASCII bars and process labels
        times: str = "0"     # will hold the timeline values, starting with 0

        for p in ordered_processes: # iterating through each process
            start_time: int = p.completion_time - p.burst_time
            bar: str = "-" * p.burst_time                         # Creating a bar proportional to burst time
            timeline += f"|{bar}P{p.pid}{bar}|"                   # Appending the bar and the process label to the string 'timeline'
            spacing: int = len(timeline) - len(times)             # Calculating number of spaces needed to align the completion time
            times += " " * spacing + str(p.completion_time)       # Appending the spaces followed by the completion time to the string 'times'

        # Printing the two strings making up the Gantt chart
        print(timeline)
        print(times)
    except Exception as e:
        logging.error(f"Error while calling display_gantt_chart_cli(): {e}")


def main_cli() -> None:
    try:
        # Asking user to input the number of processes
        num_processes: Optional[int] = None
        while num_processes is None:  # keep asking until a valid value is entered
            value, message = validate_num_processes(input("\nEnter the number of processes: "))
            if value is not None:
                num_processes = value
            else:
                print(message)

        # Asking user to input the burst time for the process
        processes: List[Process] = []     # empty list to store instances of Process
        for i in range(num_processes):
            burst_time: Optional[int] = None
            while burst_time is None:  # keep asking until a valid value is entered
                value, message = validate_time(input(f"Enter the burst time for process {i+1}: "))
                if value is not None:
                    burst_time = value
                else:
                    print(message)

            # Asking user to input the arrival time for the process
            arrival_time: Optional[int] = None
            while arrival_time is None:  # keep asking until a valid value is entered
                value, message = validate_time(input(f"Enter arrival time for process {i+1}: "),allow_zero=True)
                if value is not None:
                    arrival_time = value
                else:
                    print(message)

            processes.append(Process(i+1, burst_time, arrival_time))  # adding the current process object to the list of processes

        # Calculating, simulating, and displaying SJF Scheduling
        avg_waiting, avg_turnaround, ordered_processes = calculate_sjf(processes)
        simulate_execution_cli(ordered_processes)
        display_results_cli(create_dataframe_processes(processes), avg_waiting, avg_turnaround)
        display_gantt_chart_cli(ordered_processes)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")


###################################################### STREAMLIT FUNCTIONS ######################################################

def display_results_streamlit() -> None:
    """Display Non-Preemptive SJF Scheduling in a table format using Pandas DataFrame (Streamlit Version)."""

    try:
        # Retrieving the dataframe and average times from session_state
        df = st.session_state["df"]
        avg_waiting = st.session_state["avg_waiting"]
        avg_turnaround = st.session_state["avg_turnaround"]

        # Displaying results in Streamlit
        st.subheader("SJF Results")

        # Converting the dataframe to html so that the styling actually renders in Streamlit
        html_table = df.to_html(index=False, classes="sjf-table", border=0)

        # Injecting the CSS styling
        st.markdown("""
        <style>
        .sjf-table {
            width: 100%;
            border-collapse: collapse;
            font-family: sans-serif;
        }

        .sjf-table th {
            background-color: #1565C0;
            color: white;
            padding: 10px;
            text-align: center;
        }

        .sjf-table td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }

        .sjf-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        </style>
        """, unsafe_allow_html=True)

        # Displaying the table
        st.markdown(html_table, unsafe_allow_html=True)

        # Showing average times to 2 decimal places in 2 columns
        col1, col2 = st.columns(2)
        col1.metric("Average Waiting Time", f"{avg_waiting:.2f}")
        col2.metric("Average Turnaround Time", f"{avg_turnaround:.2f}")

        logging.info("Streamlit: SJF scheduling run completed.")
    except Exception as e:
        logging.error(f"Error while calling display_results_streamlit(): {e}")


def simulate_execution_streamlit(ordered_processes: List[Process]) -> None:
    """Simulate execution of processes in the order determined by SJF scheduling using threads (Streamlit Version)."""

    try:
        st.subheader("Simulated Execution")

        # Initialising variables
        log_area = st.empty()  # placeholder for dynamic updates
        messages: str = ""     # string of start and finish messages

        # looping through the ordered list
        for p in ordered_processes:
            # Showing when the process starts
            start_time = p.completion_time - p.burst_time
            messages += (
                f"<span style='color:green;'>"
                f"Process {p.pid} started at time {start_time}"
                "</span><br>"
            )
            log_area.markdown(messages, unsafe_allow_html=True)  # updating placeholder with updated string

            time.sleep(p.burst_time)   # simulate burst time

            # Showing when the process finishes
            messages += (
                f"<span style='color:green;'>"
                f"Process {p.pid} finished at time {p.completion_time}"
                "</span><br>"
            )
            log_area.markdown(messages, unsafe_allow_html=True)
        logging.info("Simulated execution completed.")
    except Exception as e:
        logging.error(f"Error while calling simulate_execution_streamlit(): {e}")


def display_gantt_chart_streamlit(ordered_processes: List[Process]) -> None:
    """Display a Gantt chart for the scheduled processes (Streamlit Version)."""

    # Initialising the list of colours to be used for the horizontal bars
    colors: List[str] = ["#1976D2", "#43A047", "#FB8C00", "#8E24AA", "#E53935", "#00897B", "#6D4C41"]

    try:
        st.subheader("Gantt Chart")

        # Preparing data for Gantt chart
        fig, ax = plt.subplots(figsize=(8, 4))                # creating a figure and axis with size 8x4 inches
        for i, p in enumerate(ordered_processes):             # iterating over each process
            start_time = p.completion_time - p.burst_time
            ax.barh(y=f"P{p.pid}",                  # horizontal bar for each process, label row with "P" followed by process ID
                    width=p.burst_time,             # the horizontal bar's length = burst time
                    left=start_time,                # horizontal bar starts at the process start time
                    height=0.5,                     # thickness of horizontal bar
                    align="center",                 # centers the horizontal bar vertically
                    color=colors[i % len(colors)],  # reusing colors if there are a lot of processes
                    edgecolor="black"
                    )
            ax.text(start_time + p.burst_time/2,  # label the horizontal bar at the middle
                    i,                            # the vertical position of the label text
                    f"P{p.pid}",                  # the label text
                    ha="center",                  # centered horizontally
                    va="center",                  # centered vertically
                    color="white"                 # label text color is white
                    )

        # Configuring Gantt chart
        ax.set_xlabel("Time")                       # x-axis label
        ax.set_ylabel("Processes")                  # y-axis label
        ax.set_title("SJF Scheduling Gantt Chart")  # title of chart
        ax.grid(True,                               # show grid lines
                axis="x",                           # show grid lines only on x-axis
                linestyle="--",                     # grid lines made up of dashes --
                alpha=0.7                           # transparency of grid lines
                )

        # Displaying Gantt chart in Streamlit
        st.pyplot(fig)
        plt.close(fig)  # to prevent figures accumulating
    except Exception as e:
        logging.error(f"Error while calling display_gantt_chart_streamlit(): {e}")


def main_streamlit() -> None:
    """Main function to run the Streamlit web app for SJF Scheduling."""

    # Configuring Streamlit page
    st.set_page_config(
        page_title="SJF Scheduling Simulator",
        page_icon="⏱️",
        layout="wide"
    )
    
    # Customising buttons
    st.markdown("""
                <style>

                .stButton>button{
                    background:#8FC0FF;
                    color:black;
                    border-radius:10px;
                    font-size:18px;
                    height:3em;
                    width:100%;
                }

                .stButton>button:hover{
                    background:#1565C0;
                }

                </style>
                """, 
                unsafe_allow_html=True
                )

    # Rectangular container which contains all the output below for aesthetics
    with st.container(border=True):

        # Initialise session_state variables
        defaults = {"ordered_processes": [], "results_ready": False, "df": None, "avg_waiting": 0.0, "avg_turnaround": 0.0}
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

        processes: List[Process] = []   # initialising empty list to store processes

        st.title("Non-Preemptive Shortest Job First (SJF) Scheduling")
        st.markdown(
        """
        This simulator demonstrates the Non-Preemptive Shortest Job First (SJF) Scheduling algorithm.

        - Generates a table of results
        - Calculates average waiting time
        - Calculates average turnaround time
        - Simulates SJF execution
        - Displays a Gantt chart
        """
        )

        st.divider()

        # Creating two columns of ratio 3:7, left column is for input and right column is for output
        col1, col2 = st.columns([3, 7])

        with col1:
            with st.container(border=True):
                # Heading 'Input ProcessDeatils Below' styled
                st.markdown("""
                            <div style="
                            background-color:#8FC0FF;
                            padding:5px;
                            border-radius:10px;
                            ">
                            <h3>Input Process Details Below</h3>
                            </div>
                            """, 
                            unsafe_allow_html=True
                            )
                
                # Asking for and validating number of processes
                num_input = st.text_input("Enter number of processes")
                num_processes: Optional[int] = None
                if num_input:
                    value, message = validate_num_processes(num_input)
                    if value is not None:
                        num_processes = value
                    else:
                        st.error(message)

                if num_processes:   # if a valid number of processes is entered, ask for burst and arrival times
                    for i in range(num_processes):
                        # Asking for and validating burst time for each process
                        num_input = st.text_input(f"Enter burst time for process {i+1}")
                        burst_time: Optional[int] = None
                        if num_input:
                            value, message = validate_time(num_input)
                            if value is not None:
                                burst_time = value
                            else:
                                st.error(message)
                        # Asking for and validating arrival time for each process
                        num_input = st.text_input(f"Enter arrival time for process {i+1}")
                        arrival_time: Optional[int] = None
                        if num_input:
                            value, message = validate_time(num_input, allow_zero=True)
                            if value is not None:
                                arrival_time = value
                            else:
                                st.error(message)

                        # Adding the process to the list if both times given are valid
                        if burst_time is not None and arrival_time is not None:
                            processes.append(Process(i+1, burst_time, arrival_time))
                    
                    # Button to run SJF Scheduling if all processes have valid times
                    if processes:
                        run_sjf: bool = st.button("Run SJF Scheduling")


        with col2:  
            with st.container(border=True):
                if num_processes is None:
                    st.caption("Results will be displayed here after you click the 'Run SJF Scheduling' button.")
                    st.info(f"Please enter valid burst and arrival times.")
                else:
                    # Calculating and displaying results if times for all processes are valid and the user clicks the "Run SJF Scheduling" button
                    if len(processes) == num_processes:
                        if run_sjf:
                            # Calculating and storing the average times and the ordered list
                            avg_waiting, avg_turnaround, ordered_processes = calculate_sjf(processes)

                            # Saving everything into session_state
                            st.session_state["ordered_processes"] = ordered_processes
                            st.session_state["df"] = create_dataframe_processes(processes)
                            st.session_state["avg_waiting"] = avg_waiting
                            st.session_state["avg_turnaround"] = avg_turnaround
                            st.session_state["results_ready"] = True
                        
                        # Ensuring the table is displayed even if the page reruns
                        if st.session_state["results_ready"]:
                            display_results_streamlit()

                        st.divider()

                        # Separate button for simulation
                        st.subheader("SJF Simulation")
                        if st.button("Click here for SJF Simulation"):
                            simulate_execution_streamlit(st.session_state["ordered_processes"])

                        st.divider()

                        # Displaying Gantt chart
                        display_gantt_chart_streamlit(st.session_state["ordered_processes"])

    # Footer for the web app
    st.markdown(
        """
        <hr>
        <div style="text-align:center; color:grey; font-size:14px;">
            © 2026 Bhumika Gopaul | Non-Preemptive SJF Scheduling Simulator
        </div>
        """,
        unsafe_allow_html=True
    )


############################################################# LAUNCH MENU #############################################################

if __name__ == "__main__":
    
    try:
        # Detecting if Streamlit is running this file 
        # st.runtime.exists() is not officially documented Streamlit API but the other alternatives not working on my side
        if st.runtime.exists():   
            main_streamlit()
        else:
            while True:
                # CLI menu to choose between CLI and Streamlit
                print("Choose mode to run SJF Scheduling:")
                print("1. CLI")
                print("2. Streamlit")
                choice = input("Enter choice (1 or 2): ")

                if choice == "1":                    
                    main_cli()
                    break   # valid choice entered, so loop breaks
                elif choice == "2":
                    os.system(f"streamlit run {__file__}")
                    break   # valid choice entered, so loop breaks
                else:
                    print("Invalid choice. Please enter 1 or 2.")
                    # continue looping
    except ImportError:
        # If Streamlit not installed, running CLI
        main_cli()