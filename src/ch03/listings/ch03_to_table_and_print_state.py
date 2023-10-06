from math import atan2, pi

def to_table(s, decimals=5):
    table = [[k, s[k], atan2(s[k].imag, s[k].real) / (2 * pi) * 360, abs(s[k]), abs(s[k])**2] for k in range(len(s))] (1)
    table_r = [[round(x, decimals) if isinstance(x, float) else round(x.real) + 1j*round(x.imag, decimals) if isinstance(x, complex) else x for x in table[k]] for k in range(len(table))] (2)

    return table_r

def print_state(state, decimals=5):  (3)
    print(*to_table(state, decimals),sep='\n')
