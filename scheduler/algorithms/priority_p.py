# algorithms/priority_p.py

def solve_priority_p(processes):
    """
    Priority Scheduling (Preemptive) Implementation.
    If a new process arrives with a higher priority, the current process is preempted.
    """
    # Initialize remaining times
    for p in processes:
        p.remaining_time = p.burst_time

    current_time = 0
    completed = 0
    n = len(processes)
    timeline = [] # Store Gantt segments: [pid, start, end]
    
    while completed < n:
        # Step 1: Get available processes at current time
        available = [i for i, p in enumerate(processes) 
                     if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if available:
            # Step 2: Select highest priority (lowest value).
            # Tie-break: Priority > Arrival > PID.
            idx = min(available, key=lambda x: (
                processes[x].priority, 
                processes[x].arrival_time, 
                processes[x].pid
            ))
            p = processes[idx]
            
            # Step 3: Track first start for response time 
            if p.start_time is None: 
                p.start_time = current_time
            
            # Step 4: Record for Gantt Chart (merge segments) 
            if not timeline or timeline[-1][0] != p.pid:
                timeline.append([p.pid, current_time, current_time + 1])
            else:
                timeline[-1][2] += 1
            
            # Step 5: Execute for 1 unit
            p.remaining_time -= 1
            current_time += 1
            
            # Step 6: On finish, calculate stats 
            if p.remaining_time == 0:
                completed += 1
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time  
                p.waiting_time = p.turnaround_time - p.burst_time
                p.response_time = p.start_time - p.arrival_time 
        else:
            current_time += 1

    return processes, timeline