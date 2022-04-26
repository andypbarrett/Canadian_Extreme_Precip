# Notes on creating station climatologies

Originally 10 locations in the Canadian Arctic were selected.  Long
term records were created by, in some cases, combining several station
records.  This procedure is described in
`how_to_combine_stations.txt`.

Record lengths vary by station and by variable.  For many stations the
record starts to get thin in recent years, with both the number of
missing days during times when stations were operational, as well as
some extended period with no observations at all.

It was decided to calculate climatologies for 1960 to 1995.  See email
quotes below.

To calculate climatologies:
1. Monthly means of daily mean, min and max temperatures were
calculated for months with observations on all days in that month.
2. Monthly totals of total precipitation, liquid precipitation and
solid precipitation were calculated for months with observations on
all days.
3. Where data were available, the frequency (days/month) of snow on
the ground was estimated, again for months with observations on all
days.
4. Climatologies were calculated by taking the average of monthly
values for each variable for the 1960 to 1995 period.


## Stations
Cape Dyer
Resolute Bay
Eureka
Alert
Clyde River
Pond Inlet*
Cambridge Bay
Hall Beach
Sachs Harbour
Inuvik

*Pond Inlet was excluded from the paper because of short record.  Cape
Dye was retained because it was so weird.


## Cyclone Frequency
Cyclone frequency was estimated from ERA5 by Alex Crawford.

From Mark:
"""
I'm cool with chucking Pond Inlet, and yes, 3x3 grid good.  Cape Dyer is a key site.  It so weird.
m
"""

From Alex:
""" 
> If removing Pond Inlet, the rest of the stations
(including Cape Dyer) all seem to have roughly 1960 to 1995 in good
shape -- in other words, roughly 30 years in common. That's not too
bad. The other benefit of 9 stations is that they fit better in a 3 by
3 grid.  > 
"""


