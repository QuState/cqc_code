def qft(self, targets, swap=True):
    for j in range(len(targets))[::-1]:
        self.h(targets[j])
        for k in range(j)[::-1]:
            self.cp(pi * 2.0 ** (k - j), targets[j], targets[k])

    if swap:
        self.mswap(targets)

def iqft(self, targets, swap=True):
    for j in range(len(targets))[::-1]:
        self.h(targets[j])
        for k in range(j)[::-1]:
            self.cp(-pi * 2 ** (k - j), targets[j], targets[k])

    if swap:
        self.mswap(targets)