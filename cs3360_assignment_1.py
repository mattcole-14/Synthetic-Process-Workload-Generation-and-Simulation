#!/usr/bin/env python3

""" 
CS 3360: Computing Systems Fundamentals
Synthetic Process Workload Generation and Simulation
Name: Matt Braziel """

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


def generate_exponential(rate, minimum_one=False):
    u = random.random()

    value_seconds = -math.log(1 - u) / rate
    value_ms = round(value_seconds * 1000)

    if minimum_one:
        value_ms = max(1, value_ms)

    return value_ms

def generate_processes(num_processes):
    processes = []
    current_arrival_time = 0

    for pid in range(1, num_processes + 1):
        inter_arrival_time = generate_exponential(2.0)

        current_arrival_time += inter_arrival_time
        service_time = generate_exponential(1.0, minimum_one=True)

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

def calculate_statistics(processes):
    total_complete_time = max(p.end_time for p in processes)

    total_turnaround_time = 0
    total_waiting_time = 0
    total_service_time = 0

    for process in processes:
        turnaround_time = process.end_time - process.arrival_time
        waiting_time = process.start_time - process.arrival_time

        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        total_service_time += process.service_time

    average_turnaround_time = total_turnaround_time / len(processes)
    average_waiting_time = total_waiting_time / len(processes)

    cpu_utilization = (
        total_service_time / total_complete_time
    ) * 100

    throughput = (
        len(processes) / total_complete_time
    ) * 1000

    return {
        "total_complete_time": total_complete_time,
        "average_turnaround_time": average_turnaround_time,
        "average_waiting_time": average_waiting_time,
        "cpu_utilization": cpu_utilization,
        "throughput": throughput
    }

def calculate_generation_statistics(processes):
    number_of_processes = len(processes)

    # arrival time (ms)
    final_arrival_time_ms = processes[-1].arrival_time
    final_arrival_time_seconds = final_arrival_time_ms / 1000

    average_arrival_rate = (
        number_of_processes / final_arrival_time_seconds
    )

    total_service_time_ms = sum(
        process.service_time for process in processes
    )

    average_service_time_ms = (
        total_service_time_ms / number_of_processes
    )

    average_service_time_seconds = average_service_time_ms / 1000

    return {
        "average_arrival_rate": average_arrival_rate,
        "average_service_time": average_service_time_seconds
    }

def write_markdown_output(
    processes,
    cpu_segments,
    generation_statistics,
    statistics,
    filename="cs3360_assignment_1.md"
):
    with open(filename, "w", encoding="utf-8") as file:

        file.write("# CS 3360: Computing Systems Fundamentals\n\n")
        file.write("## Synthetic Process Workload Generation and Simulation\n\n")
        file.write("**Name:** Matt Braziel\n\n")

        # Pwl
        file.write("## Process Workload\n\n")
        file.write(
            "| process_id | arrival_time | requested_service_time |\n"
        )
        file.write(
            "|-----------:|-------------:|-----------------------:|\n"
        )

        for process in processes:
            file.write(
                f"| {process.pid} "
                f"| {process.arrival_time} "
                f"| {process.service_time} |\n"
            )

        # CPU trace
        file.write("\n## CPU Simulation Trace\n\n")
        file.write("| Time (in ms) | CPU Status | PID |\n")
        file.write("|---|---|---:|\n")

        for start, end, status, pid in cpu_segments:
            pid_output = "" if pid is None else pid

            file.write(
                f"| [{start}, {end}) "
                f"| {status} "
                f"| {pid_output} |\n"
            )

        # generation
        file.write("\n## Generation Statistics\n\n")
        file.write("| Statistics | Results |\n")
        file.write("|---|---:|\n")

        file.write(
            "| Expected Average Arrival Rate "
            "| 2.00 processes/sec |\n"
        )

        file.write(
            f"| Computed Average Arrival Rate "
            f"| {generation_statistics['average_arrival_rate']:.2f} "
            f"processes/sec |\n"
        )

        file.write(
            "| Expected Average Service Time "
            "| 1.00 seconds |\n"
        )

        file.write(
            f"| Computed Average Service Time "
            f"| {generation_statistics['average_service_time']:.2f} "
            f"seconds |\n"
        )

        
        # Simulation stats
        file.write("\n## Simulation Statistics\n\n")
        file.write("| Statistics | Results |\n")
        file.write("|---|---:|\n")

        file.write(
            f"| Total Complete Time "
            f"| {statistics['total_complete_time']} ms |\n"
        )

        file.write(
            f"| Average Turnaround Time "
            f"| {statistics['average_turnaround_time']:.2f} ms |\n"
        )

        file.write(
            f"| Average Waiting Time "
            f"| {statistics['average_waiting_time']:.2f} ms |\n"
        )

        file.write(
            f"| Overall CPU Utilization "
            f"| {statistics['cpu_utilization']:.2f}% |\n"
        )

        file.write(
            f"| Overall System Throughput "
            f"| {statistics['throughput']:.2f} processes/sec |\n"
        )

def main():
    processes = generate_processes(1000)

    cpu_segments = run_fifo_simulation(processes)

    print("process_id | arrival_time | requested_service_time")

    for process in processes:
        print(
            f"{process.pid:<10} | "
            f"{process.arrival_time:<12} | "
            f"{process.service_time}"
        )

    generation_statistics = calculate_generation_statistics(processes)

    print("\nTime (in ms) | CPU Status | PID")

    for start, end, status, pid in cpu_segments:
        pid_output = "" if pid is None else pid

        print(
            f"[{start:7d}, {end:7d}) | "
            f"{status:<10} | "
            f"{pid_output}"
        )

    # generation table
    print("\nGeneration Statistics")
    print("------------------------------|------------------")
    print(
        f"Expected Average Arrival Rate | "
        f"2.00 processes/sec"
    )
    print(
        f"Computed Average Arrival Rate | "
        f"{generation_statistics['average_arrival_rate']:.2f} processes/sec"
    )
    print(
        f"Expected Average Service Time | "
        f"1.00 seconds"
    )
    print(
        f"Computed Average Service Time | "
        f"{generation_statistics['average_service_time']:.2f} seconds"
    )

    statistics = calculate_statistics(processes)

    # statistics table 
    print("\nStatistics                    | Results")
    print("------------------------------|------------------")
    print(
        f"Total Complete Time           | "
        f"{statistics['total_complete_time']} ms"
    )
    print(
        f"Average Turnaround Time       | "
        f"{statistics['average_turnaround_time']:.2f} ms"
    )
    print(
        f"Average Waiting Time          | "
        f"{statistics['average_waiting_time']:.2f} ms"
    )
    print(
        f"Overall CPU Utilization       | "
        f"{statistics['cpu_utilization']:.2f}%"
    )
    print(
        f"Overall System Throughput     | "
        f"{statistics['throughput']:.2f} processes/sec"
    )

    write_markdown_output(
        processes,
        cpu_segments,
        generation_statistics,
        statistics
    )

if __name__ == "__main__":
    main()
