import heapq
class SJFPreemtive:
    def __init__(self, processes):
        self.processes = processes
        self.timeline = []
        
    def run(self):
        self.timeline = []
        self.processes.sort(key = lambda p: (p.arrival))
        ready_queue = []
        time = 0
        i = 0
        last_pid = None

        while i < len(self.processes) or ready_queue:
            while i < len(self.processes) and self.processes[i].arrival <= time:
                p = self.processes[i]
                heapq.heappush(ready_queue, (p.burst, p.arrival, p.id, p))
                i += 1

            if not ready_queue:
                if i < len(self.processes):
                    self.timeline.append((-1, time, self.processes[i].arrival))
                    time = self.processes[i].arrival
                continue

            burst, arrival, pid, p = heapq.heappop(ready_queue)

            if p.response is None:
                p.response = time - p.arrival
            
            if i < len(self.processes):
                next_arrival = self.processes[i].arrival
                run_time = min(burst, next_arrival - time)
            else:
                run_time = burst

            if last_pid == pid:
                self.timeline[-1] = (pid, self.timeline[-1][1], time + run_time)
            else:
                self.timeline.append((pid, time, time + run_time))
                last_pid = pid

            time += run_time
            remain = burst - run_time

            if remain > 0:
                heapq.heappush(ready_queue, (remain, arrival, pid, p))

            else:
                p.finish = time
                p.turnaround = p.finish - p.arrival
                p.waiting = p.turnaround - p.burst
                
                last_pid = None
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