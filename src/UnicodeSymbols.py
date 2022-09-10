#!/usr/bin/env python

class UnicodeSymbols:
  def __init__(self):
    self.chars_light = [
      "\N{WHITE SQUARE}",
      "\N{WHITE CIRCLE}",
      "\N{WHITE HEART SUIT}",
      "\N{WHITE RIGHT-POINTING TRIANGLE}",
      "\N{WHITE LEFT-POINTING TRIANGLE}",
      "\N{UPPER HALF CIRCLE}",
      "\N{LOWER HALF CIRCLE}",
      "\N{TILDE}",
      "\N{BALLOT BOX WITH LIGHT X}",
      "\N{BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT}",
      "\N{BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT}",
      "\N{BOX DRAWINGS LIGHT DIAGONAL CROSS}",
      "\N{LOW ASTERISK}",
      "\N{ASTERISM}",
      "\N{CIRCLED PLUS}",
      "\N{CIRCLED MINUS}",
      "\N{CIRCLED TIMES}",
      "\N{CIRCLED DOT OPERATOR}",
      "\N{WHITE FOUR POINTED CUSP}",
      "\N{ROTATED WHITE FOUR POINTED CUSP}",
      "\N{ELECTRIC ARROW}",
      "\N{FIRST QUARTER MOON}",
      "\N{LAST QUARTER MOON}",
      "\N{WHITE CLUB SUIT}",
      "\N{TURNED WHITE SHOGI PIECE}",
      "\N{INFINITY}",
    ]
    self.chars_med = [
      "\N{BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY VERTICAL AND RIGHT}",
      "\N{BOX DRAWINGS HEAVY VERTICAL AND LEFT}",
      "\N{BOX DRAWINGS HEAVY UP AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY DOWN AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY DOUBLE DASH VERTICAL}",
      "\N{BOX DRAWINGS HEAVY HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY VERTICAL}",
      "\N{LIGHT FOUR POINTED BLACK CUSP}",
      "\N{ROTATED LIGHT FOUR POINTED BLACK CUSP}",
      "\N{WHITE UP-POINTING TRIANGLE}",
      "\N{WHITE DOWN-POINTING TRIANGLE}",
      "\N{WHITE DIAMOND}",
      "\N{BULLSEYE}",
      "\N{WHITE STAR}",
      "\N{VIEWDATA SQUARE}",
      "\N{CYLINDRICITY}",
      "\N{EARTH GROUND}",
      "\N{ANKH}",
    ]
    self.chars_dark = [
      "\N{BLACK SQUARE}",
      "\N{BLACK DIAMOND}",
      "\N{BLACK CIRCLE}",
      "\N{BLACK HEART SUIT}",
      "\N{BLACK CLUB SUIT}",
      "\N{TURNED BLACK SHOGI PIECE}",
      "\N{BLACK FLORETTE}",
      "\N{CIRCLE WITH LEFT HALF BLACK}",
      "\N{CIRCLE WITH RIGHT HALF BLACK}",
      "\N{CIRCLE WITH LOWER HALF BLACK}",
      "\N{CIRCLE WITH UPPER HALF BLACK}",
      "\N{SQUARE WITH TOP HALF BLACK}",
      "\N{SQUARE WITH BOTTOM HALF BLACK}",
      "\N{SQUARE WITH LEFT HALF BLACK}",
      "\N{SQUARE WITH RIGHT HALF BLACK}",
      "\N{DIAMOND WITH TOP HALF BLACK}",
      "\N{DIAMOND WITH BOTTOM HALF BLACK}",
      "\N{DIAMOND WITH LEFT HALF BLACK}",
      "\N{DIAMOND WITH RIGHT HALF BLACK}",
    ]
    self.chars = self.chars_light + self.chars_med + self.chars_dark




def main():
  symbolgroup = UnicodeSymbols()

  for char in symbolgroup.chars:
    print(char)

if __name__ == "__main__":
  main()
