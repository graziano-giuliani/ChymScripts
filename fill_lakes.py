#!/usr/bin/env python3

# Fill in lakes and reclassify Black Sea as ocean from Internal Water.

import sys
import numpy as np
from netCDF4 import Dataset
from skimage.segmentation import flood_fill
import statistics as st

ncf = Dataset(sys.argv[1], 'r+')
luc = ncf.variables['luc'][:]

luc = flood_fill(luc,(249,669), 15.0)
luc = flood_fill(luc,(349,644), 93.0)
luc = flood_fill(luc,(156,852), 2.0)
luc = flood_fill(luc,(202,851), 57.0)
luc = flood_fill(luc,(329,811), 31.0)
luc = flood_fill(luc,(322,681), 93.0)
luc = flood_fill(luc,(95,817), 51.0)
luc = flood_fill(luc,(347,844), 31.0)
luc = np.where((luc == 14.0), 85, luc)
ncf.variables['luc'][:] = luc

ncf.close( )
