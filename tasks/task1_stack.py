
class Stack:
    def __init__(self):
        self.stack = []
        
    def push(self, item):
        self.stack.append(item)
        pass
        
    def pop(self):
        if len(self.stack) == 0:
            return None
        # Remove item from the end of self.stack (replace return None with working code)
        return self.stack.pop(0)
    
    def at(self, index):
        return self.stack[index]
    
    def len(self):
        return len(self.stack)
