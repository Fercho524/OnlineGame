from Config import *


def check_colisions(x0, y0, w0, h0, x1, y1, w1, h1):
    return x0 < x1 + w1 and x0 + w0 > x1 and y0 < y1 + h1 and y0 + h0 > y1


def is_out(x0, y0):
    return (x0 <= 0 or x0 >= WIDTH or y0 <= 0 or y0 >= HEIGHT)
