class HashTable:
    def __init__(self, size=1024):
        self.table = [[] for i in range(size)]
        self.size = size

    def contains_anything(self):
        return any(self.table)

    def insert(self, item):
        # Add code to insert into the Hash Table (self.table) here
        pass

    def contains(self, item) -> bool:
        # Add code to check if an item is in self.table and return True if it is
        # And False otherwise
        return False

