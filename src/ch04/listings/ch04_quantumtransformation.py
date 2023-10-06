class QuantumTransformation:
    def __init__(self, gate, target, controls=[], name=None, arg=None):
        self.gate = gate
        self.target= target
        self.controls = controls
        self.name = name
        self.arg = arg