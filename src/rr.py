"""
rr.py — Round Robin Scheduling
Person 2
"""


def run_rr(processes, quantum):
    """
    Round Robin with configurable time quantum.

    Parameters:
        processes : list of dicts with keys: pid, arrival, burst
        quantum   : time slice in clock ticks

    Returns:
        gantt_chart : list of dicts with keys: pid, start, end
        results     : list of dicts with keys: pid, arrival, burst,
                      start, finish, waiting, turnaround, response
    """

    # Copy processes and add remaining time to each
    remaining = [p.copy() for p in processes]
    for p in remaining:
        p['remaining'] = p['burst']

    remaining.sort(key=lambda p: (p['arrival'], p['pid']))

    current_time = 0
    queue        = []
    gantt_chart  = []
    results      = []
    arrived      = set()
    started      = {}   # { pid: first_start_time }
    finish_time  = {}   # { pid: finish_time }

    # Enqueue processes that arrive at time 0
    for p in remaining:
        if p['arrival'] == 0:
            queue.append(p)
            arrived.add(p['pid'])

    while len(finish_time) < len(processes):

        if not queue:
            # CPU idle — jump to next arrival
            future       = [p for p in remaining if p['pid'] not in arrived]
            next_arrival = min(p['arrival'] for p in future)
            gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            for p in sorted(remaining, key=lambda x: (x['arrival'], x['pid'])):
                if p['arrival'] <= current_time and p['pid'] not in arrived:
                    queue.append(p)
                    arrived.add(p['pid'])
            continue

        current   = queue.pop(0)
        seg_start = current_time

        # Record first time on CPU
        if current['pid'] not in started:
            started[current['pid']] = current_time

        # Run for up to quantum ticks
        run_ticks = min(quantum, current['remaining'])

        for _ in range(run_ticks):
            current_time        += 1
            current['remaining']-= 1
            # Check for new arrivals each tick
            for p in sorted(remaining, key=lambda x: (x['arrival'], x['pid'])):
                if p['arrival'] <= current_time and p['pid'] not in arrived:
                    queue.append(p)
                    arrived.add(p['pid'])

        gantt_chart.append({'pid': current['pid'], 'start': seg_start, 'end': current_time})

        if current['remaining'] == 0:
            finish_time[current['pid']] = current_time
        else:
            queue.append(current)

    # Build results
    proc_map = {p['pid']: p for p in remaining}
    for pid, ft in finish_time.items():
        p               = proc_map[pid]
        arrival         = p['arrival']
        burst           = p['burst']
        start_time      = started[pid]
        waiting_time    = ft - arrival - burst
        turnaround_time = ft - arrival
        response_time   = start_time - arrival

        results.append({
            'pid'        : pid,
            'arrival'    : arrival,
            'burst'      : burst,
            'start'      : start_time,
            'finish'     : ft,
            'waiting'    : waiting_time,
            'turnaround' : turnaround_time,
            'response'   : response_time
        })

    results.sort(key=lambda x: x['arrival'])
    return gantt_chart, results