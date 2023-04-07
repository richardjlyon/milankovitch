"""
co2.py

A CO2 dataset using the NOAA EPICA Dome C - 800KYr CO2 Data.
https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3-composite-co2-2008-noaa.txt

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
        lines = lines[275:]

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
    df["gas_ageBP"] = df["gas_ageBP"] / 1000

    MAX_AGE = 800
    x = np.linspace(0.0, MAX_AGE, MAX_AGE + 1)
    y = np.interp(x, df["gas_ageBP"], df["CO2"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age(kYr)", "CO2(ppm)"])
    df = df.dropna()
    df = df.astype({"Age(kYr)": int})

    return df


def epica_domec_800kr_co2() -> pd.DataFrame:
    """
    Process the EPICA dataset and return a dataframe.

    Data is CO2 in ppm for the timeseries [0, 800000] years.

    Returns: a dataframe with the data

    """
    datafile = ROOT / "data" / "1634220214_2023-04-05/data/pub/data/paleo/icecore/antarctica/epica_domec/edc3-composite-co2-2008-noaa.txt"
    df = clean(datafile)
    df = interpolate(df)

    return df


if __name__ == "__main__":
    df = epica_domec_800kr_co2()
    print(df)

    df.plot(x="Age(kYr)", y="CO2(ppm)")
    plt.show()
