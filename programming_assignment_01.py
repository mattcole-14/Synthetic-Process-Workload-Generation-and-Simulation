#!/usr/bin/env python3

""" CS 3360: Programming Assignment 01 """

import random 
import math

class Process:
    def __init__(self, pid, inter_arrival_time, arrival_time, service_time):
        self.inter_arrival_time = inter_arrival_time
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time

        self.state = "NEW"

        self.start_time = None
        self.end_time = None


def generate_exponential(rate):
    u = random.random()

    value_seconds = -math.log(1 - u) / rate
    value_ms = round(value_seconds * 1000)

    return value_ms

def generate_processes(num_processes):
    processes = []

    current_arrival_time = 0

    for pid in range(1, num_processes + 1):
        # Inter-arrival time:
        # Exponential distribution with lambda = 2.0 processes/second
        inter_arrival_time = generate_exponential(2.0)

        # Arrival time is cumulative
        current_arrival_time += inter_arrival_time

        # Service time:
        # Mean = 1 second, so lambda = 1.0
        service_time = generate_exponential(1.0)

        process = Process(
            pid,
            inter_arrival_time,
            current_arrival_time,
            service_time)
        
        processes.append(process)

    return processes

def main():
    processes = generate_processes(1000)

    print("process_id | arrival_time | requested_service_time")

    for process in processes:
        print(
            f"{process.pid:<10} | "
            f"{process.arrival_time:<12} | "
            f"{process.service_time}")

if __name__ == "__main__":
    main()