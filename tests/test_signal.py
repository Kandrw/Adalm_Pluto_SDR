import os
import sys

import numpy as np
from scipy import signal
from scipy.signal import max_len_seq
from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import matplotlib.pyplot as plt
import subprocess
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import tx_rx.conf as conf

import sample.sample as sample



rf_module = conf.RxTx()


rf_module.print_parameters()


dir_gen_packet = "..\src\generate_packet\\"
argvs = ['data.txt', 'gold_sequence.txt', 'gold_seq_end.txt', 'data_bin.txt' ]

for i in range(len(argvs)):
    argvs[i] = dir_gen_packet + argvs[i]

module_gen_header = "generate_packet.exe"

data = "Test data"

file = open(argvs[0], "w")
file.write(data)
file.close()
#sys.exit()
subprocess.call([dir_gen_packet + module_gen_header] + argvs)

time.sleep(1)

file = open(argvs[-1], "r")

data_bin = file.read()
data_bin = list(map(int, data_bin))
for i in data_bin:
    print(i, end="")

plt.figure(1, figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.title("Data")
plt.plot(data_bin)








