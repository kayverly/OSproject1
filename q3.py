from typing import List
from process import Process, Processor
from processors import data, calculate

def better_sjf_memory():
    processes: List[Process] = data()
    processes.sort(key=lambda x: x.cpu_cycles)
    for process in processes:
        process.arrival_time = 0
    slow_processors: List[Processor] = [Processor() for i in range(3)] #2 GHz list
    fast_processors: List[Processor] = [Processor() for i in range(3)] #4 GHz list
    for i, cu_process in enumerate(processes[:3]): # first 3 processes with the shortest cycles
        slow_processors[i].add(process=cu_process)
        cu_process.evaluate()
    for i, cu_process in enumerate(processes[-3:]): # last 3 process which are the longest cycles
        fast_processors[i].add(process=cu_process)
        fast_eval(cu_process)

    processes_left = processes[3:-3]
    time = 0
    skip = False 

    while processes_left:
        s_first_available = min(slow_processors, key=lambda x: x.tail.cycles_left)
        f_first_available = min(fast_processors, key=lambda x: x.tail.cycles_left)
        slow = (s_first_available.tail.cycles_left < f_first_available.tail.cycles_left
            ) if not skip else False
        next_process = processes_left.pop(0)
        length = len(processes_left)
        if slow: 
            check = True
            while check:
                if next_process.memory > 8000:
                    processes_left.append(next_process)
                    next_process = processes_left.pop(0)
                    length -= 1
                    if length < 0:
                        skip = True
                        check = False
                        processes_left.append(next_process)
                else:
                    check = False

        index_done = (slow_processors.index(s_first_available)
            if slow
            else fast_processors.index(f_first_available))
        
        time = (s_first_available.tail.turnaround_time
            if slow
            else f_first_available.tail.turnaround_time)
            
        for processor in slow_processors:
            process = processor.tail
            process.cycles_left = process.cpu_cycles + process.wait_time - time
            if skip and process.cycles_left < 0:
                process.cycles_left = 0

        for processor in fast_processors:
            process = processor.tail
            process.cycles_left = (process.cpu_cycles + process.wait_time - time) // 2

        if slow:
            if not skip:
                slow_processors[index_done].add(next_process)
                next_process.evaluate()
        else:
            fast_processors[index_done].add(next_process)
            fast_eval(next_process)

    print(time)
    return slow_processors + fast_processors

def fast_eval(process: Process) -> None:
    process.evaluate()
    process.cycles_left //= 2
    process.turnaround_time -= (process.cpu_cycles // 2)


calculate(better_sjf_memory())