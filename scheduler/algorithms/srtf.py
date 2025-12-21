# algorithms/srtf.py

def solve_srtf(processes):
    """
    SRTF (Shortest Remaining Time First) Implementation - Preemptive.
    The process with the shortest remaining time is executed at each step.
    """
    # Initialize remaining times for all processes 
    for p in processes:
        p.remaining_time = p.burst_time

    current_time = 0
    completed = 0
    n = len(processes)
    timeline = [] # To store Gantt segments: [pid, start, end]
    
    while completed < n:
        # Step 1: Filter processes that have arrived and still need CPU time
        available = [i for i, p in enumerate(processes) 
                     if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if available:
            # Step 2: Pick process with minimum remaining time.
            # Tie-break logic: smallest remaining time > earliest arrival > PID.
            idx = min(available, key=lambda x: (
                processes[x].remaining_time, 
                processes[x].arrival_time, 
                processes[x].pid
            ))
            p = processes[idx]
            
            # Step 3: Handle First Start for Response Time 
            if p.start_time is None: 
                p.start_time = current_time
            
            # Step 4: Record for Gantt Chart 
            # Merge segments if the same process continues to run
            if not timeline or timeline[-1][0] != p.pid:
                timeline.append([p.pid, current_time, current_time + 1])
            else:
                timeline[-1][2] += 1
            
            # Step 5: Execute for 1 unit of time
            p.remaining_time -= 1
            current_time += 1
            
            # Step 6: If finished, calculate final stats 
            if p.remaining_time == 0:
                completed += 1
                p.completion_time = current_time
                # Turnaround Time = Completion - Arrival 
                p.turnaround_time = p.completion_time - p.arrival_time
                # Waiting Time = Turnaround - Burst 
                p.waiting_time = p.turnaround_time - p.burst_time
                # Response Time = First Start - Arrival 
                p.response_time = p.start_time - p.arrival_time
        else:
            # CPU is idle if no process is ready
            current_time += 1

    return processes, timeline