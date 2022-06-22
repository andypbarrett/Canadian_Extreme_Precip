 Hi Andy and Mark,

I'm attaching the file I made describing cyclone tracks that intersect the circle with a radius of 800 km centered on each of the weather stations. These are all average values per month for 1950-2020 ERA5 data. "Hours" is the number of hours spent by cyclones with 800 km of each station. "Tracks" is the number of unique tracks. 

"DsqP" is the Laplacian of central pressure measured at a 25-km spatial resolution. Units are hPa / [100 km]^2, and the values are almost always higher than what you would find from 100-km resolution data.  "Local" means I've take the maximum Laplacian for all times when a cyclone is within 800 km of the station. "Total" means I've taken the maximum for the entire cyclone track. I then average the maximum value from all tracks that existed in the 71 Januarys, 71 Februarys, etc. (In other words, this is the climatological monthly average of track maxima).

I assume we just what to use a frequency value, but the intensity values are present there just in case. The seasonality for the hours metric and the unique tracks metric are not perfectly aligned. I suspect the number of unique tracks is the better metric for the purposes of the paper since a) we're mostly linking to discrete precipitation events and b) the 800-km radius is not a perfect method of identifying which storms caused precipitation -- so there's probably a bigger (although unmeasured) uncertainty/error in that hours metric.  

Best wishes,
Alex

Dr. Alex Crawford (he/him/his)
Research Associate & Sessional Instructor
Centre for Earth Observation Science
Clayton H. Riddell Faculty of Environment, Earth, & Resources
University of Manitoba
