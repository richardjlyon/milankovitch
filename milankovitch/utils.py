import math

import pandas as pd

from milankovitch import ROOT


def load_data(filename: str) -> pd.DataFrame:
    """Load the data from an excel spreadsheet."""
    filename = ROOT / 'data' / filename
    df = pd.read_excel(filename)

    return df


def next_power_of_2(x):
    """Compute the smallest power of 2 greater than or equal to x."""
    return 1 if x == 0 else math.ceil(math.log2(x))
