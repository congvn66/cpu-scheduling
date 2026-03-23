import heapq
class SJFNonPreemtive:
    def __init__(self, processes):
        self.processes = processes
        self.timeline = []
        
    def run(self):
        self.timeline = []
        self.processes.sort(key = lambda p: (p.arrival))
        ready_queue = []
        time = 0
        i = 0

        while i < len(self.processes) or ready_queue:
            while i < len(self.processes) and self.processes[i].arrival <= time:
                p = self.processes[i]
                heapq.heappush(ready_queue, (p.burst, p.arrival, p.id, p))
                i += 1

            if ready_queue:
                burst, arrival, pid, p = heapq.heappop(ready_queue)
                p.start = time
                p.finish = p.start + burst
                p.waiting = p.start - arrival
                p.response = p.waiting
                p.turnaround = p.finish - p.arrival
                self.timeline.append((p.id, p.start, p.finish))
                time = p.finish
        
            else:
                if i < len(self.processes):
                    self.timeline.append((-1, time, self.processes[i].arrival))
                    time = self.processes[i].arrival
        return self.timeline

    def avg_waiting(self):
        total = 0
        for p in self.processes:
            total = total + p.waiting

        avg = total / len(self.processes)
        return avg
    
    def avg_response(self):
        return self.avg_waiting()
    
    def avg_turnaround(self):
        total = 0
        for p in self.processes:
            total = total + p.turnaround

        avg = total / len(self.processes)
        return avg
    
    def cpu_switches(self):
        return max(0, len(self.timeline) - 1)