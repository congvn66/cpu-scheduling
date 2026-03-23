class MLFQ:
    def __init__(self, processes, levels):
        """
        levels: list config for queues
        """
        self.processes = processes
        self.levels = levels
        self.k = len(levels)

        self.queues = [[] for _ in range(self.k)]
        self.timeline = []