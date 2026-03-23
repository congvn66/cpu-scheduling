import heapq
class RoundRobin:
    def __init__(self, processes, quantum = 8):
        self.processes = processes
        self.timeline = []
        self.quantum = quantum
        
    def run(self):
        self.timeline = []
        self.processes.sort(key = lambda p: (p.arrival))
        ready_queue = []
        time = 0
        i = 0
        last_id = None

        while i < len(self.processes) or ready_queue:
            while i < len(self.processes) and self.processes[i].arrival <= time:
                p = self.processes[i]
                ready_queue.append((p.id, p.burst, p))
                i += 1
            

            if not ready_queue:
                if i < len(self.processes):
                    self.timeline.append((-1, time, self.processes[i].arrival))
                    time = self.processes[i].arrival
                continue

            id, burst, p = ready_queue.pop(0)

            if p.response is None:
                p.response = time - p.arrival

            actual_run = min(burst, self.quantum)
            self.timeline.append((id, time, time + actual_run))
            
            time = time + actual_run
            remain = burst - actual_run

        
            while i < len(self.processes) and self.processes[i].arrival <= time:
                p_new = self.processes[i]
                ready_queue.append((p_new.id, p_new.burst, p_new))
                i += 1

           
            if remain > 0:
                ready_queue.append((id, remain, p))
            
            else:
                p.finish = time
                p.turnaround = p.finish - p.arrival
                p.waiting = p.turnaround - p.burst
                
                #last_pid = None
            
        return self.timeline

    def avg_waiting(self):
        total = 0
        for p in self.processes:
            total = total + p.waiting

        avg = total / len(self.processes)
        return avg
    
    def avg_response(self):
        total = 0
        for p in self.processes:
            total = total + p.response

        avg = total / len(self.processes)
        return avg
    
    def avg_turnaround(self):
        total = 0
        for p in self.processes:
            total = total + p.turnaround

        avg = total / len(self.processes)
        return avg
    
    def cpu_switches(self):
        return max(0, len(self.timeline) - 1)