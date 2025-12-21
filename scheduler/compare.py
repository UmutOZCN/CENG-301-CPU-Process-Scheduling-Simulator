# compare.py
import matplotlib.pyplot as plt
import copy
import os
from utils.parser import parse_file
from utils.statistics import calculate_metrics, count_context_switches

# Import algorithms
from algorithms.fcfs import solve_fcfs
from algorithms.sjf import solve_sjf
from algorithms.srtf import solve_srtf
from algorithms.rr import solve_rr
from algorithms.priority_np import solve_priority_np
from algorithms.priority_p import solve_priority_p

def main():
    filename = 'processes.txt'
    original_procs = parse_file(filename)
    if not original_procs: return

    # Define algorithms to test 
    # Format: (Display Name, Function, Quantum or None)
    test_suite = [
        ('FCFS', solve_fcfs, None),
        ('SJF', solve_sjf, None),
        ('SRTF', solve_srtf, None),
        ('RR (q=4)', solve_rr, 4),
        ('PRIO_NP', solve_priority_np, None),
        ('PRIO_P', solve_priority_p, None)
    ]

    names, waits, turns, responses, cs_counts = [], [], [], [], []

    print("\n" + "="*80)
    print(f"{'Algorithm':<15} {'Avg Turn':<15} {'Avg Wait':<15} {'Avg Resp':<15} {'CS':<5}")
    print("-" * 80)

    for name, func, q in test_suite:
        # Use deepcopy to ensure each algorithm starts with fresh process data
        procs_copy = copy.deepcopy(original_procs)
        
        # Run algorithm
        finished, log = func(procs_copy, q) if q else func(procs_copy)
        
        # Collect stats 
        avg_t, avg_w, avg_r = calculate_metrics(finished)
        cs = count_context_switches(log)
        
        print(f"{name:<15} {avg_t:<15.2f} {avg_w:<15.2f} {avg_r:<15.2f} {cs:<5}")
        
        # Store for graphs
        names.append(name)
        waits.append(avg_w)
        turns.append(avg_t)

    # --- Generate Required Graphs  ---
    if not os.path.exists('graphs'): os.makedirs('graphs')

    # Graph 1: Avg Waiting Time 
    plt.figure(figsize=(10, 5))
    plt.bar(names, waits, color='skyblue')
    plt.title('Average Waiting Time vs Algorithm')
    plt.ylabel('Time (units)')
    plt.savefig('graphs/waiting.png') 

    # Graph 2: Avg Turnaround Time 
    plt.figure(figsize=(10, 5))
    plt.bar(names, turns, color='salmon')
    plt.title('Average Turnaround Time vs Algorithm')
    plt.ylabel('Time (units)')
    plt.savefig('graphs/turnaround.png')

    print("\n Graphs saved in 'graphs/' directory.")

if __name__ == "__main__":
    main()