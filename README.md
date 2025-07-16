# Eco3M-MED Gyre configuration

## Pre-processing of Eco3M files

- First, computation of climatological fields using `compute-clim-eco3m.py`
- Next, computation of vertical integration using `compute-vertical-mean-eco3m.py`
- Finally, create a Gyre subset by taking a sub-region of the Med file to match NEMO-Gyre configuration amd downscale it to match the Osmose-Gyyre configuration (`interpolate-to-gyre.py`)