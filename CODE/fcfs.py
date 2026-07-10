import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from typing import List, Dict, Any
import pandas as pd
import threading  #included threading module


#this class holds all the imformation for a single cpu task

class Process:
    
    def __init__(self, process_id: int, burst_time: int, arrival_time: int = 0):
        self.id: int = process_id
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0

    #calculates how long the process takes based on when it starts
    def calculate_metrics(self, start_time: int) -> None:
        
        #formulas applied:
           #Completion Time (CT) = Start Time + Burst Time
           #Turnaround Time (TAT) = Completion Time - Arrival Time
           #Waiting Time (WT) = Turnaround Time - Burst Time
        
        self.completion_time = start_time + self.burst_time
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def to_dict(self) -> Dict[str, Any]:
        
       #turns the process data into a dictionary for the table views
        return {
            "Process ID": f"P{self.id}",
            "Arrival time": self.arrival_time,
            "Burst time": self.burst_time,
            "Waiting time": self.waiting_time,
            "Turnaround time": self.turnaround_time,
            "Completion time": self.completion_time
        }



#This manages the list of processes and calculates the averages

class FCFSScheduler:
    
    def __init__(self) -> None:
        self.processes: List[Process] = []
        self.avg_waiting_time: float = 0.0
        self.avg_turnaround_time: float = 0.0
        

    def add_process(self, process: Process) -> None:
        #adds a process to the list
        self.processes.append(process)

    def clear_queue(self) -> None:
        #clear the list and resets average
        self.processes.clear()
        self.avg_waiting_time = 0.0
        self.avg_turnaround_time = 0.0

    def run_scheduling(self) -> None:
    
        #executes the First Come First Served algorithmic execution sequence.
    
        if not self.processes:
            return
             #sorts by arrival time so the first ones get processed first

        self.processes.sort(key=lambda p: p.arrival_time)

        current_time = 0
        total_waiting_time = 0
        total_turnaround_time = 0

        for process in self.processes:
            #if the CPU is idle, jump to the arrival time of the next process
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            #calculate times for this process
            process.calculate_metrics(current_time)
            
            #move clock forward
            current_time = process.completion_time
            
            #collect data for summary analysis
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time

        #calculate average
        self.avg_waiting_time = total_waiting_time / len(self.processes)
        self.avg_turnaround_time = total_turnaround_time / len(self.processes)

    def generate_dataframe(self) -> pd.DataFrame:
        
        #converts proces list into a readable table
        
        data_list = [p.to_dict() for p in self.processes]
        return pd.DataFrame(data_list)



#this manages the visual window and buttons

class FCFSGuiApplication:
    
    def __init__(self, window_root: tk.Tk) -> None:
        self.root = window_root
        self.root.title("Advanced CPU Architecture Workspace: FCFS Scheduler")
        self.root.geometry("750x650")
        self.root.configure(bg="#f4f6f9")
        
        self.scheduler = FCFSScheduler()
        
        #build UI Structure
        self._initialize_component_layout()
        self._load_default_assignment_dataset()

    def _initialize_component_layout(self) -> None:
        #sets up the buttons, inputs, and labels on the screen
        header_frame = tk.Frame(self.root, bg="#1e293b", height=60)
        header_frame.pack(fill=tk.X)
        
        lbl_title = tk.Label(
            header_frame, 
            text="First-Come, First-Served (FCFS) Process Engine", 
            fg="white", bg="#1e293b", font=("Helvetica", 14, "bold")
        )
        lbl_title.pack(pady=15)

     
        entry_frame = tk.LabelFrame(self.root, text=" Process Custom Registration Deck ", font=("Helvetica", 10, "bold"), bg="#ffffff", padx=15, pady=10)
        entry_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(entry_frame, text="Process ID (Int):", bg="#ffffff").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_pid = tk.Entry(entry_frame, width=10)
        self.ent_pid.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Burst Time:", bg="#ffffff").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.ent_burst = tk.Entry(entry_frame, width=10)
        self.ent_burst.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(entry_frame, text="Arrival Time:", bg="#ffffff").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.ent_arrival = tk.Entry(entry_frame, width=10)
        self.ent_arrival.insert(0, "0")  # Default setting setup
        self.ent_arrival.grid(row=0, column=5, padx=5, pady=5)

        #control panel execution command buttons
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Button(btn_frame, text="Add Process", command=self._handle_add_process, bg="#2563eb", fg="white", font=("Helvetica", 9, "bold"), width=14).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Run Simulation", command=self._handle_run_simulation, bg="#16a34a", fg="white", font=("Helvetica", 9, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load Assignment Data", command=self._load_default_assignment_dataset, bg="#475569", fg="white", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Canvas", command=self._handle_clear, bg="#dc2626", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        #output terminal 
        output_frame = tk.LabelFrame(self.root, text=" Analytics Console System Terminal Summary View ", font=("Helvetica", 10, "bold"), bg="#ffffff", padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self.terminal_display = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), bg="#0f172a", fg="#38bdf8", insertbackground="white")
        self.terminal_display.pack(fill=tk.BOTH, expand=True)

    #loads basic example data
    def _load_default_assignment_dataset(self) -> None:
        self.scheduler.clear_queue()
        
        #minimum baseline criteria dataset: P1(5), P2(8), P3(12)
        self.scheduler.add_process(Process(process_id=1, burst_time=5, arrival_time=0))
        self.scheduler.add_process(Process(process_id=2, burst_time=8, arrival_time=0))
        self.scheduler.add_process(Process(process_id=3, burst_time=12, arrival_time=0))
        
        self._refresh_terminal_log(">>> System Notice: Standard Core Coursework Matrix Loaded Safely.\n")
        self._display_current_queue_status()

    def _handle_add_process(self) -> None:
        #validates and adds a user-created execution process
        try:
            pid = int(self.ent_pid.get().strip())
            burst = int(self.ent_burst.get().strip())
            arrival = int(self.ent_arrival.get().strip())

            if burst <= 0 or arrival < 0 or pid <= 0:
                raise ValueError("Operational variables must remain positive real numerals.")

            #duplicate check verification safety guard
            if any(p.id == pid for p in self.scheduler.processes):
                messagebox.showerror("Validation Collision Error", f"Process Identification token 'P{pid}' already exists.")
                return

            self.scheduler.add_process(Process(pid, burst, arrival))
            self._refresh_terminal_log(f"-> Appended Custom context: P{pid} [Arrival: {arrival}, Burst: {burst}]\n")
            
            #clear input fields for easier usability
            self.ent_pid.delete(0, tk.END)
            self.ent_burst.delete(0, tk.END)
            self._display_current_queue_status()

        except ValueError as err:
            messagebox.showerror("Input Error Encountered", f"Configuration parsing exception verified:\n{err}")

    #starts the calculatrion on a background thread
    def _handle_run_simulation(self) -> None:
        if not self.scheduler.processes:
            messagebox.showwarning("Execution Aborted", "Register process contexts before simulating system calculations.")
            return

        #initialize and kick off the scheduling simulation on a separate execution thread
        simulation_thread = threading.Thread(target=self._execute_simulation_worker, daemon=True)
        simulation_thread.start()

    #performs the math and show results in the terminal area
    def _execute_simulation_worker(self) -> None:
        self.scheduler.run_scheduling()
        
        #build DataFrame structure using Pandas API mapping
        df = self.scheduler.generate_dataframe()
        
        #clear buffer and log formatted analysis tables directly to terminal pipeline
        self.terminal_display.delete('1.0', tk.END)
        self._refresh_terminal_log("                   FCFS CPU SCHEDULER SIMULATION COMPLETE                \n")
       
        #display the formatted data frame directly to the terminal
        self._refresh_terminal_log(df.to_string(index=False))
        
        self._refresh_terminal_log("\n\n" + "="*72 + "\n")
        self._refresh_terminal_log("                          MACRO PERFORMANCE TELEMETRY                    \n")
        self._refresh_terminal_log("="*72 + "\n")
        self._refresh_terminal_log(f" Average Waiting Time (AWT)      : {self.scheduler.avg_waiting_time:.2f} ms\n")
        self._refresh_terminal_log(f" Average Turnaround Time (ATAT)  : {self.scheduler.avg_turnaround_time:.2f} ms\n")
        self._refresh_terminal_log("="*72 + "\n")

    def _display_current_queue_status(self) -> None:
        #show the list of processes waiting to run
        if not self.scheduler.processes:
            self._refresh_terminal_log("System Queue Buffer Empty.\n")
            return
            
        self._refresh_terminal_log("\nCurrent Unscheduled Process Buffer Registry:\n")
        for p in self.scheduler.processes:
            self._refresh_terminal_log(f"  [Queue Array Slot] -> Process ID: P{p.id} | Burst Length: {p.burst_time} | Arrival Entry Index: {p.arrival_time}\n")

    def _handle_clear(self) -> None:
        #claers the screen and memory
        self.scheduler.clear_queue()
        self.terminal_display.delete('1.0', tk.END)
        self._refresh_terminal_log(">>> System Memory Repositories and Canvas Cleared Successfully.\n")

    def _refresh_terminal_log(self, text_segment: str) -> None:
        #updates the scrollable text box
        self.terminal_display.insert(tk.END, text_segment)
        self.terminal_display.see(tk.END)


#PROGRAM ENTRY POINT

if __name__ == "__main__":
    #instantiate standalone execution root runtime runtime canvas window context
    root_window = tk.Tk()
    app = FCFSGuiApplication(root_window)
    root_window.mainloop()
