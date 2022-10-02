#!/usr/bin/env python
import numpy as np

class UnicodeSymbols:
  def __init__(self):
    self.chars_light = [
      "\N{TILDE}",
      "\N{LOW ASTERISK}",
      "\N{WHITE SQUARE}",
      "\N{WHITE CIRCLE}",
      "\N{WHITE HEART SUIT}",
      "\N{WHITE RIGHT-POINTING TRIANGLE}",
      "\N{WHITE LEFT-POINTING TRIANGLE}",
      #"\N{UPPER HALF CIRCLE}",
      #"\N{LOWER HALF CIRCLE}",
      "C",
      "L",
      "\N{BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT}",
      "\N{BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT}",
      "\N{BOX DRAWINGS LIGHT DIAGONAL CROSS}",
      "\N{ASTERISM}",
      "\N{CIRCLED PLUS}",
      "\N{CIRCLED MINUS}",
      "\N{CIRCLED TIMES}",
      "\N{CIRCLED DOT OPERATOR}",
      "\N{ELECTRIC ARROW}",
      "\N{FIRST QUARTER MOON}",
      "\N{LAST QUARTER MOON}",
      "\N{WHITE CLUB SUIT}",
      "\N{TURNED WHITE SHOGI PIECE}",
      "\N{WHITE FOUR POINTED CUSP}",
      "\N{ROTATED WHITE FOUR POINTED CUSP}",
    ]
    self.chars_med = [
      "\N{WHITE UP-POINTING TRIANGLE}",
      "\N{WHITE DOWN-POINTING TRIANGLE}",
      "\N{BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY VERTICAL AND RIGHT}",
      "\N{BOX DRAWINGS HEAVY VERTICAL AND LEFT}",
      "\N{BOX DRAWINGS HEAVY UP AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY DOWN AND HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY DOUBLE DASH VERTICAL}",
      "\N{BOX DRAWINGS HEAVY HORIZONTAL}",
      "\N{BOX DRAWINGS HEAVY VERTICAL}",
      "\N{WHITE DIAMOND}",
      "\N{BULLSEYE}",
      "\N{WHITE STAR}",
      "\N{VIEWDATA SQUARE}",
      "\N{CYLINDRICITY}",
      "\N{EARTH GROUND}",
      "\N{INFINITY}",
      "\N{ANKH}",
      "M",
      "W",
    ]
    self.chars_dark = [
      "\N{BLACK SQUARE}",
      "\N{BLACK DIAMOND}",
      "\N{BLACK CIRCLE}",
      "\N{BLACK HEART SUIT}",
      "\N{BLACK CLUB SUIT}",
      "\N{TURNED BLACK SHOGI PIECE}",
      "\N{BLACK FLORETTE}",
      #"\N{CIRCLE WITH LEFT HALF BLACK}",
      "#",
      "\N{CIRCLE WITH RIGHT HALF BLACK}",
      #"\N{CIRCLE WITH LOWER HALF BLACK}",
      "W",
      "\N{CIRCLE WITH UPPER HALF BLACK}",
      #"\N{SQUARE WITH TOP HALF BLACK}",
      "M",
      "\N{SQUARE WITH BOTTOM HALF BLACK}",
      "\N{SQUARE WITH LEFT HALF BLACK}",
      #"\N{SQUARE WITH RIGHT HALF BLACK}",

      "%",
      #"\N{DIAMOND WITH TOP HALF BLACK}",
      "@",
      "\N{DIAMOND WITH BOTTOM HALF BLACK}",
      "\N{DIAMOND WITH LEFT HALF BLACK}",
      "\N{DIAMOND WITH RIGHT HALF BLACK}",
      "\N{BALLOT BOX WITH LIGHT X}",
    ]
    self.chars = self.chars_light + self.chars_med + self.chars_dark

  def constructMappingDict(self, tentry_list):
    """
    Given a number of ThreadEntry objects, assigns each a unicode symbol
    Returns a dict mapping {threadEntry: unicode string}
    """
    # Take out white (special case)
    white_entry = None
    if len([x for x in tentry_list if x.dmc_num == "white"]):
      white_entry = [x for x in tentry_list if x.dmc_num == "white"][0]
      tentry_list = [x for x in tentry_list if x.dmc_num != "white"]
    # Sort our input colors based on lightness (descending)
    lightnessArray = np.array([x.getLightness() for x in tentry_list])
    sort_indexes = np.flip(np.argsort(lightnessArray))
    sortedEntries = np.take(tentry_list, sort_indexes)

    # Split the entries into light, medium, and dark
    n = len(tentry_list)
    # Even-split case
    if n <= (3 * len(self.chars_dark)):
      nlight = int(n/3)
      nmed = int((2*n)/3) - nlight
      ndark = n - nmed - nlight
      lights = sortedEntries[0:int(nlight)]
      mediums = sortedEntries[int(nlight):int(nlight + nmed)]
      darks = sortedEntries[int(nlight + nmed):int(n)]
      light_dict = dict(zip(lights, self.chars_light[0:nlight]))
      med_dict = dict(zip(mediums, self.chars_med[0:nmed]))
      dark_dict = dict(zip(darks, self.chars_dark[0:ndark]))
    else:# Mostly-full case, just zip them using dark as the remainder
      nlight = len(self.chars_light)
      nmed = len(self.chars_med)
      ndark = len(sortedEntries) - nlight - nmed
      lights = sortedEntries[0:int(nlight)]
      mediums = sortedEntries[int(nlight):int(nlight + nmed)]
      darks = sortedEntries[int(nlight + nmed):int(n)]
      light_dict = dict(zip(lights, self.chars_light))
      med_dict = dict(zip(mediums, self.chars_med))
      dark_dict = dict(zip(darks, self.chars_dark[0:ndark]))

    # Join our dictionaries and return
    retval = {**dark_dict, **med_dict, **light_dict}
    if white_entry != None:
      retval[white_entry] = " "
    return retval




def main():
  symbolgroup = UnicodeSymbols()

  for char in symbolgroup.chars:
    print(char)

if __name__ == "__main__":
  main()
