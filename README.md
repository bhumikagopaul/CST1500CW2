# CST1500 Coursework Two – Python Group Project

## Project Overview
This project implements CPU scheduling algorithms using Python.  
The algorithms included are:
- **First Come First Served (FCFS)**
- **Shortest Job First (SJF)**
- **Round Robin (RR)**

Each algorithm outputs process scheduling details such as burst time, waiting time, turnaround time, averages, etc following the coursework specification.

---

## Repository Structure
- CST1500CW2/
  - CODE/
    - fcfs.py  → FCFS scheduling implementation
    - sjf.py   → SJF scheduling implementation
    - rr.py    → Round Robin scheduling implementation
  - requirements.txt
  - README.md 

## Requirements
This project uses external Python libraries. Install them via `requirements.txt`:

```txt
pandas
matplotlib
streamlit
```

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/bhumikagopaul/CST1500CW2.git
cd CST1500CW2
pip install -r requirements.txt
```

### Note
Tkinter is part of Python but may need system installation.

## Usage
Run individual CLI algorithms:
```bash
python CODE/fcfs.py   # FCFS Algorithm
python CODE/sjf.py    # SJF Algorithm
python CODE/rr.py     # RR Algorithm
```

### Note
FCFS launches a Tkinter GUI window, while SJF and RR default to CLI.

Run SJF Streamlit web application:
```bash
streamlit run CODE/sjf.py
```