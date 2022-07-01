"""Plots T2m and TCWV July climatology for paper"""

from pathlib import Path

import numpy as np
import xarray as xr

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap

import cartopy.crs as ccrs

from plotting import plot_panarctic_panel, mask_greenland


datafile = Path('/projects/AROSS/Reanalysis/ERA5/pressure_levels/monthly/',
                'era5.pressure_levels.monthly.climatology.1980to2010.nc')

cbar_kwargs = {'shrink': 0.95, 'orientation': 'horizontal', 'pad': 0.05}

plt.rcParams.update({'mathtext.default':  'regular' })

thk_cmap = cm.get_cmap('cividis', 256)
thk_cmap = ListedColormap(thk_cmap(np.linspace(0.1, 1.0, 256)))


def plot_era5_thickness_climatology():
    """Plots climatology figure"""

    ds = xr.open_dataset(datafile)

    fig = plt.figure(figsize=(7,7))

    ax1 = plot_panarctic_panel(fig, 111)
    cbar_kwargs['label'] = 'm'
    ds.thickness.sel(month=7).plot.contourf(ax=ax1,
                                            transform=ccrs.PlateCarree(),
                                            vmin=5200, vmax=5600,
                                            levels=np.arange(5400., 5600.+20., 20.),
                                            cmap=thk_cmap,
                                            cbar_kwargs=cbar_kwargs,)
    ax1.set_title('')
    ax1.text(0.02, 0.98, 'a) $\Delta z$',
             transform=ax1.transAxes,
             fontsize=17,
             horizontalalignment='left',
             verticalalignment='top',
             bbox={'facecolor': 'white', 'alpha': 0.5,})
    mask_greenland(ax1)
    
    fig.savefig('era5.thickness.climatology.png')


if __name__ == "__main__":
    plot_era5_thickness_climatology()
