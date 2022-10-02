# This Python file uses the following encoding: utf-8

"""
This module is a place to store constants useful to a number of different processes
It should remain relatively lean, mostly to avoid circular references or redeclarations
"""
#*************************************************
# DISPLAY
#*************************************************

# The "base" side length in pixels of a displayed stitch square
SQUARE_SIDE_LEN_PX  = 24
# The "base" font size in pts of a displayed stitch square symbol
FONT_BASE_SIZE_PT   = 12
# The interval at which to draw grid lines on printed/displayed areas
GRID_NUM_INTERVAL   = 10

#*************************************************
# PRINTING
#*************************************************

# Page margin, inches
MARGINSIZE_IN = 0.5
# Margin in unscaled pixels to leave around the stitch display view for grid markings
GRID_LABEL_MARGIN_BASE_PX = SQUARE_SIDE_LEN_PX
# Page rendering resolution, dots per inch
RESOLUTION_DPI = 600
# Factor used for scaling "screen" display to pdf printing
DISPLAY_SIZEFACTOR = RESOLUTION_DPI / 96.0 # 96 conceptual pixels per inch for accurate font rendering
# Aesthetic modification to the above factor
PRINT_SIZEFACTOR = DISPLAY_SIZEFACTOR * (2.0 / 3.0)

