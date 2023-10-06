from random import choices
from collections import Counter

def measure(state, shots):
    samples = choices(range(len(state)), [abs(state[k])**2 for k in range(len(state))], k=shots)
    counts = {}
    for (k, v) in Counter(samples).items():
        counts[k] = v
    return counts