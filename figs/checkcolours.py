#!/usr/bin/env python
# Software to check the colour of a plot are understandable by colour-blind people
# Produces versions of the input images in different variants.
#
# Author for the EB: Francesco Dettori 
#
# Original software:
# Author: Loren Petrich, petrich (at) panix (dot) com, and lpetrich at various online venues. 
# Color-Blindness Simulator; uses the Python Image Library
# https://lpetrich.org/Science/ColorBlindnessSim/ColorBlindnessSim.html
# 


import sys
args = sys.argv


from PIL import Image
# Configuration from command line 
import argparse
parser = argparse.ArgumentParser(usage = 'usage: %(prog)s FILE ', description='Apply colour-blindness filters to images.  Does not accept pdf. ')
parser.add_argument("input_file", nargs = '+', metavar = 'FILE', help='files to be converted')


arguments = parser.parse_args()

# Possible filters (some of these are not used) 
cbnames = (\
	"No L (Red) - Protanopia",
	"No M (Green) - Deuteranopia",
	"No S (Blue) - Tritanopia",
	"Dog Vision",
	"Gray - Brightness",
	"Gray - L (Red)",
	"Gray - M (Green)",
	"Gray - S (Blue)"
)

# Color-blindness names and matrix values
cbmats = ( \
(0.202001295331, 0.991720719265, -0.193722014597, 0,
0.163800203026, 0.792663865514, 0.0435359314602, 0,
0.00913336570448, -0.0132684300993, 1.00413506439, 0),

(0.430749076295, 0.717402505462, -0.148151581757, 0,
0.336582831043, 0.574447762213, 0.0889694067435, 0,
-0.0236572929497, 0.0275635332006, 0.996093759749, 0),

(0.971710712275, 0.112392320487, -0.0841030327623, 0,
0.0219508442818, 0.817739672383, 0.160309483335, 0,
-0.0628595877201, 0.880724870686, 0.182134717034, 0),

(0.316086131719, 0.854894118151, -0.170980249869, 0,
0.250572926562, 0.683189199376, 0.0662378740621, 0,
-0.00735450321111, 0.00718184676374, 1.00017265645, 0),

(0.299, 0.587, 0.114, 0,
0.299, 0.587, 0.114, 0,
0.299, 0.587, 0.114, 0),

(0.340841450085, 0.580912815482, 0.0782457344332, 0,
0.340841450085, 0.580912815482, 0.0782457344332, 0,
0.340841450085, 0.580912815482, 0.0782457344332, 0),

(0.150317227739, 0.722407271325, 0.127275500935, 0,
0.150317227739, 0.722407271325, 0.127275500935, 0,
0.150317227739, 0.722407271325, 0.127275500935, 0),

(0.0336717653952, 0.114595364984, 0.851732869621, 0,
0.0336717653952, 0.114595364984, 0.851732869621, 0,
0.0336717653952, 0.114595364984, 0.851732869621, 0)
)

def cvtsave(img,ix,outfile):
	cbmat = cbmats[ix]
	imgx = img.convert('RGB',cbmat)
	imgx.save(outfile)


for infile in arguments.input_file : 
        img = Image.open(infile)
        if img.mode != 'RGB':
                img = img.convert('RGB')

        fileprefix = infile.split(".")[0]
        filesuffix = infile.split(".")[1]
        print ("Producing file " + infile +" for case: Protanopia")
        cvtsave(img,1,fileprefix+"_protanopia."+filesuffix)
        print ("Producing file " + infile +" for case: Deuteranopia")
        cvtsave(img,2,fileprefix+"_deuteranopia."+filesuffix)
        print ("Producing file " + infile +" for case: Tritanopia")
        cvtsave(img,3,fileprefix+"_tritanopia."+filesuffix)
        print ("Producing file " + infile +" in grey scale")
        cvtsave(img,5,fileprefix+"_greyscale."+filesuffix)


print("Please check all these figures are understandable ")
