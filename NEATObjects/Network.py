from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NEATObjects.Genome import Genome
    
from NEATObjects.Neuron import Neuron
from HelperObjects.ActivationFunctions import Sigmoid

MAX_NODES = 1000000

class Network():
    def __init__(self, genome: 'Genome'):
        self.neurons: dict[int, Neuron] = {}
        
        for i in range(genome.numInputs):
            self.neurons[i] = Neuron()
                
        for o in range(genome.numOutputs):
            self.neurons[MAX_NODES+o] = Neuron()
            
        genome.genes.sort(key=lambda gene: gene.out)
        for gene in genome.genes:
            if gene.enabled:
                if gene.out not in self.neurons:
                    self.neurons[gene.out] = Neuron()
                neuron = self.neurons[gene.out]
                neuron.incoming.append(gene)
                
                if not hasattr(gene, "into"):
                    gene.into = 0
                if gene.into not in self.neurons:
                    self.neurons[gene.into] = Neuron()
                    
        self.neurons = dict(sorted(self.neurons.items()))
                    
                    
    def GetOutputs(self, inputs: list[float], numInputs: int, numOutputs: int, outputThreshold: float) -> dict[int, bool]:
        if len(inputs) != numInputs:
            print(f"Unexpected number of inputs, expected {numInputs} but got {len(inputs)}")
            return

        for i in range(numInputs):
            self.neurons[i].value = inputs[i]
            
        for key, neuron in self.neurons.items():
            sum = 0
            for gene in neuron.incoming:
                connected = self.neurons[gene.into]
                sum += gene.weight*connected.value
                
            if len(neuron.incoming) > 0:
                neuron.value = Sigmoid(sum)
                
        outputs = {}
        for o in range(numOutputs):
            if self.neurons[MAX_NODES+o].value > outputThreshold:
                outputs[o] = True
            else:
                outputs[o] = False
                
        return outputs