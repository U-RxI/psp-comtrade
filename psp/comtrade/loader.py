import numpy as np
from psp.dsp.filters import dft, true_rms

def process_ch(rec: object, idx: int, opt: str = "primary"):
    """
    Function to load an analog channel from a Comtrade object.
    The functions will consider whether the recorded channel is in primary or secondary, and return primary or
    secondary based the input option opt.

    Parameters
    ----------
    rec : object
        The comtrade file record loaded into the Comtrade class using the module comtrade.
    idx : int
        Index of the channel to load.
    opt : str, optional
        Option for the return array being in primary or secondary values. The default is 'primary'.

    Returns
    -------
    TYPE
        Numpy array with the analog values from rec.analog_channels[idx] either in primary or secondary.

    """

    # Ratio of CT / VT
    a = rec.cfg.analog_channels[idx].primary / rec.cfg.analog_channels[idx].secondary

    # Check if comtrade file is stored as secondary or primary values
    if rec.cfg.analog_channels[idx].pors.upper() == "S":
        x_sec = np.array(rec.analog[idx])
        x_prim = np.array(rec.analog[idx]) * a

    if rec.cfg.analog_channels[idx].pors.upper() == "P":
        x_sec = np.array(rec.analog[idx]) / a
        x_prim = np.array(rec.analog[idx])

    # Return primary or secondary values
    if opt.lower() in ("primary", "prim"):
        return x_prim

    if opt.lower() in ("secondary", "sec"):
        return x_sec

def load_ch(rec, idx, N, opt: str = "primary"):
    x = process_ch(rec, idx, opt)
    x_dft = dft(x, N)
    x_rms = true_rms(x, N)
    return x, x_dft, x_rms