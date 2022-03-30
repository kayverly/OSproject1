from queue import Queue
import csv
import queue
import numpy as np

processes = Queue()
pid = []
cycles = []
memory = []
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []
p6 = []
turn_time = 0

csvfile = open("processes.csv", "r")
file = csv.DictReader(csvfile)
for process in file:
    pid.append(process["Process ID"])
    cycles.append(process["CPU Cycles"])
    memory.append(process["Memory Requirement"])
    processes.put(process)

# FIFO program for question 1 part 1
def fifo():
    for i in range(42):
        p1.append(processes.get())
        p2.append(processes.get())
        p3.append(processes.get())
        p4.append(processes.get())
    for i in range(41):
        p5.append(processes.get())
        p6.append(processes.get())

    wait_time = 0
    turn_time = 0

    for i, value in enumerate(p1):
        turn_time += int(value)


    p1_avg_turn_time = turn_time / len(p1)
    print("average wait time is: " + str(p1_avg_turn_time))




