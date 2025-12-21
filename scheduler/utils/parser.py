# utils/parser.py
import sys
from utils.process import Process

def parse_file(filename):
    """
    Reads process data from a text file and returns a list of Process objects.
    Follows project rules for ignoring comments and handling whitespace .
    """
    processes = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Rule: Ignore parts after '#' (comments) 
                clean_line = line.split('#')[0].strip()
                
                # Rule: Skip empty lines
                if not clean_line:
                    continue
                
                # Rule: Fields are separated by whitespace 
                parts = clean_line.split()
                
                if len(parts) >= 4:
                    pid = parts[0] # String 
                    # Convert metrics to integers 
                    arrival = int(parts[1])
                    burst = int(parts[2])
                    priority = int(parts[3])
                    
                    processes.append(Process(pid, arrival, burst, priority))
                
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid data format in input file. Please check integers.")
        sys.exit(1)

    return processes