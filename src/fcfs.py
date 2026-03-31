def run_fcfs(processes):
    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda p: p['arrival'])

    current_time = 0
    gantt_chart = []
    results = []

    for process in sorted_processes:
        pid = process['pid']
        arrival = process['arrival']
        burst = process['burst']

        # If CPU is idle, jump to process arrival time
        if current_time < arrival:
            gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': arrival})
            current_time = arrival

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

    return gantt_chart, results