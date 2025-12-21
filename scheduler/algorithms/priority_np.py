# algorithms/priority_np.py

def solve_priority_np(processes):
    """
    Priority Scheduling (Non-Preemptive) Implementation.
    The process with the highest priority (lowest numerical value) is selected.
    Once started, it runs until completion.
    """
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_output = [] # Format: (pid, start, end)
    is_completed = [False] * n
    
    while completed < n:
        # Step 1: Find all processes that have arrived and are not finished
        available = [i for i in range(n) if processes[i].arrival_time <= current_time and not is_completed[i]]
        
        if available:
            # Step 2: Pick the process with the highest priority.
            # Tie-break: Smallest priority value > earliest arrival > PID order.
            idx = min(available, key=lambda x: (
                processes[x].priority, 
                processes[x].arrival_time, 
                processes[x].pid
            ))
            
            p = processes[idx]
            
            # Step 3: Set timing and calculate metrics 
            p.start_time = current_time
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time # 
            p.waiting_time = p.turnaround_time - p.burst_time
            p.response_time = p.start_time - p.arrival_time # 
            
            # Step 4: Update Gantt and state
            gantt_output.append((p.pid, p.start_time, p.completion_time))
            is_completed[idx] = True
            completed += 1
            current_time = p.completion_time # Move time to completion
            
        else:
            # CPU is idle; jump to the next arrival time
            pending_arrivals = [p.arrival_time for i, p in enumerate(processes) if not is_completed[i]]
            if pending_arrivals:
                current_time = min(pending_arrivals)
            else:
                break
                
    return processes, gantt_output