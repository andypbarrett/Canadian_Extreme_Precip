"""Creates climatology files for each station containing station 
observations and cyclone statistics"""


from reader import read_combined_file, read_cyclone_climatology
from filepath import combined_station_filepath, climatology_filepath
from utils import to_monthly, to_climatology


stations_list = [
    'cape dyer',
    'resolute bay',
    'eureka',
    'alert',
    'clyde river',
    'cambridge bay',
    'hall beach',
    'sachs harbour',
    'inuvik',
    'pond inlet',
    ]


def load_climatology(station):
    """Loads station data and calculates climatology
    and loads cyclone frequency"""
    df = read_combined_file(combined_station_filepath(station))
    df_mon = to_monthly(df)
    df_clm = to_climatology(df_mon.loc['1960':'1995', :])
    return df_clm


def make_climatology_files(verbose=False):
    """Calculates station climatology and combines with cyclone climatology"""
    df_cyclone = read_cyclone_climatology(CYCLONE_PATH)
    df_cyclone.columns = [f"CYCLONE_{col.upper()}" for col in df_cyclone.columns]

    for station in stations_list:
        if verbose: print(f"Making climatology for {station.title()}")
        df = load_climatology(station)
        df = df.join(df_cyclone.loc[station.title(), :])

        outpath = climatology_filepath(station)
        if verbose: print(f"   Writing climatology to {outpath}\n")
        df.to_csv(outpath)


if __name__ == "__main__":
    make_climatology_files(verbose=True)
