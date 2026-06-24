import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from typing import List, Dict, Any
import pandas as pd


class Process:
    """
    Represents an independent CPU Process lifecycle context.
    Encapsulates identifiers, workloads, state metrics, and core formula tracking.
    """
    def __init__(self, process_id: int, burst_time: int, arrival_time: int = 0):
        self.id: int = process_id
        self.burst_time: int = burst_time
        self.arrival_time: int = arrival_time
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: int = 0

    def calculate_metrics(self, start_time: int) -> None:
        """
        Calculates operational performance metrics for this isolated process.
        Formulas applied:
            - Completion Time (CT) = Start Time + Burst Time
            - Turnaround Time (TAT) = Completion Time - Arrival Time
            - Waiting Time (WT) = Turnaround Time - Burst Time
        """
        self.completion_time = start_time + self.burst_time
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def to_dict(self) -> Dict[str, Any]:
        """Converts the object properties into a standard dictionary dictionary structure for pandas mapping."""
        return {
            "Process ID": f"P{self.id}",
            "Arrival Time": self.arrival_time,
            "Burst Time": self.burst_time,
            "Waiting Time": self.waiting_time,
            "Turnaround Time": self.turnaround_time,
            "Completion Time": self.completion_time
        }


class FCFSScheduler:
    """
    Algorithmic Core Engine. Handles the process execution queue array, 
    implements FCFS chronological sorting logic, and aggregates analytical system averages.
    """
    def __init__(self) -> None:
        self.processes: List[Process] = []
        self.avg_waiting_time: float = 0
