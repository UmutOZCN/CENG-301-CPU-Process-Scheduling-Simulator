# algorithms/fcfs.py

def solve_fcfs(processes):
    """
    FCFS (First-Come First-Served) Implementation.
    Non-preemptive: Once a process starts, it runs until completion.
    """
    
    # Step 1: Sort processes by arrival time, then by PID for ties.
    # This ensures deterministic behavior as required by the project specs.
    processes.sort(key=lambda x: (x.arrival_time, x.pid))
    
    current_time = 0
    gantt_output = [] # Format: (pid, start_time, end_time)
    
    for p in processes:
        # Step 2: Handle Idle Time.
        # If the CPU is free but no process has arrived, skip to the arrival time.
        if current_time < p.arrival_time:
            current_time = p.arrival_time
            
        # Step 3: Set timing metrics.
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        
        # Step 4: Calculate standard metrics using project formulas.
        # Turnaround Time = Completion - Arrival 
        p.turnaround_time = p.completion_time - p.arrival_time
        
        # Waiting Time = Turnaround - Burst 
        p.waiting_time = p.turnaround_time - p.burst_time
        
        # Response Time = First Start - Arrival 
        p.response_time = p.start_time - p.arrival_time
        
        # Step 5: Save for Gantt chart generation.
        gantt_output.append((p.pid, p.start_time, p.completion_time))
        
        # Advance clock to the end of current process.
        current_time = p.completion_time
        
    return processes, gantt_output