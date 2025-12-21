# algorithms/rr.py
from collections import deque

def solve_rr(processes, quantum):
    """
    Round Robin (RR) Implementation.
    Each process is assigned a fixed time unit (quantum) in a cyclic order.
    """
    # Initialize remaining times for all processes
    for p in processes:
        p.remaining_time = p.burst_time
        
    current_time = 0
    completed = 0
    n = len(processes)
    gantt_output = []
    
    # Ready Queue for managing processes
    queue = deque()
    # Tracking if a process is already in the queue to avoid duplicates
    in_queue = [False] * n
    
    # Ensure processes are sorted by arrival time for initial entry
    processes.sort(key=lambda x: (x.arrival_time, x.pid))
    
    # Add processes that have arrived at t=0
    for idx, p in enumerate(processes):
        if p.arrival_time <= current_time:
            queue.append(idx)
            in_queue[idx] = True

    while completed < n:
        if not queue:
            # If queue is empty but processes remain, jump to next arrival
            next_arrival = min([p.arrival_time for p in processes if p.remaining_time > 0])
            current_time = next_arrival
            for idx, p in enumerate(processes):
                if p.arrival_time <= current_time and not in_queue[idx]:
                    queue.append(idx)
                    in_queue[idx] = True
                    
        # Pop the first process from the queue
        idx = queue.popleft()
        p = processes[idx]
        
        # Record response time on first CPU contact 
        if p.start_time is None:
            p.start_time = current_time
        
        # Determine execution time (either quantum or remaining time)
        run_time = min(quantum, p.remaining_time)
        
        # Update Gantt log
        gantt_output.append((p.pid, current_time, current_time + run_time))
        
        # Progress time and reduce remaining burst
        current_time += run_time
        p.remaining_time -= run_time
        
        # IMPORTANT: Check for new arrivals while the process was running
        # These MUST enter the queue before the current process is re-added
        for i, other_p in enumerate(processes):
            if other_p.arrival_time <= current_time and not in_queue[i] and other_p.remaining_time > 0:
                queue.append(i)
                in_queue[i] = True
        
        # If the process is finished, calculate final metrics 
        if p.remaining_time == 0:
            completed += 1
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time 
            p.waiting_time = p.turnaround_time - p.burst_time 
            p.response_time = p.start_time - p.arrival_time 
        else:
            # If not finished, put it back at the end of the queue
            queue.append(idx)

    return processes, gantt_output