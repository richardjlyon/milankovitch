"""
temperature.py

A temperature dataset using the NOAA  EPICA Dome C - 800KYr Deuterium Data and Temperature Estimates.
https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007.txt

"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from milankovitch import ROOT


def clean(datafile: Path) -> pd.DataFrame:
    """
    Clean the text data
    Returns: a dataframe

    """
    tempfile = "temp.csv"

    # discard first 91 lines
    with open(datafile, "r", errors="replace") as f:
        lines = f.readlines()
        lines = lines[91:]

    with open(tempfile, "w") as f:
        f.writelines(lines)

    df = pd.read_csv("temp.csv", delim_whitespace=True)
    Path.unlink(tempfile)

    return df


def interpolate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolate a dataframe
    Args:
        df: the dataframe to interpolate

    Returns: an interpolated dataframe

    """
    # convert year to '000 of years
    df["Age"] = df["Age"] / 1000

    MAX_AGE = 800
    x = np.linspace(0.0, MAX_AGE, MAX_AGE + 1)
    y = np.interp(x, df["Age"], df["Temperature"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age(kYr)", "Temperature(degC)"])
    df = df.dropna()

    return df


def epica_domec_800kr_temperature() -> pd.DataFrame:
    """
    Process the EPICA dataset and return a dataframe.

    Data is temperature difference from the average of the last 1000 years in degC ppm for the timeseries [0, 800] kYears
    years.

    Returns: a dataframe with the data

    """
    datafile = ROOT / "data" / "1634220214_2023-04-05/data/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007.txt"
    df = clean(datafile)
    df = interpolate(df)

    return df


if __name__ == "__main__":
    df = epica_domec_800kr_temperature()
    print(df)

    df.plot(x="Age(kYr)", y="Temperature(degC)")
    plt.show()
