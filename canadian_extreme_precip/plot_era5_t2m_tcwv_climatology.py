"""Plots T2m and TCWV July climatology for paper"""

from pathlib import Path

import xarray as xr

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

NSIDCNorthPolarStereo = ccrs.NorthPolarStereo()

datafile = Path('/projects/AROSS/Reanalysis/ERA5/surface/monthly/',
                'era5.single_levels.monthly.climatology.1980to2010.nc')


def plot_panel(fig, position):
    """Plots figure panel"""
    ax = fig.add_subplot(position,
                         projection=NSIDCNorthPolarStereo)
    ax.set_extent([-180,180,60,90], ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    return ax


def plot_era5_t2m_tcwv_climatology():
    """Plots climatology figure"""

    ds = xr.open_dataset(datafile)
    ds.t2m = ds.t2m - 273.15
    
    fig = plt.figure(figsize=(10,7))

    ax1 = plot_panel(fig, 121)
    ds.t2m.sel(month=7).plot(ax=ax1,
                             transform=ccrs.PlateCarree(),
                             vmin=-3, vmax=18)
    
    ax2 = plot_panel(fig, 122)
    ds.tcwv.sel(month=7).plot(ax=ax2,
                              transform=ccrs.PlateCarree(),
                              vmin=0, vmax=24)
    
    plt.show()


if __name__ == "__main__":
    plot_era5_t2m_tcwv_climatology()
