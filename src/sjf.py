def run_sjf(processes):
   

    # Copy processes to avoid modifying original
    remaining = [p.copy() for p in processes]

    current_time = 0
    gantt_chart = []
    results = []
    completed = []

    while len(completed) < len(processes):
        # Get all processes that have arrived and not yet completed
        available = [p for p in remaining if p['arrival'] <= current_time]

        if not available:
            # CPU is idle, jump to next arrival
            next_arrival = min(p['arrival'] for p in remaining)
            gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': next_arrival})
            current_time = next_arrival
            continue

        # Pick process with shortest burst time (SJF logic)
        # If tie in burst time, pick the one that arrived first
        selected = min(available, key=lambda p: (p['burst'], p['arrival']))

        pid = selected['pid']
        arrival = selected['arrival']
        burst = selected['burst']

        start_time = current_time
        finish_time = current_time + burst

        # Calculate metrics
        waiting_time = start_time - arrival
        turnaround_time = finish_time - arrival
        response_time = start_time - arrival  # Same as waiting for non-preemptive

        gantt_chart.append({'pid': pid, 'start': start_time, 'end': finish_time})

        results.append({
            'pid': pid,
            'arrival': arrival,
            'burst': burst,
            'start': start_time,
            'finish': finish_time,
            'waiting': waiting_time,
            'turnaround': turnaround_time,
            'response': response_time
        })

        current_time = finish_time
        completed.append(pid)
        remaining = [p for p in remaining if p['pid'] != pid]

    return gantt_chart, results