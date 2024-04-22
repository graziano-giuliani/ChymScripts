#!/usr/bin/env python3

# Very simple merger. Merge to GDAL created netCDF files together.

import sys
import numpy as np
from netCDF4 import Dataset

eu = Dataset(sys.argv[1], 'r+')
af = Dataset(sys.argv[2], 'r')

dem1 = eu.variables['Band1'][:]
dem2 = af.variables['Band1'][:]

dem1 = np.where(dem1>float(sys.argv[3]),dem2,dem1)

eu.variables['Band1'][:] = dem1

eu.close( )
af.close( )
