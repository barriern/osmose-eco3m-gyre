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
#     display_name: Python (base)
#     language: python
#     name: base
# ---

import xarray as xr
from glob import glob
import os

dirin = '/home/datawork-marbec-scenlab/OSMOSE/Eco3M-Melika'

filelist = glob(os.path.join(dirin, '*climato*nc'))
filelist.sort()
filelist

grid = xr.open_dataset(os.path.join(dirin, 'mesh_mask_v75.nc')).squeeze()
grid

volume = grid['e1t'] * grid['e2t'] * grid['e3t_0'] * grid['tmask']
volume

weight = volume.sum(dim='z')
weight.plot()

for f in filelist:
    
    foutname = f.replace('climato', 'vertical_mean')
    foutname

    if os.path.isfile(foutname):
        print(f'------------ File {f} is processed. Skipped')
        continue
        
    print(f'+++++ Process {f}')

    data = xr.open_dataset(f, chunks={'time_counter': 1})
    data

    dsout = xr.Dataset()

    varlist = data.variables

    discards = ['nav_lat',
     'nav_lon',
     'deptht',
     'deptht_bounds',
     'time_centered',
     'time_centered_bounds',
     'time_counter',
     'time_counter_bounds']
    varlist2 = [v for v in varlist if v not in discards]
    varlist2

    for v in varlist2:
        
        print(v)

        temp = data[v]
        
        if 'deptht' in temp.dims:
            temp = temp.rename({'deptht': 'z'})
            temp

            temp2 = temp.weighted(volume).sum(dim='z')
            temp2
    
            dsout[v] = temp2
        else:
            dsout[v] = temp

    dsout['weight'] = weight
    
    dsout.to_netcdf(foutname)
