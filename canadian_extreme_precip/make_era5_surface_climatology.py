"""Makes climatology for ERA5 monthly reanalysis files"""

from pathlib import Path

import xarray as xr

year_start = 1980
year_end = 2010

path = Path('/', 'projects', 'AROSS', 'Reanalysis', 'ERA5', 'surface', 'monthly')


def make_era5_surface_climatology():
    """Makes climatology files"""

    filelist = [path / f"era5.single_levels.monthly.{y}.nc" for y in range(year_start, year_end+1)]
    ds = xr.open_mfdataset(filelist, combine="by_coords")

    ds_clim = ds.groupby(ds.time.dt.month).mean()
    ds_clim.to_netcdf(path / f"era5.single_levels.monthly.climatology.{year_start}to{year_end}.nc")


if __name__ == "__main__":
    make_era5_surface_climatology()
