#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from numpy import *
from pylab import *

from test import sift

imname1 = 'empire.jpg'
im1 = array(Image.open(imname1).convert('L'))
# sift.process_image(imname1, 'empire.sift')
l1,d1 = sift.read_features_from_file('empire.sift')
print (l1)
imname2 = '1.jpg'
im2 = array(Image.open(imname2).convert('L'))
# sift.process_image(imname2, '1.sift')
l2,d2 = sift.read_features_from_file('1.sift')
print (l2)

print ('starting matching')
matches = sift.match_twosided(d1, d2)

figure()
gray()
sift.plot_matches(im1, im2, l1, l2, matches)
show()