# utils/gantt.py

def render_gantt_chart(gantt_log):
    """
    Generates a professional ASCII Gantt chart showing time progression,
    running processes, and idle periods.
    """
    if not gantt_log:
        print("No execution data available.")
        return

    print("\n--- CPU SCHEDULING GANTT CHART ---")
    
    # We will build the chart in three rows: top border, middle (PID), and time axis
    top_row = " "
    mid_row = "|"
    time_row = "0"
    
    current_time = 0
    for pid, start, end in gantt_log:
        # Step 1: Handle CPU Idle Time (Gap between processes)
        if start > current_time:
            idle_width = (start - current_time) * 3
            top_row += " " * idle_width + " "
            mid_row += "IDLE".center(idle_width) + "|"
            time_row += str(start).rjust(idle_width + 1)
        
        # Step 2: Calculate block width based on duration 
        # We use a multiplier (3) to make short processes visible
        duration = end - start
        block_width = max(len(pid) + 2, duration * 3)
        
        # Step 3: Build the visual components
        # Python's .center() and .rjust() handle all the manual spacing you did!
        top_row += "_" * block_width + " "
        mid_row += pid.center(block_width) + "|"
        time_row += str(end).rjust(block_width + 1)
        
        current_time = end

    # Final Output
    print(top_row)
    print(mid_row)
    print(time_row)
    print("----------------------------------\n")