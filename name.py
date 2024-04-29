# a simple class that keeps track of a first, last, and middle name
class Name:
    ''' A class that keeps track of a first, last, and (optional) middle name'''
    def __init__(self, first, last, middle = None):
        self.first = first
        self.last = last
        self.middle = middle
    
    def __str__(self):
        if self.middle:
            return f"{self.first} {self.middle} {self.last}"
        return f"{self.first} {self.last}"