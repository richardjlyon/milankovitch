import math
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class OrbitalParameter:
    """Class for representing orbital parameter."""
    name: str
    period_years: int


orbital_parameters = [
    OrbitalParameter(name="Orbital Ellipticity", period_years=100_000),
    OrbitalParameter(name="Axial tilt", period_years=41_000),
    OrbitalParameter(name="Axial precession", period_years=23_000)
]


def next_power_of_2(x):
    """Compute the smallest power of 2 greater than or equal to x."""
    return 1 if x == 0 else math.ceil(math.log2(x))


def compute_fft(df: pd.DataFrame, data_col: str) -> pd.DataFrame:
    """
    Compute the Fourier Transform into the frequency domain.
    Args:
        df: A dataframe containing sea level data as a timeseries
        max_period: The maximum period to return (in thousands of years)

    Returns: A Dataframe of periods and signal power

    """

    # Number of points, a power of 2 larger than the number of the data
    N = 2 ** (next_power_of_2(len(df)) + 8)

    # Timestep ('000 years)
    T = 1

    # Normalise sea level data to mean
    df_copy = df.copy()
    df_copy[data_col] = df_copy[data_col] - np.mean(df_copy[data_col])

    # Compute normalised power spectrum and periods
    frequencies = np.fft.rfftfreq(N, T)
    periods = 1 / frequencies

    spectrum = np.fft.rfft(df_copy[data_col], N, norm="ortho")
    power = np.real(spectrum.conj() * spectrum)
    power = power / np.max(power)

    # Dataframe of periods less than max_period years
    df = pd.DataFrame(list(zip(periods, power)), columns=["periods", "power"])

    return df
