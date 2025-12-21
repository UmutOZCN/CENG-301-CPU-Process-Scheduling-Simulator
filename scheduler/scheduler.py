# scheduler.py
import argparse
import sys
from utils.parser import parse_file
from utils.gantt import render_gantt_chart
from utils.statistics import calculate_metrics, count_context_switches

# Import algorithms
from algorithms.fcfs import solve_fcfs
from algorithms.sjf import solve_sjf
from algorithms.srtf import solve_srtf
from algorithms.rr import solve_rr
from algorithms.priority_np import solve_priority_np
from algorithms.priority_p import solve_priority_p

def print_execution_log(gantt_log):
    """Prints a detailed timeline log of scheduling events."""
    print("\n--- DETAILED EXECUTION LOG ---")
    for pid, start, end in gantt_log:
        # Each entry shows when a process starts and finishes/preempted
        print(f"t={start}: {pid} starts running")
        print(f"t={end}: {pid} finishes/preempted")

def print_results_table(processes):
    """Prints the per-process statistics in a formatted table."""
    print("\n" + "="*85)
    # Required table headers
    header = f"{'PID':<6} {'Arr':<6} {'Burst':<8} {'Compl':<8} {'Turn':<12} {'Wait':<10} {'Resp':<10}"
    print(header)
    print("-" * 85)
    
    for p in processes:
        print(f"{p.pid:<6} {p.arrival_time:<6} {p.burst_time:<8} {p.completion_time:<8} "
              f"{p.turnaround_time:<12} {p.waiting_time:<10} {p.response_time:<10}")
    print("="*85)

def main():
    # CLI argument configuration
    parser = argparse.ArgumentParser(description="CENG 301 CPU Scheduling Simulator")
    parser.add_argument('--input', type=str, required=True, help="Path to input file (e.g., processes.txt)")
    parser.add_argument('--algo', type=str, required=True, 
                        choices=['FCFS', 'SJF', 'SRTF', 'RR', 'PRIO_NP', 'PRIO_P'],
                        help="Scheduling algorithm to use")
    parser.add_argument('--quantum', type=int, help="Time quantum (Required for RR)")

    args = parser.parse_args()

    # Step 1: Parse the input file
    processes = parse_file(args.input)
    if not processes:
        return

    # Step 2: Select and run the algorithm
    # Each algorithm must return the modified process list and a Gantt log
    result_procs, gantt_log = None, None

    if args.algo == 'FCFS':
        result_procs, gantt_log = solve_fcfs(processes)
    elif args.algo == 'SJF':
        result_procs, gantt_log = solve_sjf(processes)
    elif args.algo == 'SRTF':
        result_procs, gantt_log = solve_srtf(processes)
    elif args.algo == 'RR':
        if args.quantum is None:
            print("Error: --quantum is required for RR algorithm.")
            return
        result_procs, gantt_log = solve_rr(processes, args.quantum)
    elif args.algo == 'PRIO_NP':
        result_procs, gantt_log = solve_priority_np(processes)
    elif args.algo == 'PRIO_P':
        result_procs, gantt_log = solve_priority_p(processes)

    # Step 3: Generate Outputs
    if result_procs and gantt_log:
        print_results_table(result_procs)
        
        # Calculate and print averages and context switches
        avg_t, avg_w, avg_r = calculate_metrics(result_procs)
        cs = count_context_switches(gantt_log)
        
        print(f"Average Turnaround Time: {avg_t:.2f}")
        print(f"Average Waiting Time: {avg_w:.2f}")
        print(f"Average Response Time: {avg_r:.2f}")
        print(f"Total Context Switches: {cs}")
        
        print_execution_log(gantt_log)
        render_gantt_chart(gantt_log)

if __name__ == "__main__":
    main()