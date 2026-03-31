"""
srt.py — Shortest Remaining Time (Preemptive SJF)
Person 2
"""


def run_srt(processes):
    """
    Shortest Remaining Time — preemptive SJF.

    Parameters:
        processes : list of dicts with keys: pid, arrival, burst

    Returns:
        gantt_chart : list of dicts with keys: pid, start, end
        results     : list of dicts with keys: pid, arrival, burst,
                      start, finish, waiting, turnaround, response
    """

    # Copy processes and add remaining time to each
    remaining = [p.copy() for p in processes]
    for p in remaining:
        p['remaining'] = p['burst']

    current_time = 0
    completed    = []
    gantt_chart  = []
    results      = []
    started      = {}   # track first time each process gets CPU { pid: start_time }

    while len(completed) < len(processes):

        # All processes that have arrived and still have work left
        available = [p for p in remaining
                     if p['arrival'] <= current_time and p['remaining'] > 0]

        if not available:
            # CPU idle — jump to next arrival
            next_arrival = min(p['arrival'] for p in remaining if p['remaining'] > 0)
            gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            continue

        # Pick shortest remaining time
        # Tie-break: arrival time, then pid
        selected = min(available, key=lambda p: (p['remaining'], p['arrival'], p['pid']))

        # Record first time on CPU
        if selected['pid'] not in started:
            started[selected['pid']] = current_time

        # Run one tick
        seg_start = current_time
        selected['remaining'] -= 1
        current_time          += 1

        # Add Gantt segment
        gantt_chart.append({'pid': selected['pid'], 'start': seg_start, 'end': current_time})

        # Check if finished
        if selected['remaining'] == 0:
            pid            = selected['pid']
            arrival        = selected['arrival']
            burst          = selected['burst']
            start_time     = started[pid]
            finish_time    = current_time
            waiting_time   = finish_time - arrival - burst
            turnaround_time= finish_time - arrival
            response_time  = start_time  - arrival

            results.append({
                'pid'        : pid,
                'arrival'    : arrival,
                'burst'      : burst,
                'start'      : start_time,
                'finish'     : finish_time,
                'waiting'    : waiting_time,
                'turnaround' : turnaround_time,
                'response'   : response_time
            })
            completed.append(pid)

    return gantt_chart, results