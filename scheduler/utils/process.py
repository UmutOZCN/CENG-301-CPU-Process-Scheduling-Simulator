# utils/process.py

class Process:
    """
    A class to represent a CPU process and its scheduling metrics.
    """
    def __init__(self, pid, arrival_time, burst_time, priority):
        # Static properties from input file 
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Dynamic properties for simulation logic
        self.remaining_time = burst_time  # Used for preemptive algorithms (SRTF, RR)
        self.start_time = None            # To calculate Response Time 
        self.completion_time = 0          # Time when execution finishes 
        self.waiting_time = 0             # Total time spent in ready queue 
        self.turnaround_time = 0          # Total time from arrival to completion 
        self.response_time = 0            # Time from arrival to first CPU contact 

    def __repr__(self):
        """String representation for debugging and logging."""
        return f"Process(PID={self.pid}, Arr={self.arrival_time}, Burst={self.burst_time}, Prio={self.priority})"