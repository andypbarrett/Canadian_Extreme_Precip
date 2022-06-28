from canadian_extreme_precip.get_precipitation_quantiles import load_precip_data


stations_list = [
    'inuvik',
    'sachs harbour',
    'cambridge bay',
    'resolute bay',
    'alert',
    'eureka',
    'hall beach',
    'clyde river',
    'cape dyer',
    ]


def main():
    for station in stations_list:
        df = load_precip_data(station)
        nrecord = len(df)
        nmissing = df.isna().sum()
        print(f"{station.title():13s} {df.index.year[0]:4d} {df.index.year[-1]:4d} {nmissing * 100. / nrecord:3.0f}")


if __name__ == "__main__":
    main()
