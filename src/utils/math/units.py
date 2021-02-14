from numpy import pi


def mm2m(mm):
    return mm * 1e-3


def um2m(um):
    return um * 1e-6


def nm2m(nm):
    return nm * 1e-9


def px2m(px, px_size_m=5.04e-6):
    return px * px_size_m


def m2px(m, px_size_m=5.04e-6):
    return m // px_size_m


def m2mm(m):
    return m * 1e+3


def um2mm(um):
    return um * 1e-3


def nm2mm(nm):
    return nm * 1e-6


def m2um(m):
    return m * 1e+6


def mm2um(mm):
    return mm * 1e+3


def nm2um(nm):
    return nm * 1e-3


def m2nm(m):
    return m * 1e+9


def rad2mm(rad, wave_len_m):
    wave_num = 2 * pi / m2mm(wave_len_m)
    return rad / wave_num


def mm2rad(mm, wave_len_mm):
    wave_num = 2 * pi / wave_len_mm
    return mm * wave_num


def percent2decimal(percent):
    return percent / 100


def decimal2percent(decimal):
    return decimal * 100
