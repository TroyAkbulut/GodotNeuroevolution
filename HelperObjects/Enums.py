import enum
    
class Signals(int, enum.Enum):
    START = 1
    REQUEST = 2
    DATA = 3
    STOP = 4
    TEST = -1
       
class Moves(int, enum.Enum):
    LEFT = 0
    RIGHT = 1
    JUMP = 2