from math import log2

def bin_digit(k, j):
    return 1 if k & (1 << j) else 0

def cfft(state):
    n = int(log2(len(state)))
    for j in range(n)[::-1]:
        for k in range(len(state)):
            if bin_digit(k, j) == 0:
                state[k] = 1/sqrt(2)*(state[k] + state[k+2**j])
                state[k+2**j] = state[k] - sqrt(2)*state[k+2**j]

            else:
                state[k] *= cis(-pi * (k%2**j)*2**-j)