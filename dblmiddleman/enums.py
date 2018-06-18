from enum import Enum

class VoteType(Enum):
    upvote = "upvote"
    test   = "test"
    
    def __str__(self):
        return self.name

def try_enum(cls, val):
    try:
        return cls(val)
    except ValueError:
        return val