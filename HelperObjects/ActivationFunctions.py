import math

def Sigmoid(x):
    return 1/(1+math.exp(x*-4.9))

def Relu(x):
    return min(x, 0)

def Linear(x):
    return x