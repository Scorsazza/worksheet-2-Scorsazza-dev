class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        pass

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        # Remove item from the end of self.queue (replace return None with working code)
        return self.queue.pop(0)

    def at(self, index):
        return self.queue[index]

    def len(self):
        return len(self.queue)
