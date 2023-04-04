import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from milankovitch.utils import load_data, next_power_of_2, gaussian_filter

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
np.seterr(divide='ignore')
plt.style.use("../style/elegant.mplstyle")


def prepare(df: pd.DataFrame, N: int = 500) -> pd.DataFrame:
    """Interpolate sea level data with N points."""
    x = np.linspace(0.0, N, N + 1)
    y = np.interp(x, df["Age_kaBP"], df["RSL_m"])

    df = pd.DataFrame(y, index=x, columns=["RSL_m"])
    df.index.name = "Age_kaBP"

    return df


def compute_fft(df) -> pd.DataFrame:
    """Compute fft."""

    # Number of points, a power of 2 larger than the number of the data
    N = 2 ** (next_power_of_2(len(df)) + 8)

    # Timestep ('000 years)
    T = 1

    # Normalise sea level data to mean
    df["RSL_m"] = df["RSL_m"] - np.mean(df["RSL_m"])

    # Compute normalised power spectrum and periods
    spectrum = np.fft.rfft(df["RSL_m"], N, norm="ortho")

    power = np.real(spectrum.conj() * spectrum)
    power = power / np.max(power)
    frequencies = np.fft.rfftfreq(N, T)
    periods = 1 / frequencies

    # Gaussian filter
    filtered_spectrum = gaussian_filter(frequencies, spectrum, 0.1, 0.05)
    filtered_series = np.fft.irfft(filtered_spectrum, N, norm='ortho')
    # plt.plot(filtered_series[:600])
    # plt.plot(filtered_spectrum)
    # plt.show()

    # Dataframe of periods less that 150,000 years
    df = pd.DataFrame(list(zip(periods, power)), columns=["periods", "power"])
    df = df[df["periods"] < 150]

    return df


if __name__ == "__main__":
    df = load_data('RSL_data.xlsx')
    df_sealevel = prepare(df)
    df_power = compute_fft(df_sealevel)

    df_sealevel.plot()

    df_power.plot(x="periods", y="power")
    plt.gca().invert_xaxis()
    plt.show()
