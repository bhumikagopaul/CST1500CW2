def run_fcfs(processes, burst_times):

    #implement the FCFS scheduling algorithm
    #processes are executed in the order they arrive

    n = len(processes)
    waiting_times = [0] * n
    turn_around_times = [0] * n

    #first process to arrive always has a waiting time of 0
    waiting_times[0] = 0

    #calculate waiting times for the remaining processes
    #waiting time = burst time of previous process + waiting time of previous process
    for i in range(1, n):
        waiting_times[i] = waiting_times[i - 1] + burst_times[i - 1]

    #calculate turn-around times
    #turn-around time = waiting time + burst time
    for i in range(n):
        turn_around_times[i] = waiting_times[i] + burst_times[i]

        #format and display the final results as specified in the assignment 
        print(f"\n{'='*20} First-Come, First-Served (FCFS) Simulation Results {'='*20}")
        print(f"\n{'Process':<10}{'Burst Time':<15}{'Waiting Time':<15}{'Turn-Around Time':<20}")
        print('-'*62)

        for i in range(n):
            print(f"{processes[i]:<16}{burst_times[i]:<12}{waiting_times[i]:<14}{turn_around_times[i]:<18}")

        #calculate and output summary average
        avg_waiting_time = sum(waiting_times) / n
        avg_turn_around_time = sum(turn_around_times) / n

        print("-"*62)
    print(f"\n{'Average Waiting Time:'}{avg_waiting_time:.2f}")
    print(f"{'Average Turn-Around Time:'}{avg_turn_around_time:.2f}")
    print(f"{'='*54}\n")

def main():
            print("\n--- First-Come, First-Served (FCFS) Scheduling Program ---")
            use_default = input("Use the baseline assignment test data? (Y/N): > ").strip().lower()
            
            if use_default == 'y' or use_default == '':
                #default minimum test data provided in the project specification sheet
                processes = [1, 2, 3]
                burst_times = [5, 8, 12]
            else:
                #dynamic user input collection to satisfy the higher grade evaluation bands
                while True:
                    try:
                        num_processes = int(input("Enter the number of processes:  "))
                        if num_processes <= 0:
                            print("Please enter a positive integer for the number of processes.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                    except ValueError:
                        print("Invalid input. Please enter numbers only.")

            processes = []
            burst_times = []

            for i in range(num_processes):
                processes.append(i + 1)  # Process IDs starting from 1
                while True:
                    try:
                        b_time = int(input(f"Enter burst time for process {i + 1}:  "))
                        if b_time <= 0:
                            print("Burst time must be greater than 0.")
                            continue
                        burst_times.append(b_time)
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer value.")
                
                #execute the algorithm logic
                run_fcfs(processes, burst_times)

                
if __name__ == '__main__':
    main()