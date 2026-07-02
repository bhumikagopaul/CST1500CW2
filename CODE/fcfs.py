import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from typing import List, Dict, Any
import pandas as pd
import threading  # Included threading module


# CLASS: Process

class Process:

    #represents an independent CPU Process lifecycle context.
    #encapsulates identifiers, workloads, state metrics, and core formula tracking.
    
    def __init__(self, process_id: int, burst_time: int, arrival_time: int = 0):
        self.id: int = process_id
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0

    def calculate_metrics(self, start_time: int) -> None:
        
        #calculates operational performance metrics for this isolated process.
        #formulas applied:
           #Completion Time (CT) = Start Time + Burst Time
           #Turnaround Time (TAT) = Completion Time - Arrival Time
           #Waiting Time (WT) = Turnaround Time - Burst Time
        
        self.completion_time = start_time + self.burst_time
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def to_dict(self) -> Dict[str, Any]:
        
        #converts the object properties into a standard dictionary structure 
        #for pandas mapping and GUI tabular presentation.
        
        return {
            "Process ID": f"P{self.id}",
            "Arrival Time": self.arrival_time,
            "Burst Time": self.burst_time,
            "Waiting Time": self.waiting_time,
            "Turnaround Time": self.turnaround_time,
            "Completion Time": self.completion_time
        }



# CLASS: FCFSScheduler

class FCFSScheduler:
    
    #algorithmic Core Engine. Handles the process execution queue array,
    #implements FCFS chronological sorting logic, and aggregates analytical system averages.
    
    def __init__(self) -> None:
        self.processes: List[Process] = []
        self.avg_waiting_time: float = 0.0
        self.avg_turnaround_time: float = 0.0

    def add_process(self, process: Process) -> None:
        #appends a valid process object into the scheduling registration queue.
        self.processes.append(process)

    def clear_queue(self) -> None:
        #flushes the registered process list to reset system states.
        self.processes.clear()
        self.avg_waiting_time = 0.0
        self.avg_turnaround_time = 0.0

    def run_scheduling(self) -> None:
    
        #executes the First Come First Served algorithmic execution sequence.
        #sorts incoming items by arrival time, sequentially executes them, 
        #and updates system average metrics.
    
        if not self.processes:
            return

        #sort based on arrival time to maintain strict chronological FCFS integrity
        self.processes.sort(key=lambda p: p.arrival_time)

        current_time = 0
        total_waiting_time = 0
        total_turnaround_time = 0

        for process in self.processes:
            #handle idle CPU state if a process hasn't arrived yet
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            #compute processing metrics
            process.calculate_metrics(current_time)
            
            #progress system timeline forward
            current_time = process.completion_time
            
            #collect data for summary analysis
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time

        #calculate final macro statistical trends
        self.avg_waiting_time = total_waiting_time / len(self.processes)
        self.avg_turnaround_time = total_turnaround_time / len(self.processes)

    def generate_dataframe(self) -> pd.DataFrame:
        
        #leverages Pandas API to transform internal object arrays into structured 
        #DataFrames for analytics mapping and clean presentation outputs.
        
        data_list = [p.to_dict() for p in self.processes]
        return pd.DataFrame(data_list)



# CLASS: FCFSGuiApplication (The Desktop Layer Interface)

class FCFSGuiApplication:
    
    #user Interface Presentation Controller utilizing Tkinter. 
    #manages layout matrices, structural inputs, rendering logic, and validation schemas.
    
    def __init__(self, window_root: tk.Tk) -> None:
        self.root = window_root
        self.root.title("Advanced CPU Architecture Workspace: FCFS Scheduler")
        self.root.geometry("750x650")
        self.root.configure(bg="#f4f6f9")
        
        #instantiate scheduler core controller context
        self.scheduler = FCFSScheduler()
        
        #build UI Structure
        self._initialize_component_layout()
        self._load_default_assignment_dataset()

    def _initialize_component_layout(self) -> None:
        #Constructs widgets grid structure across the frame canvas.
        # Top Header Banner Frame
        header_frame = tk.Frame(self.root, bg="#1e293b", height=60)
        header_frame.pack(fill=tk.X)
        
        lbl_title = tk.Label(
            header_frame, 
            text="First-Come, First-Served (FCFS) Process Engine", 
            fg="white", bg="#1e293b", font=("Helvetica", 14, "bold")
        )
        lbl_title.pack(pady=15)

        # Dynamic Custom Data Entry Interactive Deck
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

        # Control Panel Execution Command Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Button(btn_frame, text="Add Process", command=self._handle_add_process, bg="#2563eb", fg="white", font=("Helvetica", 9, "bold"), width=14).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Run Simulation", command=self._handle_run_simulation, bg="#16a34a", fg="white", font=("Helvetica", 9, "bold"), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load Assignment Data", command=self._load_default_assignment_dataset, bg="#475569", fg="white", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Canvas", command=self._handle_clear, bg="#dc2626", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        # Output Terminal & Telemetry Logs
        output_frame = tk.LabelFrame(self.root, text=" Analytics Console System Terminal Summary View ", font=("Helvetica", 10, "bold"), bg="#ffffff", padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self.terminal_display = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), bg="#0f172a", fg="#38bdf8", insertbackground="white")
        self.terminal_display.pack(fill=tk.BOTH, expand=True)

    def _load_default_assignment_dataset(self) -> None:
        #Injects core assignment parameters natively required within assignment documentation specifications.
        self.scheduler.clear_queue()
        
        # Minimum baseline criteria dataset: P1(5), P2(8), P3(12)
        self.scheduler.add_process(Process(process_id=1, burst_time=5, arrival_time=0))
        self.scheduler.add_process(Process(process_id=2, burst_time=8, arrival_time=0))
        self.scheduler.add_process(Process(process_id=3, burst_time=12, arrival_time=0))
        
        self._refresh_terminal_log(">>> System Notice: Standard Core Coursework Matrix Loaded Safely.\n")
        self._display_current_queue_status()

    def _handle_add_process(self) -> None:
        #Validates entry parameters and saves a generated custom user-defined execution process block instance.
        try:
            pid = int(self.ent_pid.get().strip())
            burst = int(self.ent_burst.get().strip())
            arrival = int(self.ent_arrival.get().strip())

            if burst <= 0 or arrival < 0 or pid <= 0:
                raise ValueError("Operational variables must remain positive real numerals.")

            # Duplicate Check Verification Safety Guard
            if any(p.id == pid for p in self.scheduler.processes):
                messagebox.showerror("Validation Collision Error", f"Process Identification token 'P{pid}' already exists.")
                return

            # Register clean item instance
            self.scheduler.add_process(Process(pid, burst, arrival))
            self._refresh_terminal_log(f"-> Appended Custom context: P{pid} [Arrival: {arrival}, Burst: {burst}]\n")
            
            # Clear input fields for easier usability
            self.ent_pid.delete(0, tk.END)
            self.ent_burst.delete(0, tk.END)
            self._display_current_queue_status()

        except ValueError as err:
            messagebox.showerror("Input Error Encountered", f"Configuration parsing exception verified:\n{err}")

    def _handle_run_simulation(self) -> None:
        # Verifies queue before spinning up the execution thread
        if not self.scheduler.processes:
            messagebox.showwarning("Execution Aborted", "Register process contexts before simulating system calculations.")
            return

        # Initialize and kick off the scheduling simulation on a separate execution thread
        simulation_thread = threading.Thread(target=self._execute_simulation_worker, daemon=True)
        simulation_thread.start()

    def _execute_simulation_worker(self) -> None:
        # Compiles metric calculations via Scheduler Core and produces system reports using Pandas data frameworks.
        # Core operational engine routine pass execution
        self.scheduler.run_scheduling()
        
        # Build DataFrame structure using Pandas API mapping
        df = self.scheduler.generate_dataframe()
        
        # Clear buffer and log formatted analysis tables directly down to terminal pipeline
        self.terminal_display.delete('1.0', tk.END)
        self._refresh_terminal_log("                   FCFS CPU SCHEDULER SIMULATION COMPLETE                \n")
       
        # Display the formatted data frame directly to the terminal
        self._refresh_terminal_log(df.to_string(index=False))
        
        self._refresh_terminal_log("\n\n" + "="*72 + "\n")
        self._refresh_terminal_log("                          MACRO PERFORMANCE TELEMETRY                    \n")
        self._refresh_terminal_log("="*72 + "\n")
        self._refresh_terminal_log(f" Average Waiting Time (AWT)      : {self.scheduler.avg_waiting_time:.2f} ms\n")
        self._refresh_terminal_log(f" Average Turnaround Time (ATAT)  : {self.scheduler.avg_turnaround_time:.2f} ms\n")
        self._refresh_terminal_log("="*72 + "\n")

    def _display_current_queue_status(self) -> None:
        #Renders raw registration entries prior to operational computation cycles.
        if not self.scheduler.processes:
            self._refresh_terminal_log("System Queue Buffer Empty.\n")
            return
            
        self._refresh_terminal_log("\nCurrent Unscheduled Process Buffer Registry:\n")
        for p in self.scheduler.processes:
            self._refresh_terminal_log(f"  [Queue Array Slot] -> Process ID: P{p.id} | Burst Length: {p.burst_time} | Arrival Entry Index: {p.arrival_time}\n")

    def _handle_clear(self) -> None:
        #Wipes terminal panels and functional simulation lists clean.
        self.scheduler.clear_queue()
        self.terminal_display.delete('1.0', tk.END)
        self._refresh_terminal_log(">>> System Memory Repositories and Canvas Cleared Successfully.\n")

    def _refresh_terminal_log(self, text_segment: str) -> None:
        #Safely inserts structured output records into console visual interface panels.
        self.terminal_display.insert(tk.END, text_segment)
        self.terminal_display.see(tk.END)


# APPLICATION ENVIRONMENT ENTRY POINT

if __name__ == "__main__":
    # Instantiate standalone execution root runtime runtime canvas window context
    root_window = tk.Tk()
    app = FCFSGuiApplication(root_window)
    root_window.mainloop()
