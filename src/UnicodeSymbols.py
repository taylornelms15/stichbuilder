#!/usr/bin/env python

class UnicodeSymbols:
    def __init__(self):
        line_horiz_thin = "\u2500"
        line_horiz_thic = "\u2501"
        line_vert_thin  = "\u2502"
        line_vert_thic  = "\u2503"
        cross_forward   = "\u2571"
        cross_back      = "\u2572"
        cross_x         = "\u2573"
        square          = "\N{WHITE SQUARE}"
        tri_l           = "\N{WHITE LEFT-POINTING TRIANGLE}"
        tri_r           = "\N{WHITE RIGHT-POINTING TRIANGLE}"

        self.chars = [line_horiz_thin, line_horiz_thic, line_vert_thin, line_vert_thic, cross_forward, cross_back, cross_x, square, tri_l, tri_r]



def main():
    symbolgroup = UnicodeSymbols()

    for char in symbolgroup.chars:
        print(char)

if __name__ == "__main__":
    main()
