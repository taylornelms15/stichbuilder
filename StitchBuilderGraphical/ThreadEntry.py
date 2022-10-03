#!/usr/bin/env python3

DEFAULT_DISTANCE_COLORSPACE = "LUV"

class ColorSpace:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def getVals(self):
        return [self.x, self.y, self.z]

class RGB_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "RGB", x, y, z)
class HSV_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "HSV", x, y, z)
class LUV_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "LUV", x, y, z)
class LAB_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "LAB", x, y, z)

class ThreadEntry:
    def __init__(self, DisplayName, DisplayNumStr, dmc_num, 
                rgb_r, rgb_g, rgb_b, 
                hsv_h, hsv_s, hsv_v,
                luv_l, luv_u, luv_v,
                lab_l, lab_a, lab_b):
        self.DisplayName = DisplayName
        self.DisplayNumStr = DisplayNumStr
        self.dmc_num = dmc_num
        self.rgb = RGB_CS(rgb_r, rgb_g, rgb_b)
        self.hsv = HSV_CS(hsv_h, hsv_s, hsv_v)
        self.luv = LUV_CS(luv_l, luv_u, luv_v)
        self.lab = LAB_CS(lab_l, lab_a, lab_b)
    
    def getColor(self, colorspace):
        if colorspace == "RGB":
            return self.rgb.getVals()
        elif colorspace == "HSV":
            return self.hsv.getVals()
        elif colorspace ==  "LUV":
            return self.luv.getVals()
        elif colorspace == "LAB":
            return self.lab.getVals()
        else:
            raise ValueError("Unsupported colorspace %s" % colorspace)

    def calcColorDistance(self, rh, colorspace=DEFAULT_DISTANCE_COLORSPACE):
        """
        Calculates the "distance" to the other color
        """
        # switch Colorspace
        if colorspace == "RGB":
            return self.rgb.distance(rh.rgb)
        elif colorspace == "HSV":
            return self.hsv.distance(rh.hsv)
        elif colorspace ==  "LUV":
            return self.luv.distance(rh.luv)
        elif colorspace == "LAB":
            return self.lab.distance(rh.lab)
        else:
            raise ValueError("Unsupported colorspace %s" % colorspace)

    def getRGBFloat(self):
        return self.rgb.getVals()
    def getRGB(self):
        rgbFloat = self.getRGBFloat()
        return [int(rgbFloat[0] * 255), int(rgbFloat[1] * 255), int(rgbFloat[2] * 255)]
    def getBGR(self):
        rgb = self.getRGB()
        return [rgb[2], rgb[1], rgb[0]]

    def getLightness(self):
        return self.luv.x

    def getHSV(self):
        return self.hsv.getVals()
    def getLUV(self):
        return self.luv.getVals()
    def getLAB(self):
        return self.lab.getVals()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Entry dmc=%s name=%s r=%s g=%s b=%s luv [%s %s %s]>" % (self.dmc_num, self.DisplayName, self.rgb.x, self.rgb.y, self.rgb.z, self.luv.x, self.luv.y, self.luv.z)

    def __lt__(self, rh):
      (mx, my, mz) = self.getLUV()
      (tx, ty, tz) = rh.getLUV()
      if mx < tx: return True
      if mx > tx: return False
      if my < ty: return True
      if my > ty: return False
      if mz < tz: return True
      if mz > tz: return False
      return (self.DisplayName < rh.DisplayName)

    def __eq__(self, rh):
      if not hasattr(rh, "DisplayName"):
        return False
      return self.DisplayName == rh.DisplayName

    def __hash__(self):
      return self.DisplayName.__hash__()
