from fcfs import run_fcfs
from sjf import run_sjf


def get_processes():
    """Get process input from user"""
    processes = []

    print("\nHow many processes do you want to run? ", end="")
    n = int(input())

    for i in range(n):
        pid = f"P{i+1}"
        arrival = int(input(f"  Arrival Time for {pid}: "))
        burst = int(input(f"  Burst Time for {pid}  : "))
        processes.append({'pid': pid, 'arrival': arrival, 'burst': burst})

    return processes


def print_gantt_chart(gantt_chart):
    """Display ASCII Gantt chart"""
    print("\n--- Gantt Chart ---")

    top = ""
    middle = ""
    timeline = ""

    for block in gantt_chart:
        width = max((block['end'] - block['start']) * 2, len(block['pid']) + 2)
        top += "+" + "-" * width
        middle += "|" + block['pid'].center(width)

    top += "+"
    middle += "|"

    # Timeline
    timeline = str(gantt_chart[0]['start'])
    for block in gantt_chart:
        width = max((block['end'] - block['start']) * 2, len(block['pid']) + 2)
        timeline += " " * width + str(block['end'])

    print(top)
    print(middle)
    print(top)
    print(timeline)


def print_results(results):
    """Display results table"""
    print("\n--- Results Table ---")
    print(f"{'PID':<6} {'Arrival':<10} {'Burst':<8} {'Finish':<10} {'Turnaround':<14} {'Waiting':<10} {'Response':<10}")
    print("-" * 68)

    total_waiting = 0
    total_turnaround = 0
    total_response = 0

    for r in results:
        print(f"{r['pid']:<6} {r['arrival']:<10} {r['burst']:<8} {r['finish']:<10} {r['turnaround']:<14} {r['waiting']:<10} {r['response']:<10}")
        total_waiting += r['waiting']
        total_turnaround += r['turnaround']
        total_response += r['response']

    n = len(results)
    print("-" * 68)
    print(f"{'Average':<6} {'':<10} {'':<8} {'':<10} {total_turnaround}/{n} = {total_turnaround/n:<8.1f} {total_waiting}/{n} = {total_waiting/n:<4.1f} {total_response}/{n} = {total_response/n:.1f}")


def select_algorithm():
    """Show algorithm menu and return choice"""
    print("\nSelect Algorithm:")
    print("  1. FCFS - First Come First Serve")
    print("  2. SJF  - Shortest Job First")
    print("\nEnter choice (1-2): ", end="")

    while True:
        choice = input().strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice! Enter 1 or 2: ", end="")


def main():
    while True:
        print("\n" + "=" * 45)
        print("      CPU Scheduling Simulator")
        print("=" * 45)

        choice = select_algorithm()
        processes = get_processes()

        if choice == '1':
            print("\n>> Running FCFS...")
            gantt_chart, results = run_fcfs(processes)
        elif choice == '2':
            print("\n>> Running SJF...")
            gantt_chart, results = run_sjf(processes)

        print_gantt_chart(gantt_chart)
        print_results(results)

        print("\nRun again? (y/n): ", end="")
        again = input().strip().lower()
        if again != 'y':
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()