class QuantumCircuit:
    def __init__(self, *args):
        bits = 0
        regs = []
        for register in args:
            register.shift = bits
            bits += register.size
            regs.append(register.size)

        self.state = init_state(bits)
        self.transformations = []
        self.regs = regs
        self.reports = {}

    def initialize(self, state):
        self.state = state

    def h(self, t):
        self.transformations.append(QuantumTransformation(h, t, [], 'h'))

    def x(self, t):
        self.transformations.append(QuantumTransformation(x, t, [], 'x'))

    def cx(self, c, t):
        self.transformations.append(QuantumTransformation(x, t, [c], 'cx'))

    def mcx(self, cs, t):
        self.transformations.append(QuantumTransformation(x, t, cs))

    def run(self):
        for tr in self.transformations:
            cs = tr.controls
            if len(cs) == 0:
                transform(self.state, tr.target, tr.gate)
            elif len(cs) == 1:
                c_transform(self.state, cs[0], tr.target, tr.gate)
            else:
                mc_transform(self.state, cs, tr.target, tr.gate)
        self.transformations = []
        return self.state

    def measure(self, shots):
        return measure(self.state, shots)