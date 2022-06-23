"""Plots T2m and TCWV July climatology for paper"""

from pathlib import Path

import numpy as np

import xarray as xr

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs

from plotting import plot_panarctic_panel

datafile = Path('/projects/AROSS/Reanalysis/ERA5/surface/monthly/',
                'era5.single_levels.monthly.climatology.1980to2010.nc')

cbar_kwargs = {'shrink': 0.95, 'orientation': 'horizontal', 'pad': 0.05}


class MidpointNormalize(mcolors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        mcolors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


def plot_era5_t2m_tcwv_climatology():
    """Plots climatology figure"""

    ds = xr.open_dataset(datafile)
    ds["t2m"] = ds.t2m - 273.15
    
    fig = plt.figure(figsize=(10,7))

    ax1 = plot_panarctic_panel(fig, 121)
    cbar_kwargs['label'] = '$^\circ$C'
    ds.t2m.sel(month=7).plot(ax=ax1,
                             transform=ccrs.PlateCarree(),
                             norm=MidpointNormalize(vmin=-3, vmax=18, midpoint=0.),
                             cmap='RdBu_r',
                             cbar_kwargs=cbar_kwargs,)
    ax1.set_title('')
    
    ax2 = plot_panarctic_panel(fig, 122)
    cbar_kwargs['label'] = 'kg m$^{-2}$'
    ds.tcwv.sel(month=7).plot(ax=ax2,
                              transform=ccrs.PlateCarree(),
                              vmin=0, vmax=24,
                              cmap='cividis_r',
                              cbar_kwargs=cbar_kwargs,)
    ax2.set_title('')
    
    fig.savefig('era5.t2m_and_tcwv.climatology.png')


if __name__ == "__main__":
    plot_era5_t2m_tcwv_climatology()
