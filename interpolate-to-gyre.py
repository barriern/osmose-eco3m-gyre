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
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

filelist = glob('../configurations/osmose-melika/forcings-melika/MED12*vertical_mean*nc')
filelist.sort()
filelist

mesh = xr.open_dataset("trash/mesh_mask.nc").squeeze()
mesh = mesh.rename({'z': 'deptht'})
ny = mesh.sizes['y']
nx = mesh.sizes['x']
ny, nx

weight = mesh['e1t'] * mesh['e2t'] * mesh['e3t_1d']
weight


def integrate(var2d, function):
    cptx = 0
    cpty = 0
    ntime = var2d.shape[0]
    output = np.zeros((ntime, ny//2, nx//2))
    for j in range(0, ny, 2):
        cptx = 0
        for i in range(0, nx, 2):
            temp = var2d[..., slice(j, j+2), slice(i, i+2)]
            output[..., cpty, cptx] = function(temp, axis=(1, 2))
            cptx +=1
        cpty += 1
    return output


for f in filelist:

    print("---------------------------------- Processing", f)
    data = xr.open_dataset(f)
    data
    
    varlist = [v for v in data.variables if len(data[v].shape) == 3]
    varlist
    
    dsout = xr.Dataset()
    i = 325
    j = 62
    ix = slice(i, i + nx)
    iy = slice(j, j + ny)
    
    for v in varlist:
        print("Processing variable", v)
    
        # recover the variable on a domain that corresponds to 
        # gyre
        var2d = data[v].values[:, iy, ix]
    
        # Recover the index of NaN values and fill them with the
        # mean value over the region
        itime, ilat, ilon = np.nonzero(np.isnan(var2d))
        iok = np.nonzero(~np.isnan(var2d))
        print(var2d.shape)
        mean = np.nanmean(var2d, axis=(1, 2))
        filled = np.tile(mean, (len(ilon), 1)).T
        var2d[:, ilat, ilon] = filled
    
        # Integrate over the gyre basin
        dsout[v] = (['time', 'y', 'x'], integrate(var2d, np.sum))
    dsout
    
    # write the longitude coordinates
    lon = mesh['glamt'].values[np.newaxis, :, :]
    temp = integrate(lon, np.mean).squeeze()
    dsout["lon"] = (['y', 'x'], temp)
    
    # write the latitude coordinates
    lat = mesh['gphit'].values[np.newaxis, :, :]
    dsout["lat"] = (['y', 'x'], integrate(lat, np.mean).squeeze())
    dsout['tmask'] = (['y', 'x'], np.ones(dsout['lat'].shape))
    dsout
    
    foutname = os.path.basename(f)
    foutname = foutname.replace('MED12', 'GYRE')
    foutname = 'data/' + foutname
    
    dsout.to_netcdf(foutname, unlimited_dims=['time'])
    dsout




