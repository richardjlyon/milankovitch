"""
composite.py

Plots a composite figure of Antarctic CO2, temperature and dust, and global sea level.

"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from milankovitch import PLOTDIR
from milankovitch.sources import *
from milankovitch.utils import compute_fft, orbital_parameters

np.seterr(divide='ignore')


def normalise(df: pd.DataFrame, data_col: str, normalised_col: str) -> pd.DataFrame:
    """
    Adds a column of data with the data_col normalised to the range [0,1]
    Returns: dataframe with normalised colum as `data_col_norm`

    """
    df[normalised_col] = (df[data_col] - np.min(df[data_col])) / (np.max(df[data_col]) - np.min(df[data_col]))

    return df


def plot_composite():
    # get sources
    df_temp = epica_domec_800kr_temperature()
    df_co2 = epica_domec_800kr_co2()
    df_sealevel = rses_sealevel()
    df_dust = epica_domec_800kr_dust()

    # ffts

    df_temp_fft = compute_fft(df_temp, "Temperature(degC)", 120)
    df_co2_fft = compute_fft(df_co2, "CO2(ppm)", 120)
    df_sealevel_fft = compute_fft(df_sealevel, "RSL(m)", 120)

    # construct a normalised set

    df_temp = normalise(df_temp, "Temperature(degC)", "Temp(norm)")
    df_co2 = normalise(df_co2, "CO2(ppm)", "CO2(norm)")
    df_sealevel = normalise(df_sealevel, "RSL(m)", "Sealevel(norm)")

    f, (ax0, ax1) = plt.subplots(2, 1, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4)
    f.suptitle("Effect of orbital parameters on global sea level, and Antarctic CO2 and temperature")

    # plot temperature, CO@, and sea level

    df_temp.plot(ax=ax0, x="Age(kYr)", y="Temp(norm)", color="tab:red")
    df_co2.plot(ax=ax0, x="Age(kYr)", y="CO2(norm)", color="tab:green")
    df_sealevel.plot(ax=ax0, x="Age(kYr)", y="Sealevel(norm)", color="tab:blue", )
    ax0.invert_xaxis()
    ax0.set_xlabel("Age ('000 years before present)")

    # plot power spectra

    df_temp_fft.plot(ax=ax1, x="periods", y="power", color="tab:red", legend=None)
    df_co2_fft.plot(ax=ax1, x="periods", y="power", color="tab:green", legend=None)
    df_sealevel_fft.plot(ax=ax1, x="periods", y="power", color="tab:blue", legend=None)

    # plot annotations

    for p in orbital_parameters:
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

    plotname = PLOTDIR / "composite.png"
    plt.savefig(plotname)
    print(f"Saved `{plotname}`")

    plt.show()


if __name__ == "__main__":
    plot_composite()
