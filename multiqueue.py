class MultilevelQueueSimple:
    def __init__(self, queues, schedulers):
        self.queues = queues
        self.schedulers = schedulers
        self.timeline = []

    def run(self):
        self.timeline = []
        for queue, scheduler in zip(self.queues, self.schedulers):
            queue_timeline = scheduler(queue)
            self.timeline.extend(queue_timeline)
        return self.timeline
    
    def avg_waiting(self):
        total = 0
        n = 0
        for queue in self.queues:
            for p in queue:
                total += p.waiting
                n += 1
        return total / n

    def avg_turnaround(self):
        total = 0
        n = 0
        for queue in self.queues:
            for p in queue:
                total += p.turnaround
                n += 1
        return total / n

    def avg_response(self):
        total = 0
        n = 0
        for queue in self.queues:
            for p in queue:
                total += p.response
                n += 1
        return total / n