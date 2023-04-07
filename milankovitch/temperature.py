# temperature.py
#
# Computes the power spectrum of historical temperature and plots, noting the
# periods of the dominant orbital parameters (Orbital eccentricity, Axial tilt, and Axial precession
#
# Richard Lyon
#
# 1 April 2023

import warnings

import matplotlib.pyplot as plt
import numpy as np

from milankovitch import PLOTDIR
from milankovitch.sources import epica_domec_800kr_temperature
from milankovitch.utils import orbital_parameters, compute_fft

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
np.seterr(divide='ignore')
plt.style.use("../style/elegant.mplstyle")


def plot_temperature():
    df_temp = epica_domec_800kr_temperature()
    df_fft = compute_fft(df_temp, "Temperature(degC)")
    df_fft = df_fft[df_fft["periods"] < 120]

    f, (ax0, ax1) = plt.subplots(2, 1, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4)
    f.suptitle("Effect of orbital parameters on Antarctic temperature")

    # plot sea level

    df_temp.plot(ax=ax0, x="Age(kYr)", y="Temperature(degC)", legend=None)
    ax0.invert_xaxis()
    ax0.set_title("Temperature")
    ax0.set_xlabel("Age ('000 years before present)")
    ax0.set_ylabel("degC")

    # plot power spectrum

    df_fft.plot(ax=ax1, x="periods", y="power", color="tab:red", legend=None)
    ax1.set_title("Milankovitch Cycle components")
    ax1.set_xlabel("Period ('000 years)")
    ax1.set_ylabel("Power (relative)")
    ax1.invert_xaxis()

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

    plotname = PLOTDIR / "temperature.png"
    plt.savefig(plotname)
    print(f"Saved `{plotname}`")

    plt.show()


if __name__ == "__main__":
    plot_temperature()
