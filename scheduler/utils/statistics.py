# utils/statistics.py

def calculate_metrics(processes):
    """
    Computes average performance metrics for the simulation.
    Uses standard OS scheduling formulas:
    - Turnaround = Completion - Arrival 
    - Waiting = Turnaround - Burst 
    - Response = First Start - Arrival 
    """
    n = len(processes)
    if n == 0: return 0, 0, 0
    
    avg_turnaround = sum(p.turnaround_time for p in processes) / n
    avg_waiting = sum(p.waiting_time for p in processes) / n
    avg_response = sum(p.response_time for p in processes) / n
    
    return avg_turnaround, avg_waiting, avg_response

def count_context_switches(gantt_log):
    """
    Counts the total number of context switches.
    A switch is counted whenever a different process gains control of the CPU.
    """
    if not gantt_log: return 0
    
    switches = 0
    for i in range(1, len(gantt_log)):
        # If the PID of current segment is different from the previous one
        if gantt_log[i][0] != gantt_log[i-1][0]:
            switches += 1
            
    return switches