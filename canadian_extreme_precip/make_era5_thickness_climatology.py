"""Makes thickness climatology from ERA5 geopotential monthly reanalysis files

Here we calculate 500 hPa thickness which is defined as:

    thickness = z500 - z1000

Thickness is calculated for each month and the monthly means calculated
"""

from pathlib import Path

import xarray as xr

year_start = 1980
year_end = 2010

path = Path('/', 'projects', 'AROSS', 'Reanalysis', 'ERA5', 'pressure_levels', 'monthly')

g = 9.80665

def make_era5_thickness_climatology():
    """Makes climatology files"""

    filelist = [path / f"era5.pressure_levels.monthly.{y}.nc" for y in range(year_start, year_end+1)]
    ds = xr.open_mfdataset(filelist, combine="by_coords")
    ds['thickness'] = (ds.z.sel(level=500) - ds.z.sel(level=1000)) / g
    ds['thickness'].attrs = {
        'units': 'm',
        'long_name': '500 hPa thickness',
        'standard_name': 'atmosphere_layer_thickness_expressed_as_geopotential_height_difference',
        'level': '500 hPa'
        }
    
    ds_clim = ds.groupby(ds.time.dt.month).mean(keep_attrs=True)
    ds_clim.to_netcdf(path / f"era5.pressure_levels.monthly.climatology.{year_start}to{year_end}.nc")


if __name__ == "__main__":
    make_era5_thickness_climatology()
