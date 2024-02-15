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


dir_gen_packet = "../src/generate_packet/"
argvs = ['data.txt', 'gold_sequence.txt', 'gold_seq_end.txt', 'data_bin.txt' ]

for i in range(len(argvs)):
    argvs[i] = dir_gen_packet + argvs[i]

module_gen_header = "generate_packet"

data = "Test"

file = open(argvs[0], "w")
file.write(data)
file.close()
#sys.exit()
subprocess.call([dir_gen_packet + module_gen_header] + argvs)
time.sleep(1)

file = open(argvs[-1], "r")

data_bin = file.read()
data_bin = list(map(int, data_bin))
#data_bin = data_bin[:10]
for i in data_bin:
    print(i, end="")

plt.figure(1, figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.title("Data")
plt.plot(data_bin)
N = 10
data_rep = sample.duplication_sample(data_bin, N)
data_qpsk = sample.encode_QPSK(data_rep, 4)

plt.subplot(2, 2, 2)
plt.title("Data duplicate")
plt.plot(data_rep)

plt.subplot(2, 2, 3)
plt.title("BPSK")
plt.scatter(data_qpsk.real, data_qpsk.imag)


h1 = np.ones(N)
# Noise
pos_read = 0
noise_coef = 0.01
data_noise = data_qpsk[0:] 
noise = np.random.normal(0, noise_coef, len(data_noise))
data_noise += noise

plt.subplot(2, 2, 4)
plt.title(f"BPSK + noise({noise_coef})")
plt.scatter(data_noise.real, data_noise.imag)

data_conv = np.convolve(h1,data_noise,'full')

plt.figure(3, figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.title("data convolve")
plt.plot(data_conv)

#eye diagram
data_conv_real = data_conv.real
plt.subplot(2, 2, 2)
for i in range(0,len(data_conv_real), N):
     plt.plot(data_conv_real.real[0:N*2])
     data_conv_real1 = np.roll(data_conv_real,-1* N)
     data_conv_real= data_conv_real1


def gardner_TED(data):
    error = 0
    tau = 2
    t1 = 1
    errors = [0 for i in range(len(data))]
    for i in range(1, len(data)):
        t1 = i
        t2 = t1 + tau
        errors[i] = (data.real[i-1]) % N
    

def rrc_filter(N, beta):
# Impulse response of the root rise cosine filter given the number of samples
# Inputs:
# beta: roll-off factor
# p: time samples of the filter
# num_samples: number of samples, must be a even number
# T_samples: number of samples per signal period
    
    Ts = 1
    t = (1/Ts)*np.linspace(-Ts/np.sqrt(1+beta/2), Ts/np.sqrt(1+beta/2), N)
    p = np.zeros(len(t));
    for i in np.arange(len(t)):
        p[i] = (4*beta/(np.pi*np.sqrt(Ts)))*(np.cos((1+beta)*np.pi*t[i]/Ts) +np.sin((1-beta)*np.pi*t[i]/Ts)/(4*beta*t[i]/Ts))/(1-(4*beta*t[i]/Ts)**2)
        
    t_0 = 0
    t_0 = [i for i in range(len(t)) if t[i] == 0.0] 
    if (t_0 != 0):
        p[t_0] = (4*beta/(np.pi*np.sqrt(Ts)))*(1 + (1-beta)*np.pi/(4*beta))

    t_1 = Ts/(4*beta)
    t_1p = 0
    t_1m = 0
    t_1p =  [i for i in range(len(t)) if t[i] == t_1]
    t_1m = [i for i in range(len(t)) if t[i] == -t_1]
    if (t_1p != 0):
        p[t_1p] = (beta/np.sqrt(2*Ts))*((1+2/np.pi)*np.sin(np.pi/(4*beta)) + (1-2/np.pi)*np.cos(np.pi/(4*beta)))
        p[t_1m] = (beta/np.sqrt(2*Ts))*((1+2/np.pi)*np.sin(np.pi/(4*beta)) + (1-2/np.pi)*np.cos(np.pi/(4*beta)))
      
    p = p - np.amin(p)
    # Guarantizes normalized energy
    p = p/np.sum(p)

    return np.resize(p, (100,1))

#gardner_TED(data_conv)
rrc_filter(N, data_conv.real)


