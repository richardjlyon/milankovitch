# dust.py
#
# Computes the power spectrum of historical Antarctic dust and plots, noting the
# periods of the dominant orbital parameters (Orbital eccentricity, Axial tilt, and Axial precession
#
# Richard Lyon
#
# 1 April 2023

import warnings

import matplotlib.pyplot as plt
import numpy as np

from milankovitch import PLOTDIR
from milankovitch.sources import epica_domec_800kr_dust
from milankovitch.utils import orbital_parameters, compute_fft

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
np.seterr(divide='ignore')
plt.style.use("../style/elegant.mplstyle")


def plot_dust():
    df_dust = epica_domec_800kr_dust()
    df_fft = compute_fft(df_dust, "Dust(ng/g)")
    df_fft = df_fft[df_fft["periods"] < 120]

    f, (ax0, ax1) = plt.subplots(2, 1, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4)
    f.suptitle("Effect of orbital parameters on Antarctic dust")

    # plot sea level

    df_dust.plot(ax=ax0, x="Age(kYr)", y="Dust(ng/g)", legend=None)
    ax0.invert_xaxis()
    ax0.set_title("Dust")
    ax0.set_xlabel("Age ('000 years before present)")
    ax0.set_ylabel("ng/g")

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

    plotname = PLOTDIR / "dust.png"
    plt.savefig(plotname)
    print(f"Saved `{plotname}`")

    plt.show()


if __name__ == "__main__":
    plot_dust()
