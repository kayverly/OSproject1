import csv
from typing import List
from process import Process, Processor

def data():
    processes = []

    with open("processes.csv", encoding="utf8") as csvfile:
        next(csvfile)
        input = csv.reader(csvfile)
        for pid, cpu_cycles, memory in input:
            processes.append(Process(pid=int(pid), cpu_cycles=int(cpu_cycles), memory=int(memory)))
        return processes

   
# FIFO program for question 1 part 1
def fifo():
    processes: List[Process] = data()
    for process in processes:
        process.arrival_time = 0
    processors: List[Processor] = [Processor() for i in range(6)]
    for i, cu_process in enumerate(processes[:6]):
        processors[i].add(process=cu_process)
        cu_process.evaluate()
    
    proccesses_left = processes[6:]
    time = 0
    while(proccesses_left):
        next_process = proccesses_left.pop(0)
        first_available = min(processors, key=lambda x: x.tail.cycles_left)
        time = first_available.tail.turnaround_time
        for processor in processors:
            process = processor.tail
            process.cycles_left = process.cpu_cycles + process.wait_time - time
        fastest_done_index = processors.index(first_available)
        processors[fastest_done_index].add(next_process)

        next_process.evaluate()
    print(time)
    return processors

def sjf(): 
    processes: List[Process] = data()
    processes.sort(key=lambda x: x.cpu_cycles)
    for process in processes:
        process.arrival_time = 0
    processors: List[Processor] = [Processor() for i in range(6)]
    for i, cu_process in enumerate(processes[:6]):
        processors[i].add(process=cu_process)
        cu_process.evaluate()
    
    proccesses_left = processes[6:]
    time = 0
    while(proccesses_left):
        next_process = proccesses_left.pop(0)
        first_available = min(processors, key=lambda x: x.tail.cycles_left)
        time = first_available.tail.turnaround_time
        for processor in processors:
            process = processor.tail
            process.cycles_left = process.cpu_cycles + process.wait_time - time
        fastest_done_index = processors.index(first_available)
        processors[fastest_done_index].add(next_process)

        next_process.evaluate()
    print(time)
    return processors

def rrobin():
    processes: List[Process] = data()
    for process in processes:
        process.arrival_time = 0
    processors: List[Processor] = [Processor() for i in range(6)]
    for i, cu_process in enumerate(processes[:6]):
        processors[i].add(process=cu_process)
        processes_left = processes[6:]
        time_quantum = 10*(10**10)
        time = [0 for i in range(6)]

    while(processes_left):
        for i, processor in enumerate(processors):
            process = processor.tail
            if process.cycles_left <= time_quantum:
                process.wait_time = (
                    time[i] - process.cpu_cycles + process.cycles_left
                )
                process.cycles_left = 0
                process.turnaround_time = process.wait_time + process.cpu_cycles
                if processes_left:
                    new_process = processes_left.pop(0)
                    processors[i].add(new_process)
            else:
                time[i] += time_quantum
                process.cycles_left -= time_quantum
                if processes_left:
                    processors[i].remove()
                    processes_left.append(process)
                    new_process = processes_left.pop(0)
                    processors[i].add(new_process)
    for i, processor in enumerate(processors):
        process = processor.tail
        process.wait_time = time[i] - process.cpu_cycles + process.cycles_left
        process.cycles_left = 0
        process.turnaround_time = process.wait_time + process.cpu_cycles
    print(time)
    return processors

# Calculate the average wait time and average turnaround time 
def calculate(processors: List[Processor]):
    index = 1
    for processor in processors:
        total_processes = 0
        total_wait = 0
        total_turnaround = 0
    
        for process in processor:
            total_processes += 1
            total_wait += process.wait_time
            total_turnaround += process.turnaround_time
        
        print(f"Processor {index} had {total_processes} processes. The average wait time was {total_wait/total_processes} and the average turnaround time was {total_turnaround/total_processes}")
        index += 1
