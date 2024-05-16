#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:23:24 2024

@author: plutosdr
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:17:56 2024

@author: plutosdr
"""


import os
import sys

import numpy as np
from scipy import signal
from scipy.signal import max_len_seq
from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import matplotlib.pyplot as plt
import subprocess
import time
import datetime

import platform

def EXIT(show = 1):
    #plt.ion()
    #plt.pause(100)
    if(show):
        plt.show()
    sys.exit()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import tx_rx.conf as conf

import sample.sample as sample



def norm_corr(x,y):
    #x_normalized = (cp1 - np.mean(cp1)) / np.std(cp1)
    #y_normalized = (cp2 - np.mean(cp2)) / np.std(cp2)

    c_real = np.vdot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
    c_imag = np.vdot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
    
    return c_real+1j*c_imag

def indexs_of_CP_after_PSS(rx, cp, fft_len):
    """
    Возвращает массив начала символов (вместе с CP) (чтобы только символ был нужно index + 16)
    """
    corr = [] # Массив корреляции 

    for i in range(len(rx) - fft_len):
        o = norm_corr((rx[:cp]), rx[fft_len:fft_len+cp])

        corr.append(abs(o))
        rx = np.roll(rx, -1)

    corr = np.array(corr) / np.max(corr) # Нормирование
    max_len_cycle = len(corr)
    # if corr[0] > 0.97:
    #     max_len_cycle = len(corr)
    # else:
    #     max_len_cycle = len(corr)-(fft_len+cp)

    ind = np.argmax(corr[0 : (fft_len+cp)// 2 ])
    arr_index = [] # Массив индексов максимальных значений corr
    arr_index.append(ind)
    for i in range((fft_len+cp) // 2, max_len_cycle, (fft_len+cp)):
        #print(i, i+(fft_len+cp))
        max = np.max(corr[i : i+(fft_len+cp)])
        if max > 0.90: 
            ind = i + np.argmax(corr[i : i+(fft_len+cp)])
            if ind < (len(corr)):
                arr_index.append(ind)
    
    ### DEBUG
    
    # print(corr)
    #plt.figure()
    #plt.plot(abs(corr))
    #plt.show()
    return arr_index


def indiv_symbols(ofdm, N_fft, CP_len):
    cp = CP_len
    all_sym = N_fft + cp
    
    
    index = indexs_of_CP_after_PSS(ofdm, cp, N_fft)
    index = index[:5]
    symbols = []
    for ind in index:
        symbols.append(ofdm[ind+cp : ind+all_sym])
        
    return np.asarray(symbols)



PLATFORM = platform.system()#"Linux"

sample_rate  = 1000000

IF_SDR = 1#True
READ_FILE = 0#Если True, то игнорируются блоки: 1, 2, 3, 4, сигнал считывается из файла
COUNT_SDR = 1 # 1-2
CON = 1# метод обработки сигнала (1, 2)
IF_PSS = 1#True


filename_output = "input_qpsk.txt" #файл записи принятого сигнала

print("Platform:", PLATFORM)

def config_(sdr):
    
    F_n = 2900100011
    sdr.sample_rate = sample_rate
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
    #sdr.rx_lo = 1900100011
    #sdr.tx_lo = 1900100011
    sdr.rx_lo = F_n
    sdr.tx_lo = F_n
    sdr.tx_cyclic_buffer = True
    #sdr.tx_cyclic_buffer = False
    sdr.tx_hardwaregain_chan0 = 0
    sdr.rx_hardwaregain_chan0 = 20
    #sdr.gain_control_mode_chan0 = "slow_attack"
    sdr.gain_control_mode_chan0 = "manual"
    
def resource_grid_3(data1, Nfft, cp): 
    """
        data - matrix
        count_frame - количество OFDM фреймов бля ресурсной сетки
        len_frame - количество ofdm-символов в ofdm фрейме
        Nftt - количество поднесущих
        cp - защитный префикс

    """
    #data1 = data[:(Nfft)*len_frame*count_frames]
    half_nfft = Nfft//2

    # преобразуем в матрицу 
    data_freq = data1.reshape(2, (Nfft+cp))

    # обрезаем циклический префикс
    data1 = data_freq[:, cp:]
    # производим обратное преобразование фурье и транспонируем матрицу для удобного вывода на карте

    data2 = np.fft.fft(data1).T

    # переставляем строки местами из-за не шифтнутых частот
    #temp = np.copy(data2[0:half_nfft, :])
    #data2[0:half_nfft, :] = data2[half_nfft:Nfft, :]
    #data2[half_nfft:Nfft, :] = temp

    plt.figure()
    plt.imshow(abs(data2), cmap='jet',interpolation='nearest', aspect='auto')
    plt.colorbar()
    #plt.show()


#rf_module = conf.RxTx(adi.Pluto('ip:192.168.2.1'))
#rf_module.print_parameters()

def sqrt_rc_imp(ns, alpha, m):
    n = np.arange(-m * ns, m * ns + 1)
    b = np.zeros(len(n))
    ns *= 1.0
    a = alpha
    for i in range(len(n)):
       #if abs(1 - 16 * a ** 2 * (n[i] / ns) ** 2) <= np.finfo(np.float32).eps/2:
        #   b[i] = 1/2.*((1+a)*np.sin((1+a)*np.pi/(4.*a))-(1-a)*np.cos((1-a)*np.pi/(4.*a))+(4*a)/np.pi*np.sin((1-a)*np.pi/(4.*a)))
       #else:
           b[i] = 4*a/(np.pi * (1 - 16 * a ** 2 * (n[i] / ns) ** 2))
           b[i] = b[i]*(np.cos((1+a) * np.pi * n[i] / ns) + np.sinc((1 - a) * n[i] / ns) * (1 - a) * np.pi / (4. * a))
    return b    

## PARAMETRS
if 1:
    N2 = 10#длительность символа
    #data_qpsk = sample.duplication_sample(data_qpsk, N2)
    #Количество поднесущих
    Nb = 64
    #Защитный интервал
    N_interval = 16
    RS = 4 # < Nb
    Nz = 10 # < Nb
    
    pilot = 5009.7 + 5009.7j
    pilot *= 3.2
    #pilot = 100009.7 + 100009.7j
    #pilot = 18000.7 + 18000.7j
    #pilot *= 2 ** 3
    if IF_PSS:
        pss = [0, 1, 1, 1, 0, 1, 0, 1, 0, 
               0, 1, 0, 1, 0, 0, 0, 1, 0, 
               1, 1, 1, 0, 0, 1, 1, 0, 1,
               1, 0, 1, 1, 0, 0, 1, 0, 1,
               1, 1, 1, 1, 0, 1, 1, 0, 1,
               1, 1, 0, 0, 0, 1, 1, 0, 1,
               1, 0, 1, 0, 1, 0, 1, 0, 1
               ]
        
        #pss_fft = sample.PSS_to_freq(pss[:20])
        #EXIT(1)
        pss_fft = np.array(pss) + np.array(pss) * 1j
        pss_fft *= 2 ** 14
        pss_fft = np.fft.ifft(pss_fft)
        print("len pss = ", len(pss_fft))
        plt.figure(5, figsize=(10, 10))
        plt.subplot(2, 2, 1)
        plt.title("PSS")
        plt.plot(abs(np.fft.fft(pss_fft)))

if READ_FILE == 0:
    ## BLOCK 1 - формирование сигнала (11 - 20)
    print("BLOCK 1")
    dir_gen_packet = "../src/generate_packet/"
    argvs = ['data.txt', 'gold_sequence.txt', 'gold_seq_end.txt', 'data_bin.txt' ]

    for i in range(len(argvs)):
        argvs[i] = dir_gen_packet + argvs[i]

    module_gen_header = "generate_packet"
    if(PLATFORM == "Windows"):
        module_gen_header += ".exe"

    data = "Andrey Karpenko"
    data = "ert"
    file = open(argvs[0], "w")
    file.write(data)
    file.close()
    #EXIT()
    subprocess.call([dir_gen_packet + module_gen_header] + argvs)

    time.sleep(1)

    file = open(argvs[-1], "r")

    data_bin = file.read()
    data_bin = list(map(int, data_bin))
    for i in data_bin:
        print(i, end="")

    #data = np.random.randint(0, 2, 200)
    #data_bin = data
    plt.figure(11, figsize=(10, 10))
    plt.subplot(2, 2, 1)
    plt.title("Data")
    plt.plot(data_bin)

    N = 10
    data_rep = data_bin
    N_qam = 4
    data_qpsk = np.array(sample.encode_QAM(data_rep, N_qam))
    #data_qpsk = sample.encode_QPSK(data_rep, 4)
    

    fs = sample_rate
    rs=100000
    ns=fs//rs


    data_qpsk = np.array(data_qpsk)
    plt.subplot(2, 2, 2)
    plt.title(f"QAM{N_qam}")
    plt.scatter(data_qpsk.real, data_qpsk.imag)

        



    #gardner_TED(data_conv)
    #rrc_filter(N, data_conv.real)

    #sdr.rx_rf_bandwidth = 1000000
    #sdr.rx_destroy_buffer()
    #sdr.rx_hardwaregain_chan0 = -5

    data_qpsk *= 2**14
    plt.subplot(2, 2, 4)
    plt.title(f"QAM{N_qam} ** 14")
    plt.scatter(data_qpsk.real, data_qpsk.imag)


    #sample.OFDM_modulator(data_qpsk, Nb)

        #OFDM
    Nc = N_qam
    ofdm_argv = sample.OFDM_modulator(data_qpsk, Nb, N_interval, pilot, RS, Nz)
    ofdm_tx = ofdm_argv[0]
    count_ofdm = ofdm_argv[1]
    #ofdm_indexes = ofdm_argv[2]
    plt.figure(12, figsize=(10, 10))
    plt.subplot(2, 2, 1)
    plt.title("OFDM, count " + str(ofdm_argv[1]))
    
    plt.plot(abs(np.fft.fft(ofdm_tx,int(1e6))))
    len_data_tx = len(ofdm_tx)
    len_one_ofdm = int(len_data_tx / count_ofdm)
    print("len_data_tx = ", len_data_tx)
    #f1 = open(, "w")
    resource_grid_3(ofdm_tx, Nb, N_interval)
    if IF_PSS:
        ofdm_tx = sample.add_PSS(ofdm_tx, pss_fft)
        
    np.savetxt("data_save/tx" + str(datetime.datetime.now()) + ".txt", ofdm_tx.view(float))
    #f1.write(str(ofdm_tx))
    #f1.close()
    
    
    if IF_SDR:
        ## BLOCK 2 - настройка SDR (21-30)
        print("BLOCK 2: SDR")
        import adi
        sdr = adi.Pluto('ip:192.168.2.1')
        
        sdr2 = sdr
        sdr2 = adi.Pluto('ip:192.168.3.1')
        config_(sdr)
        config_(sdr2)
        sdr.rx_buffer_size =2*len(data_qpsk) *40
        sdr2.rx_buffer_size =2*len(data_qpsk) *40

    ## BLOCK 3 - отправка сигнала (31-40)
    
    print("BLOCK 3")
    if IF_SDR:
        sdr.rx_buffer_size =2*len(ofdm_tx) * 40
        sdr2.rx_buffer_size =2*len(ofdm_tx) * 40
        print("Отправлено:", len(ofdm_tx))
        sdr.tx(ofdm_tx)
        
        #time.sleep(1)
    else:
        #Добавление шума
        print("Add noise")
        plt.figure(31, figsize = (10, 10))
        
        e = 1000
        e_no_data = 1000
        np.random.normal
        start_t_data = 40
        len_end = 50
        print
        noise = np.random.normal(loc=-e, scale=e, size= start_t_data + len(ofdm_tx) + len_end)
        noise = noise + noise * 1j
        
        plt.subplot(2, 2, 1)
        plt.title("Noise")
        plt.plot(noise)
        ofdm_rx = ofdm_tx #/ 50
        noise_s = np.random.normal(loc=-e, scale=e, size= start_t_data + len(ofdm_tx) + len_end)
        noise = noise + noise * 1j
        if 1:
            t_s = np.random.normal(loc=-e_no_data, scale=e_no_data, size= start_t_data)
            t_s = t_s + t_s * 1j
            t_e = np.random.normal(loc=-e_no_data, scale=e_no_data, size= len_end)
            t_e = t_e + t_e * 1j
        else:
            t_s = np.zeros(start_t_data, dtype="complex_")
            t_e = np.zeros(len_end, dtype="complex_")
        print("Позиция данных в канале:", len(t_s))
        ofdm_rx = np.concatenate([t_s, ofdm_rx, t_e])
        if 1:
            ofdm_rx += noise
        plt.subplot(2, 2, 2)
        plt.title("Data + Noise")
        plt.plot(ofdm_rx)
        plt.subplot(2, 2, 3)
        plt.title("Data + Noise")
        plt.plot(abs(np.fft.fft(ofdm_rx,int(1e6))))


    ## BLOCK 4 - принятие сигнала  (41-50)
    if IF_SDR:
        print("BLOCK 4: rx SDR")
        ofdm_rx = sdr2.rx()
        np.savetxt("data_save/rx" + str(datetime.datetime.now()) + ".txt", ofdm_tx.view(float))
        np.savetxt(filename_output, ofdm_rx, delimiter=":")
        if IF_SDR:
            sdr.tx_destroy_buffer()
            sdr.rx_destroy_buffer()
            sdr2.tx_destroy_buffer()
            sdr2.rx_destroy_buffer()
else:
##    (41-50)
    ofdm_rx = np.loadtxt(filename_output, delimiter=":", dtype=complex)


## BLOCK 5 - обработка сигнала (51-60)
print("BLOCK 5")

if CON == 1:

    


    ofdm_rx_pss_calc = ofdm_rx.copy()

    if IF_PSS:
        if 0:
            start_data = -1
            if_start = 0.8 + 0.8j
            arr_cor_pos = []
            for i in range(0, len(ofdm_rx_pss_calc) - len(pss_fft)):
                
                a = sample.norm_corr(ofdm_rx_pss_calc[0:len(pss_fft)], 
                    pss_fft)
        
                #if start_data == -1 and a.real >= abs(if_start.real) and a.imag >= abs(if_start.imag):
                if start_data == -1 and abs(a) >= abs(if_start):
                
                    start_data = i + len(pss_fft)
                    #start_data = 58
                arr_cor_pos.append(a)
                ofdm_rx_pss_calc = np.roll(ofdm_rx_pss_calc, -1)
                
            print("Начало PSS:", start_data)
            plt.figure(50, figsize = (10, 10))
            plt.subplot(2, 2, 1)
            plt.title("Correlation PSS")
            plt.plot(arr_cor_pos)
        else:
            start_data = -1
            if_start = 0.8 + 0.8j
            max_corr = -0.5
            arr_cor_pos = []
            for i in range(0, len(ofdm_rx_pss_calc) - len(pss_fft)):
                
                a = sample.norm_corr(ofdm_rx_pss_calc[0:len(pss_fft)], 
                    pss_fft)
        
                #if start_data == -1 and a.real >= abs(if_start.real) and a.imag >= abs(if_start.imag):
                if abs(a) >= abs(max_corr)  :
                
                    start_data = i #+ len(pss_fft)
                    max_corr = a
                    #start_data = 58
                arr_cor_pos.append(abs(a))
                ofdm_rx_pss_calc = np.roll(ofdm_rx_pss_calc, -1)
                
            print("Начало PSS:", start_data, "max_corr:", max_corr, abs(max_corr))
            plt.figure(50, figsize = (10, 10))
            plt.subplot(2, 2, 1)
            plt.title("Correlation PSS")
            plt.plot(arr_cor_pos)
        
    else:
        start_data = 0
    if(start_data == -1):
        print("Не удалось определить начало PSS")
        EXIT()
    #ofdm_rx_2 = ofdm_rx.copy()
    #index1 = sample.correlat_ofdm(ofdm_rx_2, N_interval, Nb)
    #print("index1:", index1)
    ofdm_rx_2 = ofdm_rx.copy()
    ofdm_rx_2 = ofdm_rx_2[start_data:]
    
    
    # print("0 :", N_interval)
    # print(N_interval, ":", Nb)
    print("0 :", N_interval)
    print(len_one_ofdm - N_interval, ":", len_one_ofdm)
    
    ofdm_rx_2 = sample.calculate_correlation(Nb, ofdm_rx_2, 1e6 // Nb, pss_fft)
    ofdm_rx_3 = ofdm_rx_2.copy()
    CON2 = 2
    if 1 == CON2:  
        arr = []
        start_data = -1
        if_start = 0.95 + 0.95j
        for i in range(0, len(ofdm_rx_2) - Nb):
            
            #a = np.vdot(data_read2[0:N_interval], data_read2[Nb:Nb + N_interval])
           
            a = sample.norm_corr(ofdm_rx_2[0:N_interval], 
                                 ofdm_rx_2[len_one_ofdm - N_interval: len_one_ofdm])
            #a = abs(a)
            #print("a = ", abs(a.real), abs(a.imag), end = " | ")
            
            if start_data == -1 and a.real >= abs(if_start.real) and a.imag > (if_start.imag):
            #if start_data == -1 and a >= if_start:
                start_data = i
    
            # if start_data == -1 and -if_start <= a and a <= if_start:
            #     start_data = i
            arr.append(a)
            ofdm_rx_2 = np.roll(ofdm_rx_2, -1)
        plt.figure(51, figsize = (10, 10))
        plt.subplot(2, 2, 1)
        plt.title("Correlation")
        plt.plot(arr)
        if(start_data == -1):
            print("не удалось определить начало")
            EXIT()
        print("Начало данных:", start_data)
    elif 2 == CON2:
        arr = []
        start_data = -1
        if_start = 0.9 + 0.9j
        max_corr = -0.5
        for i in range(0, len(ofdm_rx_2) - Nb):
            
            #a = np.vdot(data_read2[0:N_interval], data_read2[Nb:Nb + N_interval])
           
            a = sample.norm_corr(ofdm_rx_2[0:N_interval], 
                                 ofdm_rx_2[len_one_ofdm - N_interval: len_one_ofdm])
            #a = abs(a)
            #print("a = ", abs(a.real), abs(a.imag), end = " | ")
            
            if abs(a) > abs(max_corr):
                max_corr = a
                start_data = i
    
            # if start_data == -1 and -if_start <= a and a <= if_start:
            #     start_data = i
            arr.append(abs(a))
            ofdm_rx_2 = np.roll(ofdm_rx_2, -1)
        plt.figure(51, figsize = (10, 10))
        plt.subplot(2, 2, 1)
        plt.title("Correlation")
        plt.plot(arr)
        if(start_data == -1):
            print("[2] не удалось определить начало")
            EXIT()
        print("[2] Начало данных:", start_data)
    elif 3 == CON2:
        read_ofdms = np.array([])
        
        step = 0
        for index in range(ofdm_argv[1]):
            
            arr = []
            start_data = -1
            max_corr = -0.5
            ofdm_rx_2_iter = ofdm_rx_2[step:]
            for i in range(0, len(ofdm_rx_2_iter) - Nb):
                
                #a = np.vdot(data_read2[0:N_interval], data_read2[Nb:Nb + N_interval])
               
                a = sample.norm_corr(ofdm_rx_2_iter[0:N_interval], 
                                     ofdm_rx_2_iter[len_one_ofdm - N_interval: len_one_ofdm])
                #a = abs(a)
                #print("a = ", abs(a.real), abs(a.imag), end = " | ")
                
                if abs(a) > abs(max_corr):
                    max_corr = a
                    start_data = i
                arr.append(abs(a))
                ofdm_rx_2_iter = np.roll(ofdm_rx_2_iter, -1)
            plt.figure(51 + index, figsize = (10, 10))
            plt.subplot(2, 2, 1)
            plt.title("Correlation")
            plt.plot(arr)
            if(start_data == -1):
                print("[2] не удалось определить начало")
                EXIT()
            print("[2] Начало данных:", start_data)
            step += 0
            
    else:
        start_data = 0
    #start_data = 19
    #EXIT(1)
    data_rx = ofdm_rx_3[start_data:start_data + len_data_tx]
    plt.figure(52, figsize=(10, 10))
    plt.subplot(2, 2, 1)
    plt.title("data_rx")
    plt.scatter(ofdm_rx.real, ofdm_rx.imag)

    #EXIT()
    print("OFDM demodulator")
    data_decode = sample.OFDM_demodulator(data_rx, ofdm_argv[1:], Nb, N_interval, pilot, RS, Nz)
    resource_grid_3(data_rx, Nb, N_interval)
    print("len data_decode = ", len(data_decode))
    plt.figure(52, figsize=(10, 10))
    plt.subplot(2, 2, 2)
    plt.title("data")
    plt.scatter(data_decode.real, data_decode.imag)
    plt.subplot(2, 2, 3)
    plt.title("data, No FR")
    data_decode_nfr = sample.OFDM_demodulator_NO_FR(data_rx, ofdm_argv[1:], Nb, N_interval, pilot, RS, Nz)
    print("len data_decode_nfr = ", len(data_decode_nfr))
    plt.scatter(data_decode_nfr.real, data_decode_nfr.imag)
    EXIT()


