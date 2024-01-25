import os
import sys

import numpy as np
from scipy import signal
from scipy.signal import max_len_seq
from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import tx_rx.conf as conf

import sample.sample as sample



rf_module = conf.RxTx()


rf_module.print_parameters()



data = "BIG DATA"

data_bin = sample.data_to_byte(data)


