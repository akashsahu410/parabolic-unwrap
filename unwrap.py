#!/usr/bin/env python

import os,sys,math,operator
import numpy as np
from scipy import ndimage, misc
import argparse

parser = argparse.ArgumentParser(description="Unwrap photos from a parabolic mirror")
parser.add_argument("input", metavar="Input Image", help="Input Image File")
parser.add_argument("output", metavar="Output Image", help="Output Image File")
parser.add_argument("--center", help="Position of center pixel in the form x,y or \" +/-x,+/-y\"")
parser.add_argument("--size", help="Output image size in the form WIDTHxHEIGHT")
args = parser.parse_args()
raw_img = misc.imread(args.input)

center = (raw_img.shape[0] / 2, raw_img.shape[1] / 2)
if args.center:
  try:
    x,y = args.center.split(',')
    if '-' in args.center or '+' in args.center:
      new_center = (center[0] + int(y), center[1] + int(x))
      center = new_center
    else:
      center = (int(y),int(x))
  except:
    print "Center must me integers in the form x,y or +/-x,+/-y"
    sys.exit(-1)

size = (1024, 2048)
if args.size:
  try:
    width,height = args.size.split('x')
    width = int(width)
    height = int(height) 
    size = (height,width)
  except:
    print  "Size must be integers in the form WIDTHxHEIGHT"
    sys.exit(-1)
    
square_img = np.zeros((size[0], size[1]), np.uint8)
color_img  = np.zeros((size[0], size[1], 3), np.uint8)
it = np.nditer(square_img, flags=['multi_index'], op_flags=['readwrite'])
while not it.finished:
    axA = it.multi_index[0]
    axB = it.multi_index[1]

    radius = ((size[0]-float(axA)-1)/size[0])*center[0]
    cx = math.cos(2*math.pi*axB/size[1])*radius + center[1]
    cy = math.sin(2*math.pi*axB/size[1])*radius + center[0]
    r = raw_img[cy, cx, 0]
    g = raw_img[cy, cx, 1]
    b = raw_img[cy, cx, 2]

    color_img[axA, axB, 0] = r
    color_img[axA, axB, 1] = g
    color_img[axA, axB, 2] = b

    it.iternext()
misc.imsave(args.output, color_img)

