"""
dust.py

A dust dataset using the EPICA Dome C Ice Core 800KYr Dust Data.
https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc-dust2008.txt

"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from milankovitch import ROOT


def clean(datafile: Path) -> pd.DataFrame:
    """
    Clean the text data
    Returns: a dataframe

    """
    tempfile = "temp.csv"

    # discard first 275 lines
    with open(datafile, "r", errors="replace") as f:
        lines = f.readlines()

    slice = lines[98:5857]

    with open(tempfile, "w") as f:
        f.writelines(slice)

    df = pd.read_csv("temp.csv", delim_whitespace=True)
    Path.unlink(tempfile)

    # convert from kYears to Years
    df["EDC3Age(kyrBP)"] = df["EDC3Age(kyrBP)"] * 1000

    return df


def interpolate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolate a dataframe
    Args:
        df: the dataframe to interpolate

    Returns: an interpolated dataframe

    """
    # convert year to '000 of years
    df["EDC3Age(kyrBP)"] = df["EDC3Age(kyrBP)"] / 1000

    MAX_AGE = 800
    x = np.linspace(0.0, MAX_AGE, MAX_AGE + 1)
    y = np.interp(x, df["EDC3Age(kyrBP)"], df["LaserDust(ng/g)"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age(kYr)", "Dust(ng/g)"])
    df = df.dropna()
    df = df.astype({"Age(kYr)": int})

    return df


def epica_domec_800kr_dust() -> pd.DataFrame:
    """
    Process the EPICA dust dataset and return a dataframe.

    Data is dust in ng/g for the timeseries [0, 800000] years.

    Returns: a dataframe with the data

    """
    datafile = ROOT / "data" / "1634220214_2023-04-05/data/pub/data/paleo/icecore/antarctica/epica_domec/edc-dust2008.txt"
    df = clean(datafile)
    df = interpolate(df)

    return df


if __name__ == "__main__":
    df = epica_domec_800kr_dust()
    print(df)

    df.plot(x="Age(kYr)", y="Dust(ng/g)")
    plt.show()
