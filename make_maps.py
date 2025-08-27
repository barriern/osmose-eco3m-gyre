# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import xarray as xr
from glob import glob
import numpy as np
import os

filelist = glob("fisheries/Fishery_maps/*nc")
filelist.sort()
filelist

output = np.ones((1, 11, 16))
for f in filelist:

    print("------------------------------- process", f)
    data = xr.open_dataset(f)
    data
    print(data)    
    varlist = [v for v in data.variables if len(data[v].shape)>=2]
    varlist
    print(varlist)
    
    dsout = xr.Dataset()
    dsout[varlist[0]] = (['time', 'y', 'x'], output)
    dsout.to_netcdf(os.path.basename(f))
