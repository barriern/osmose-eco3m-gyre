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
import numpy as np
from dask.diagnostics import ProgressBar
from glob import glob
import os

# +
dirin = '/home/datawork-marbec-scenlab/OSMOSE/Eco3M-Melika'

ymin = 1997
ymax = 2018
# -

filelist = glob(os.path.join(dirin, 'MED12_nemo36_SPIN_1m_20181201_20181231_*.nc'))
filelist.sort()
filelist

for file_pattern in filelist:

    foutname = file_pattern.replace('20181201_20181231', 'climato')
    print('---------------------------------------- ', foutname)

    if os.path.isfile(foutname):
        print(f'File {file_pattern} has been processed. Skip file')
        continue

    temp_file_list = np.array(glob(file_pattern.replace('20181201_20181231', '*_*')))
    temp_file_list.sort()

    varlist = xr.open_dataset(temp_file_list[0]).variables

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

    dsout = xr.Dataset()
    list_years = np.arange(ymin, ymax + 1)
    
    print(len(list_years))

    for year in list_years:

        index_files = np.nonzero([f'1m_{year}' in f for f in temp_file_list])
#         print(temp_file_list[index_files])

        data = xr.open_mfdataset(temp_file_list[index_files])
        data

        if year == ymin:
#             print("Init file")
            for v in varlist2:
                dsout[v] = data[v]
        else:
#             print("Aggregate file")
            for v in varlist2:
                dsout[v].values += data[v].values
    
    for v in varlist2:
        dsout[v].values /= len(list_years)

    dsout = dsout.chunk({'time_counter': 1})

    dsout.to_netcdf(foutname)


