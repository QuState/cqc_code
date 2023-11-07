from ch03.util import *
from math import pi, log2, log10, atan2, floor


class Config:
    def __init__(self):
        self.use_mpl_tables = False

    def set_use_mpl_tables(self, mpl=True):
        self.use_mpl_tables = mpl
        if self.use_mpl_tables:
            import matplotlib.pyplot as plt
            self.plt = plt

            from matplotlib import colors, cm
            import colorcet

            cmap = plt.get_cmap('cet_CET_C6')
            norm = colors.Normalize(vmin=0, vmax=360)
            self.scalarMap = cm.ScalarMappable(norm=norm, cmap=cmap)

    def get_use_mpl_tables(self):
        return self.use_mpl_tables


CONFIG = Config()


def show_state_table(state, decimals=4):
    if CONFIG.get_use_mpl_tables():
        state_to_mpl_table(state).show()
    else:
        print_state_table(state, decimals)


def complex_to_rgb(c):
    a = c.real
    b = c.imag

    hue = atan2(b, a)/pi*180
    if hue < 0: hue += 360

    rgb = CONFIG.scalarMap.to_rgba(hue)[:3]

    return rgb


def to_table(s, decimals=4):
    n = int(log2(len(s)))

    round_state = [round(s[k].real, decimals) + 1j*round(s[k].imag, decimals) for k in range(len(s))]
    table = [[k, bin(k)[2:].zfill(n),
              ('+' if round_state[k].real >= 0 else '-') + str(abs(round_state[k].real)).ljust(decimals+2, '0') +
              (' + ' if round_state[k].imag >= 0 else ' - ') + str(abs(round_state[k].imag)).ljust(decimals+2, '0') + '*i',
              abs(s[k]),
              str(0 if s[k] == 0.0 else round(atan2(s[k].imag, s[k].real) / (2 * pi) * 360, 2)) + '\u00b0',
              int(floor(24*abs(s[k])))*'\u2588',
              abs(s[k])**2] for k in range(len(s))]
    table_r = [[round(x, decimals) if isinstance(x, float) else round(x.real, decimals) + 1j*round(x.imag, decimals) if isinstance(x, complex) else x for x in table[k]] for k in range(len(table))]
    return table_r


def state_to_mpl_table(state, highlight=[]):
    assert(CONFIG.get_use_mpl_tables())
    plt = CONFIG.plt

    n_rows = len(state)
    data = to_table(state)

    column_headers = ('Outcome', 'Binary', 'Amplitude', 'Magnitude', 'Direction', 'Amplitude Bar', 'Probability')

    tb = plt.table(cellText=data,
                   rowLoc='right',
                   cellLoc='center',
                   colLabels=column_headers,
                   loc='center')

    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    tb.auto_set_column_width(col=list(range(len(column_headers))))


    plt.axis('tight')
    plt.axis('off')

    tb.scale(2, 2)

    for col in range(len(column_headers)):
        tb[0, col].set_facecolor('lavender')

    for h in highlight:
        for col in range(len(column_headers)):
            tb[h+1, col].set_facecolor('lightyellow')

    bar_index = column_headers.index('Amplitude Bar')
    for row in range(n_rows):
        tb[row+1, bar_index].set_text_props(ha='left', size=16)
        tb[row+1, bar_index].get_text().set_color(complex_to_rgb(state[row]))

    return plt


def print_state_table(state, decimals=4, symbol='\u2588'):
    assert(decimals <= 10)
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j * round(state[k].imag, decimals) for k in range(len(state))]

    headers = ['Outcome', 'Binary', 'Amplitude', 'Magnitude', 'Direction', 'Amplitude Bar', 'Probability']
    offsets = [max(len(headers[0]), floor(log10(len(state)))),               # outcome
               max(len(headers[1]), n),                                      # binary
               max(len(headers[2]), 2*(decimals + 2) + 6),                   # amplitude
               max(len(headers[3]), (decimals + 2)),                         # magnitude
               max(len(headers[4]), decimals),                               # direction
               max(len(headers[5]), 20),                                     # amplitude bar
               max(len(headers[6]), decimals + 2),                           # probability
               ]

    for i in range(len(offsets)):
        headers[i] = headers[i] + ' '*(offsets[i] - len(headers[i]))

    header_str = '  '.join(headers)

    print('\n')
    print(header_str)
    print(len(header_str) * '-')

    for k in range(len(round_state)):

        print('  '.join([str(k).ljust(offsets[0], ' '),

                         str(bin(k)[2:].zfill(n)).ljust(offsets[1] - 1, ' '),

                         ((' ' if round_state[k].real >= 0 else '-') +
                         str(abs(round_state[k].real)).ljust(decimals + 2, '0') +
                         (' + ' if round_state[k].imag >= 0 else ' - ') +
                         str(abs(round_state[k].imag)).ljust(decimals + 2, '0') + '*i').ljust(offsets[2] + 1, ' '),

                         str(round(abs(round_state[k]), decimals)).ljust(offsets[3], ' '),

                         (str(round(atan2(round_state[k].imag, round_state[k].real) * 180 / pi, decimals)) if
                          abs(round_state[k]) > 0 else offsets[4] * ' ').ljust(offsets[4], ' '),

                         (int(abs(round_state[k] * 20)) * symbol).ljust(offsets[5], ' '),

                         str(round(abs(round_state[k]) ** 2, decimals)).ljust(decimals + 2, '0')
                         ]))
