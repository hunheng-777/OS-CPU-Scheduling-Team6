"""
mlfq.py — Multilevel Feedback Queue
Person 3
"""


def run_mlfq(processes, quantum=2):
    """
    Multilevel Feedback Queue scheduler.

    Parameters:
        processes : list of dicts with keys: pid, arrival, burst
        quantum   : time quantum for Q1 (Q2 uses quantum * 2)

    Returns:
        gantt_chart : list of dicts with keys: pid, start, end
        results     : list of dicts with keys: pid, arrival, burst,
                      start, finish, waiting, turnaround, response
    """

    q1_quantum  = quantum
    q2_quantum  = quantum * 2
    aging_limit = 10

    jobs = []
    for p in processes:
        jobs.append({
            "pid"      : p["pid"],
            "arrival"  : p["arrival"],
            "burst"    : p["burst"],
            "remaining": p["burst"],
            "level"    : 1,
            "waited"   : 0,
            "finish"   : 0,
            "first_run": -1,
            "added"    : False,
        })

    q1, q2, q3  = [], [], []
    gantt_chart = []
    t           = 0

    while True:

        for job in jobs:
            if job["arrival"] == t and not job["added"]:
                q1.append(job)
                job["added"] = True

        if all(job["remaining"] == 0 for job in jobs):
            break

        current_job = (q1 or q2 or q3 or [None])[0]
        for queue in [q2, q3]:
            for job in queue[:]:
                if job is current_job:
                    continue
                job["waited"] += 1
                if job["waited"] >= aging_limit:
                    queue.remove(job)
                    job["level"]  = 1
                    job["waited"] = 0
                    q1.append(job)

        if q1:
            queue       = q1
            cur_quantum = q1_quantum
            level       = 1
        elif q2:
            queue       = q2
            cur_quantum = q2_quantum
            level       = 2
        elif q3:
            queue       = q3
            cur_quantum = None
            level       = 3
        else:
            t += 1
            continue

        job = queue[0]

        if job["first_run"] == -1:
            job["first_run"] = t

        if level in [1, 2]:
            ran = 0

            for _ in range(cur_quantum):
                ran              += 1
                job["remaining"] -= 1
                t                += 1

                for other in jobs:
                    if other["arrival"] == t and not other["added"]:
                        other["added"] = True
                        q1.append(other)

                if level > 1 and q1:
                    break

                if job["remaining"] == 0:
                    break

            gantt_chart.append({"pid": job["pid"], "start": t - ran, "end": t})

            if job["remaining"] == 0:
                job["finish"] = t
                queue.remove(job)
            elif ran == cur_quantum and level == 1:
                queue.remove(job)
                job["level"]  = 2
                job["waited"] = 0
                q2.append(job)
            elif ran == cur_quantum and level == 2:
                queue.remove(job)
                job["level"]  = 3
                job["waited"] = 0
                q3.append(job)
            else:
                queue.remove(job)
                queue.append(job)

        else:
            ran = 0

            while job["remaining"] > 0:
                ran              += 1
                job["remaining"] -= 1
                t                += 1

                for other in jobs:
                    if other["arrival"] == t and not other["added"]:
                        other["added"] = True
                        q1.append(other)

                if q1:
                    break

            gantt_chart.append({"pid": job["pid"], "start": t - ran, "end": t})

            if job["remaining"] == 0:
                job["finish"] = t
                queue.remove(job)
            else:
                queue.remove(job)
                queue.append(job)

    results = []
    for job in jobs:
        turnaround = job["finish"]    - job["arrival"]
        waiting    = turnaround       - job["burst"]
        response   = job["first_run"] - job["arrival"]
        results.append({
            "pid"       : job["pid"],
            "arrival"   : job["arrival"],
            "burst"     : job["burst"],
            "start"     : job["first_run"],
            "finish"    : job["finish"],
            "waiting"   : waiting,
            "turnaround": turnaround,
            "response"  : response,
        })

    return gantt_chart, results