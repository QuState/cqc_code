from math import pi, atan2, log2, log10

from ch05.util import *


def print_state_table(state, decimals=4):
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j*round(state[k].imag, decimals) for k in range(len(state))]
    symbol = '#'
    print('\n')
    print((' ').join(['Outcome', (2*' ') + 'Binary', (7*' ') + 'Amplitude', (7*' ') + 'Magnitude', (2*' ') + 'Direction', (5*' ') + 'Amplitude Bar', (8*' ') + 'Probability']))
    print(100*'-')
    for k in range(len(round_state)):
        print((5*' ').join([str(k).rjust(2 + int(log10(len(state)))+1, ' '),
                            str(bin(k)[2:].zfill(n)).rjust(6, ' '),
                            ('+' if round_state[k].real >= 0 else '-') + str(abs(round_state[k].real)).ljust(decimals+2, '0') +
                            (' + ' if round_state[k].imag >= 0 else ' - ') + str(abs(round_state[k].imag)).ljust(decimals+2, '0') + '*i',
                            str(round(abs(round_state[k]), decimals)).ljust((decimals+2), '0'),
                            (str(round(atan2(round_state[k].imag, round_state[k].real)*180/pi, 2)) if abs(round_state[k]) > 0 else (decimals+5)*'').ljust((decimals+5), ' '),
                            (int(abs(round_state[k] * 20)) * symbol).ljust(20, ' '),
                            str(round(abs(round_state[k])**2, decimals))
                            ]))