from ch06.util import *
from math import log2
import matplotlib.pyplot as plt
from sty import fg


def rev(n, k):
    return int(bin(k)[2:].zfill(n)[::-1], 2)


def padded_bin(n, k):
    return bin(k)[2:].zfill(n)


def reverse_index_state(state):
    n = int(log2(len(state)))
    s = state.copy()
    for k in range(len(state)):
        s[k] = state[int(padded_bin(n, k)[::-1], 2)]
    return s


def inner(v1, v2):
    assert(len(v1) == len(v2))
    return sum(z1*z2.conjugate() for z1, z2 in zip(v1, v2))


def list_to_dict(state, show_binary=True):
    n = int(log2(len(state)))
    return dict(zip([str(k) + (('=' + padded_bin(n, k)) if show_binary else '') for k in range(len(state))],
                    [state[k] for k in range(len(state))]))


def plot_bars(bars, title, title_x, title_y, color=None, fig_name=None, action=lambda plt: None):
    if isinstance(bars, list):
        bars = dict(zip(range(len(bars)), bars))
    _, ax = plt.subplots()

    y_position = range(len(bars))
    ax.bar(y_position, [abs(v) for v in bars.values()], align='center', #width=0.257,
           color=color if color is not None else [[x for x in complex_to_rgb(round(v, 5))] for v in bars.values()])
    plt.xticks(y_position, bars.keys())
    if len(bars) > 16:
        plt.xticks(rotation=90, fontsize=10)
    else:
        plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title)
    plt.tight_layout()
    fig = plt.gcf()
    action(ax)
    plt.show()
    if fig_name:
        fig.savefig(fig_name)
     
    
def state_table_to_string(state, decimals=4, symbol='\u2588'):
    assert(decimals <= 10)
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j * round(state[k].imag, decimals) for k in range(len(state))]

    headers = ['Outcome', 'Binary', 'Amplitude', 'Magnitude', 'Direction', 'Amplitude Bar', 'Probability']
    offsets = [max(len(headers[0]), floor(log10(len(state)))),               # outcome
               max(len(headers[1]), n),                                      # binary
               max(len(headers[2]), 2*(decimals + 2) + 6),                   # amplitude
               max(len(headers[3]), (decimals + 2)),                         # magnitude
               max(len(headers[4]), decimals),                               # direction
               max(len(headers[5]), 24),                                     # amplitude bar
               max(len(headers[6]), decimals + 2),                           # probability
               ]

    for i in range(len(offsets)):
        headers[i] = headers[i] + ' '*(offsets[i] - len(headers[i]))

    header_str = '  '.join(headers)

    output = '\n'
    output += header_str
    output += '\n'
    output += len(header_str) * '-'
    output += '\n'

    for k in range(len(round_state)):
        direction = round(atan2(round_state[k].imag, round_state[k].real) * 180 / pi, 2)

        output += '  '.join([str(k).ljust(offsets[0], ' '),

                             str(bin(k)[2:].zfill(n)).ljust(offsets[1] - 1, ' '),

                             ((' ' if round_state[k].real >= 0 else '-') +
                              str(abs(round_state[k].real)).ljust(decimals + 2, '0') +
                              (' + ' if round_state[k].imag >= 0 else ' - ') + 'i' +
                              str(abs(round_state[k].imag)).ljust(decimals + 2, '0')).ljust(offsets[2] + 1, ' '),

                             str(round(abs(state[k]), decimals)).ljust(decimals + 2, ' ').ljust(offsets[3], ' '),

                             (str(((' ' if direction >= 0 else '-') + str(floor(abs(direction)))).rjust(4, ' ') +
                                  '.' + str(int(100*round(direction - floor(direction), 2))).ljust(2, '0')) + '\u00b0' if
                              abs(round_state[k]) > 0 else offsets[4] * ' ').ljust(offsets[4], ' '),

                             fg(*[int(255*a) for a in complex_to_rgb(state[k])]) + (int(abs(state[k] * 24)) * symbol).ljust(offsets[5], ' ') + fg.rs,

                             str(round(abs(state[k]) ** 2, decimals)).ljust(decimals + 2, ' ')
                             ])
        output += '\n'

    return output


def print_state_table(state, decimals=4, symbol='\u2588'):
    print(state_table_to_string(state, decimals, symbol))