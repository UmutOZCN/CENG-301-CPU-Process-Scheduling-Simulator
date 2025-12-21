# algorithms/sjf.py

def solve_sjf(processes):
    """
    SJF (Shortest Job First) - Non-Preemptive implementation.
    The process with the smallest burst time is executed first.
    """
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_output = []
    
    # Track which processes are finished
    is_completed = [False] * n
    
    while completed < n:
        # Step 1: Find all processes that have arrived but are not finished yet
        available_processes = []
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                available_processes.append(i)
        
        if available_processes:
            # Step 2: Pick the shortest job. 
            # Tie-break: Smallest burst time first, then earliest arrival, then PID.
            # This ensures determinism as requested in the project brief.
            idx = min(available_processes, key=lambda x: (
                processes[x].burst_time, 
                processes[x].arrival_time, 
                processes[x].pid
            ))
            
            p = processes[idx]
            
            # Step 3: Record timing statistics 
            p.start_time = current_time
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.response_time = p.start_time - p.arrival_time
            
            # Step 4: Update Gantt chart and system state
            gantt_output.append((p.pid, p.start_time, p.completion_time))
            is_completed[idx] = True
            completed += 1
            current_time = p.completion_time # Non-preemptive: move time to completion
            
        else:
            # Step 5: If no process is ready, jump current_time to the next arrival 
            # This avoids an infinite loop and handles CPU idle periods.
            pending_arrivals = [p.arrival_time for i, p in enumerate(processes) if not is_completed[i]]
            if pending_arrivals:
                current_time = min(pending_arrivals)
            else:
                break

    return processes, gantt_output