class Process:
    def __init__(self, id, arrival, burst, start = None, finish = None, waiting = None, response = None, turnaround = None, priority=None):
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

        # metric
        self.start = start
        self.finish = finish
        self.waiting = waiting
        self.response = response
        self.turnaround = turnaround

        # MLFQ
        self.remaining = burst
        self.level = 0