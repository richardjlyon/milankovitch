# Milankovitch
#
# Computes the power spectrum of historical global sea levels and plots, noting the
# periods of the dominant orbital parameters (Orbital eccentricity, Axial tilt, and Axial precession
#
# Richard Lyon
#
# 1 April 2023

import warnings
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from milankovitch.utils import load_data, next_power_of_2

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
np.seterr(divide='ignore')
plt.style.use("../style/elegant.mplstyle")


@dataclass
class OrbitalParameter:
    """Class for representing orbital parameter."""
    name: str
    period_years: int


parameters = [
    OrbitalParameter(name="Orbital Ellipticity", period_years=100_000),
    OrbitalParameter(name="Axial tilt", period_years=41_000),
    OrbitalParameter(name="Axial precession", period_years=23_000)
]


def prepare(df: pd.DataFrame, N: int = 500) -> pd.DataFrame:
    """
    Interpolate sea level data with N points.
    Args:
        df: A dataframe containing sea level data as a timeseries
        N: The number of points in the interpolated set

    Returns: A Dataframe of interpolated data

    """
    x = np.linspace(0.0, N, N + 1)
    y = np.interp(x, df["Age_kaBP"], df["RSL_m"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age_kaBP", "RSL_m"])

    return df


def compute_fft(df: pd.DataFrame, max_period: int = 120) -> pd.DataFrame:
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
    df_copy["RSL_m"] = df_copy["RSL_m"] - np.mean(df_copy["RSL_m"])

    # Compute normalised power spectrum and periods
    spectrum = np.fft.rfft(df_copy["RSL_m"], N, norm="ortho")

    power = np.real(spectrum.conj() * spectrum)
    power = power / np.max(power)
    frequencies = np.fft.rfftfreq(N, T)
    periods = 1 / frequencies

    # Dataframe of periods less than max_period years
    df = pd.DataFrame(list(zip(periods, power)), columns=["periods", "power"])
    df = df[df["periods"] < max_period]

    return df


def plot_sealevel():
    df = load_data('RSL_data.xlsx')
    df_sealevel = prepare(df)
    df_fft = compute_fft(df_sealevel)

    f, (ax0, ax1) = plt.subplots(2, 1, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4)
    f.suptitle("Effect of orbital parameters on global sea level")

    # plot sea level

    df_sealevel.plot(ax=ax0, x="Age_kaBP", y="RSL_m", legend=None)
    ax0.invert_xaxis()
    ax0.set_title("Sea Level")
    ax0.set_xlabel("Age ('000 years before present)")
    ax0.set_ylabel("Sea Level [m]")

    # plot power spectrum

    df_fft.plot(ax=ax1, x="periods", y="power", color="tab:red", legend=None)
    ax1.set_title("Milankovitch Cycle components")
    ax1.set_xlabel("Period ('000 years)")
    ax1.set_ylabel("Power (relative)")
    ax1.invert_xaxis()

    # plot annotations

    for p in parameters:
        ax1.axvline(p.period_years / 1000, linestyle="--", color="black")
        ax1.annotate(p.name, xy=(p.period_years / 1000, 0), xytext=(-10, 25), textcoords='offset points',
                     rotation=90,
                     va='bottom', ha='center')

    ax1.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (-50, -50),
        xycoords="axes pixels",
        textcoords="offset pixels",
        va="top",
        color="lightgrey",
    )

    plt.savefig("milankovitch.png")
    print("Saved `milankovitch.png`")
    plt.show()


if __name__ == "__main__":
    plot_sealevel()
