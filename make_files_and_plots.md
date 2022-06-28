# How to make combined files, tables and plots for paper

## Make combined files

To obtain long records, we combine several stations for a single
location.  This is done with the following code, which generates
combined station files with an daily timestep.  The station files are
combined according to "recipes" given in `station_merge_recipe.json`.
This `json` file gives the stations to be combined and the timespans
for each station used to create the combined record.

```
python -m canadian_extreme_precip.make_combined_files --verbose
```

The `make_combined_files` also replaces any data that have been
identified as bad.  A list of bad data records is in
`data/bad_records.csv`


## Generate a table of percentage missing data

A table of percentage of missing values is written to standard out
with the following command

```
python -m canadian_extreme_precip.get_percent_missing_data
```


## Generate a table of preciptation quantiles

We generate precipitation quantiles for each station using:

```
python -m canadian_extreme_precip.get_precipitation_quantiles
```

This writes a table to standard out.  Quantiles are generated for all
non-zero precipitation values.  For Canadian stations, the minimum
measureable precipitation is 0.2 mm.  All precipitation less than 0.2
mm is recorded as Trace.

NB. Trace precipitation makes up a large number of precipitation
events in the Arctic.


## Plot station locations and precipitation statistics

TODO
- plot station locations
- plot station climatologies - add legend for snow cover
- Update quantile table
- reorder quantile table
