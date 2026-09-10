#!/usr/bin/env python3

""" CS 3360: Programming Assignment 01 """

import random 
import math
from collections import deque

class Process:
    def __init__(self, pid, inter_arrival_time, arrival_time, service_time):
        self.inter_arrival_time = inter_arrival_time
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time

        self.state = "NEW"
        self.start_time = None
        self.end_time = None
        self.remaining_time = service_time


def generate_exponential(rate):
    u = random.random()
    value_seconds = -math.log(1 - u) / rate
    
    #preventing 0 ms 
    value_ms = max(1, round(value_seconds * 1000))

    return value_ms

def generate_processes(num_processes):
    processes = []

    current_arrival_time = 0

    for pid in range(1, num_processes + 1):
        inter_arrival_time = generate_exponential(2.0)
        current_arrival_time += inter_arrival_time

        # lambda = 1.0
        service_time = generate_exponential(1.0)

        process = Process(
            pid,
            inter_arrival_time,
            current_arrival_time,
            service_time)
        
        processes.append(process)

    return processes

def add_cpu_segment(segments, start, end, status, pid):
    if (
        segments
        and segments[-1][2] == status
        and segments[-1][3] == pid
        and segments[-1][1] == start
    ):
        segments[-1] = (
            segments[-1][0],
            end,
            status,
            pid
        )
    else:
        segments.append(
            (start, end, status, pid)
        )

def run_fifo_simulation(processes):
    ready_queue = deque()

    current_process = None
    current_time = 0
    next_process = 0
    completed_processes = 0

    cpu_segments = []

    while completed_processes < len(processes):

        while (
            next_process < len(processes)
            and processes[next_process].arrival_time <= current_time
        ):
            process = processes[next_process]
            process.state = "READY"
            ready_queue.append(process)
            next_process += 1

        if current_process is None and ready_queue:
            current_process = ready_queue.popleft()
            current_process.state = "RUNNING"

            if current_process.start_time is None:
                current_process.start_time = current_time

        if current_process is not None:
            add_cpu_segment(
                cpu_segments,
                current_time,
                current_time + 1,
                "BUSY",
                current_process.pid
            )

            current_process.remaining_time -= 1

            if current_process.remaining_time == 0:
                current_process.end_time = current_time + 1
                current_process.state = "TERMINATED"

                completed_processes += 1
                current_process = None

        else:
            add_cpu_segment(
                cpu_segments,
                current_time,
                current_time + 1,
                "IDLE",
                None
            )

        current_time += 1

    return cpu_segments

def main():
    processes = [
        Process(1, 1, 1, 2),
        Process(2, 1, 2, 7),
        Process(3, 11, 13, 4)]

    cpu_segments = run_fifo_simulation(processes)

    print("Time (in ms) | CPU Status | PID")

    for start, end, status, pid in cpu_segments:
        pid_output = "" if pid is None else pid

        print(
            f"[{start:4d}, {end:4d}) | "
            f"{status:<10} | "
            f"{pid_output}"
        )

if __name__ == "__main__":
    main()
