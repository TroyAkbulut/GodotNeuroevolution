from NEATObjects.Gene import Gene

class Neuron():
    def __init__(self):
          self.incoming: list[Gene] = []
          self.value = 0.0