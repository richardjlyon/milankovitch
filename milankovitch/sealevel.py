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

from milankovitch.utils import load_data, next_power_of_2, gaussian_filter

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
    """Interpolate sea level data with N points."""
    x = np.linspace(0.0, N, N + 1)
    y = np.interp(x, df["Age_kaBP"], df["RSL_m"])

    df = pd.DataFrame(list(zip(x, y)), columns=["Age_kaBP", "RSL_m"])

    return df


def compute_fft(df) -> pd.DataFrame:
    """Compute fft."""

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

    # Dataframe of periods less that 150,000 years
    df = pd.DataFrame(list(zip(periods, power)), columns=["periods", "power"])
    df = df[df["periods"] < 120]

    return df


def filter(df: pd.DataFrame, fcentral: float = 0.1, width: float = 0.05) -> np.ndarray:
    """Filter the given signal."""

    # Number of points, a power of 2 larger than the number of the data
    N = 2 ** (next_power_of_2(len(df)) + 8)
    # Timestep ('000 years)
    T = 1

    frequencies = np.fft.rfftfreq(N, T)
    spectrum = np.fft.rfft(df["RSL_m"], N, norm="ortho")

    filtered_spectrum = gaussian_filter(frequencies, spectrum, fcentral, width)
    filtered_series = np.fft.irfft(filtered_spectrum, N, norm='ortho')

    return filtered_series[:len(df)]


if __name__ == "__main__":
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

    # plot power spectra

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
    plt.show()
