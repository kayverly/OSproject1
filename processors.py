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
        

