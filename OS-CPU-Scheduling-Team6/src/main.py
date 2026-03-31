"""
main.py — CPU Scheduling Simulator
Run: python main.py
"""

from srt import run_srt
from rr  import run_rr
from fcfs import run_fcfs
from sjf  import run_sjf
from mlfq import run_mlfq

DIVIDER = "=" * 70


# ─────────────────────────────────────────────
#  Display — Gantt Chart
# ─────────────────────────────────────────────

def merge_gantt(gantt):
    """Merge consecutive same-pid segments."""
    if not gantt:
        return gantt
    merged = [gantt[0].copy()]
    for seg in gantt[1:]:
        if seg['pid'] == merged[-1]['pid'] and seg['start'] == merged[-1]['end']:
            merged[-1]['end'] = seg['end']
        else:
            merged.append(seg.copy())
    return merged


def print_gantt_chart(gantt):
    gantt    = merge_gantt(gantt)
    top      = ""
    middle   = ""
    bottom   = ""
    time_row = ""

    for seg in gantt:
        pid   = seg['pid']
        start = seg['start']
        end   = seg['end']
        width = max(len(pid) + 2, 6)
        top    += "+" + "-" * width
        middle += "| " + pid.center(width - 2) + " "
        bottom += "+" + "-" * width
        label   = str(start)
        time_row += label + " " * (width + 1 - len(label))

    top      += "+"
    middle   += "|"
    bottom   += "+"
    time_row += str(gantt[-1]['end'])

    print("\n  Gantt Chart")
    print("  " + top)
    print("  " + middle)
    print("  " + bottom)
    print("  " + time_row)
    print()


# ─────────────────────────────────────────────
#  Display — Metrics Table
# ─────────────────────────────────────────────

def print_metrics(results, algorithm_name):
    col_widths = [5, 14, 12, 13, 17, 14]
    headers    = ["Job", "Arrival Time", "Burst Time",
                  "Finish Time", "Turnaround Time", "Waiting Time"]

    sep  = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    head = "| " + " | ".join(h.center(w) for h, w in zip(headers, col_widths)) + " |"

    print(f"  {algorithm_name}")
    print("  " + sep)
    print("  " + head)
    print("  " + sep)

    total_tat = total_wt = 0
    n = len(results)

    for r in sorted(results, key=lambda x: x['arrival']):
        total_tat += r['turnaround']
        total_wt  += r['waiting']

        row = "| " + " | ".join([
            r['pid'].center(col_widths[0]),
            str(r['arrival']).center(col_widths[1]),
            str(r['burst']).center(col_widths[2]),
            str(r['finish']).center(col_widths[3]),
            str(r['turnaround']).center(col_widths[4]),
            str(r['waiting']).center(col_widths[5]),
        ]) + " |"
        print("  " + row)

    print("  " + sep)

    avg_tat_str = f"{total_tat} / {n} = {total_tat/n:.2f}"
    avg_wt_str  = f"{total_wt} / {n} = {total_wt/n:.2f}"

    avg_row = ("| " +
               "".center(col_widths[0]) + " | " +
               "".center(col_widths[1]) + " | " +
               "".center(col_widths[2]) + " | " +
               "Average".center(col_widths[3]) + " | " +
               avg_tat_str.center(col_widths[4]) + " | " +
               avg_wt_str.center(col_widths[5]) + " |")
    print("  " + avg_row)
    print("  " + sep)
    print()

    return {
        "avg_waiting_time"    : round(total_wt  / n, 2),
        "avg_turnaround_time" : round(total_tat / n, 2),
    }


def print_comparison(summary):
    print("\n" + DIVIDER)
    print("  Comparative Summary")
    print(DIVIDER)
    print(f"  {'Algorithm':<25} {'Avg Turnaround Time':>22} {'Avg Waiting Time':>18}")
    print("  " + "-" * 67)
    for name, avg in summary.items():
        print(f"  {name:<25} {avg['avg_turnaround_time']:>22.2f} {avg['avg_waiting_time']:>18.2f}")
    print("  " + "-" * 67 + "\n")


# ─────────────────────────────────────────────
#  Input
# ─────────────────────────────────────────────

def input_processes():
    processes = []
    print("\n  Enter processes (press Enter with no PID to finish):\n")
    idx = 1
    while True:
        pid = input(f"    PID (default P{idx}, Enter to stop): ").strip()
        if pid == "" and idx > 1:
            break
        if pid == "":
            pid = f"P{idx}"
        try:
            arrival = int(input(f"    {pid} Arrival Time : "))
            burst   = int(input(f"    {pid} Burst Time   : "))
        except ValueError:
            print("    Please enter integers only.\n")
            continue
        processes.append({'pid': pid, 'arrival': arrival, 'burst': burst})
        print()
        idx += 1
    return processes


def sample_processes():
    return [
        {'pid': 'P1', 'arrival': 0, 'burst': 5},
        {'pid': 'P2', 'arrival': 1, 'burst': 3},
        {'pid': 'P3', 'arrival': 2, 'burst': 8},
        {'pid': 'P4', 'arrival': 3, 'burst': 6},
    ]


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────

def main():
    summary = {}

    while True:
        print("\n" + DIVIDER)
        print("         CPU Scheduling Algorithm Simulator")
        print(DIVIDER)

        # Step 1 — Choose algorithm
        print("\n  Select Algorithm:")
        print("  [1] FCFS  - First Come First Serve")
        print("  [2] SJF   - Shortest Job First")
        print("  [3] SRT   - Shortest Remaining Time")
        print("  [4] RR    - Round Robin")
        print("  [5] MLFQ  - Multilevel Feedback Queue")
        print("  [6] Show Comparison Table")
        print("  [0] Exit")

        algo = input("\n  Choice: ").strip()

        if algo == "0":
            print("\n  Goodbye!\n")
            break

        if algo == "6":
            if summary:
                print_comparison(summary)
            else:
                print("\n  No results yet. Run at least one algorithm first.")
            continue

        if algo not in ("1", "2", "3", "4", "5"):
            print("\n  Invalid choice. Please try again.")
            continue

        # Step 2 — Enter processes
        print("\n  Process Input:")
        print("  [1] Use sample scenario (P1=0,5 | P2=1,3 | P3=2,8 | P4=3,6)")
        print("  [2] Enter processes manually")
        src = input("\n  Choice: ").strip()

        processes = sample_processes() if src != "2" else input_processes()

        if not processes:
            print("\n  No processes entered. Please try again.")
            continue

        if src != "2":
            print("\n  Sample scenario loaded:")
            for p in processes:
                print(f"    {p['pid']}: Arrival={p['arrival']}, Burst={p['burst']}")

        # Step 3 — Quantum (only for RR and MLFQ)
        quantum = 2
        if algo in ("4", "5"):
            try:
                quantum = int(input("\n  Enter Time Quantum (default 2): ").strip() or "2")
            except ValueError:
                quantum = 2

        # Step 4 — Run selected algorithm
        print(f"\n{DIVIDER}")

        if algo == "1":
            print("  Algorithm: FCFS\n" + DIVIDER)
            # gantt, results = run_fcfs(processes)
            # print_gantt_chart(gantt)
            # summary["FCFS"] = print_metrics(results, "FCFS")
            print("  FCFS coming soon (Person 1).")

        elif algo == "2":
            print("  Algorithm: SJF\n" + DIVIDER)
            # gantt, results = run_sjf(processes)
            # print_gantt_chart(gantt)
            # summary["SJF"] = print_metrics(results, "SJF")
            print("  SJF coming soon (Person 1).")

        elif algo == "3":
            print("  Algorithm: SRT\n" + DIVIDER)
            gantt, results = run_srt(processes)
            print_gantt_chart(gantt)
            summary["SRT"] = print_metrics(results, "SRT")

        elif algo == "4":
            print(f"  Algorithm: Round Robin (Quantum = {quantum})\n" + DIVIDER)
            gantt, results = run_rr(processes, quantum)
            print_gantt_chart(gantt)
            summary[f"RR (q={quantum})"] = print_metrics(results, f"Round Robin (q={quantum})")

        elif algo == "5":
            print("  Algorithm: MLFQ\n" + DIVIDER)
            # gantt, results = run_mlfq(processes, quantum)
            # print_gantt_chart(gantt)
            # summary["MLFQ"] = print_metrics(results, "MLFQ")
            print("  MLFQ coming soon (Person 3).")