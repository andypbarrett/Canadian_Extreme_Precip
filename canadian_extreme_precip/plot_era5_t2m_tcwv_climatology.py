"""Plots T2m and TCWV July climatology for paper"""

from pathlib import Path

import numpy as np

import xarray as xr

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap

import cartopy.crs as ccrs

from plotting import plot_panarctic_panel

datafile = Path('/projects/AROSS/Reanalysis/ERA5/surface/monthly/',
                'era5.single_levels.monthly.climatology.1980to2010.nc')

cbar_kwargs = {'shrink': 0.95, 'orientation': 'horizontal', 'pad': 0.05}

plt.rcParams.update({'mathtext.default':  'regular' })

t2m_cmap = cm.get_cmap('coolwarm', 256)
t2m_cmap = ListedColormap(t2m_cmap(np.linspace(0., 1., 256)))

tcwv_cmap = cm.get_cmap('viridis_r', 256)
tcwv_cmap = ListedColormap(tcwv_cmap(np.linspace(0.0, 0.8, 256)))


def plot_era5_t2m_tcwv_climatology():
    """Plots climatology figure"""

    ds = xr.open_dataset(datafile)
    ds["t2m"] = ds.t2m - 273.15

    fig = plt.figure(figsize=(10,7))

    ax1 = plot_panarctic_panel(fig, 122)
    cbar_kwargs['label'] = '$^\circ$C'
    ds.t2m.sel(month=7).plot.contourf(ax=ax1,
                                      transform=ccrs.PlateCarree(),
                                      center=0., vmin=-20., vmax=20.,
                                      levels=np.arange(-20, 22, 4),
                                      cmap=t2m_cmap,
                                      cbar_kwargs=cbar_kwargs,)
    ax1.set_title('')
    ax1.text(0.02, 0.98, 'b) $T_{2m}$',
             transform=ax1.transAxes,
             fontsize=17,
             horizontalalignment='left',
             verticalalignment='top',
             bbox={'facecolor': 'white', 'alpha': 0.5,})
    
    ax2 = plot_panarctic_panel(fig, 121)
    cbar_kwargs['label'] = 'kg m$^{-2}$'
    ds.tcwv.sel(month=7).plot.contourf(ax=ax2,
                                       transform=ccrs.PlateCarree(),
                                       vmin=0, vmax=50,
                                       levels=np.arange(0, 22, 2),
                                       cmap=tcwv_cmap,
                                       cbar_kwargs=cbar_kwargs,)
    ax2.set_title('')
    ax2.text(0.02, 0.98, 'a) Prec. Water.',
             transform=ax2.transAxes,
             fontsize=17,
             horizontalalignment='left',
             verticalalignment='top',
             bbox={'facecolor': 'white', 'alpha': 0.5,})
    
    fig.savefig('era5.t2m_and_tcwv.climatology.png')


if __name__ == "__main__":
    plot_era5_t2m_tcwv_climatology()
