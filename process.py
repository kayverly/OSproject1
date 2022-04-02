from __future__ import annotations
from typing import Iterable, Iterator

class Process:

    def __init__(self, pid: int, cpu_cycles: int, memory: int) -> None:
        self.pid: int = pid
        self.cpu_cycles: int = cpu_cycles
        self.memory = memory
        self.cycles_left: int = cpu_cycles
        self.arrival_time: float = None
        self.wait_time: float = None
        self.turnaround_time: float = None
        self.next_process: Process = None
        self.prev_process: Process = None

    def printStr(self) -> str:
        return f'Process(PID: {self.pid}, Cycles: {self.cpu_cycles}, Memory Requirement: {self.memory}'

    @property
    def next(self) -> Process:
        return self.next_process

    @next.setter
    def next(self, next_process: Process) -> None:
        next_process.prev_process = self
        self.next_process = next_process
    
    def evaluate(self):
        self.wait_time = (
            self.prev_process.turnaround_time - self.arrival_time
            if self.prev_process is not None
            else self.arrival_time)
        self.turnaround_time = self.wait_time + self.cpu_cycles

class Processor(Iterator, Iterable):
    assigned_work = 0

    def __init__(self) -> None:
        self.head: Process = None
        self.tail: Process = None
        self.next: Process = None
    
    def __iter__(self):
        self.next = self.head
        return self
    
    def __next__(self):
        if self.next is not None:
            x = self.next
            self.next = self.next.next
            return x
        raise StopIteration

    def add(self, process: Process) -> None:
        if self.head is None and self.tail is None:
            self.head = process
            self.tail = process
        else: 
            self.tail.next = process
            self.tail = process
    def remove(self) -> Process:
        if self.head is None and self.tail is None:
            return None
        if self.head is self.tail:
            process = self.head
            self.head = None
            self.tail = None
            return process
        process = self.tail
        process.prev_process.next_process = None
        self.tail = process.prev_process
        return process
