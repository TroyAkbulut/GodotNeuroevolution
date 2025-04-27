from __future__ import annotations

class Gene():
    def __init__(self):
        self.into = 0
        self.out = 0
        self.weight = 0.0
        self.enabled = True
        self.innovation = 0
        
    def CopyGene(self) -> Gene:
        newGene = Gene()
        newGene.into = self.into
        newGene.out = self.out
        newGene.weight = self.weight
        newGene.enabled = self.enabled
        newGene.innovation = self.innovation

        return newGene
