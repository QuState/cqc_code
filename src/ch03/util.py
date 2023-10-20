from math import cos, sin


def is_close_float(a, b, rtol=1e-5, atol=1e-8):
    return abs(a - b) < atol + rtol * abs(b)


def is_close(a, b):
    if isinstance(a, float):
        a = complex(a, 0)

    if isinstance(b, float):
        b = complex(b, 0)

    return is_close_float(a.real, b.real) and is_close_float(a.imag, b.imag)


def all_close(state1, state2):
    for (a, b) in zip(state1, state2):
        if not is_close(a, b):
            return False
    return True


def cis(theta):
    return cos(theta) + 1j*sin(theta)
