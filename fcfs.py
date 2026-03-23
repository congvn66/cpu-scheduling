class FCFS:
    def __init__(self, processes):
        self.processes = processes
        self.timeline = []
        
    def run(self):
        self.timeline = []
        self.processes.sort(key= lambda p: (p.arrival, p.id))
        time = 0
        for p in self.processes:
            if time < p.arrival:
                self.timeline.append((-1, time, p.arrival))
                time = p.arrival
            p.start = time
            p.finish = p.start + p.burst
            p.waiting = p.start - p.arrival
            p.response = p.waiting
            p.turnaround = p.finish - p.arrival
            self.timeline.append((p.id, p.start, p.finish))
            time = p.finish


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