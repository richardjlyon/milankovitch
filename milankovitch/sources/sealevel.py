"""
sealevel.py

A sealevel dataset using the Research School of Earth Sciences dataset
https://github.com/ANU-RSES-Education/EMSC-4033/tree/master/Notebooks/StepByStep/Ex17

"""
from pathlib import Path

import numpy as np
import pandas as pd

from milankovitch import ROOT


def clean(datafile: Path) -> pd.DataFrame:
    """
    Clean the text data
    Returns: a dataframe

    """
    df = pd.read_excel(datafile)
    # df["Age_kaBP"] = df["Age_kaBP"] * 1000

    return df


def interpolate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolate a dataframe
    Args:
        df: the dataframe to interpolate

    Returns: an interpolated dataframe

    """
    MAX_AGE = 500
    x = np.linspace(0.0, MAX_AGE, MAX_AGE + 1)
    y = np.interp(x, df["Age_kaBP"], df["RSL_m"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age(Year)", "RSL(m)"])
    df = df.astype({"Age(Year)": int})

    return df


def rses_sealevel() -> pd.DataFrame:
    """
    Process the RSES dataset and return a dataframe.

    Data is sealevel in meters relative to current  for the timeseries [0, 500_000] years.

    Returns: a dataframe with the data

    """
    datafile = ROOT / "data" / 'RSL_data.xlsx'
    df = clean(datafile)
    df = interpolate(df)

    return df


if __name__ == "__main__":
    rses_sealevel()
