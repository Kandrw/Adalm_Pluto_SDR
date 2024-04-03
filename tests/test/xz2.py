# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 21:44:10 2024

@author: Andrey
"""

import numpy as np
import matplotlib.pyplot as plt
def generate_qam_signal(binary_sequence, M, fc, T, p_t):
    symbol_sequence = np.zeros(int(len(binary_sequence)//np.log2(M)), dtype=complex)
    
    for i in range(0, len(binary_sequence), int(np.log2(M))):
        symbol_index = int(binary_sequence[i:i+int(np.log2(M))], 2)
        symbol = 2 * symbol_index/(M-1) - 1
        symbol_sequence[int(i//np.log2(M))] = symbol

    t = np.linspace(0, T, len(symbol_sequence))
    qam_signal = np.zeros(len(t))
    
    for i, symbol in enumerate(symbol_sequence):
        qam_signal += np.sqrt(2/T) * (symbol.real * np.cos(2*np.pi*fc*t) - symbol.imag * np.sin(2*np.pi*fc*t)) * p_t[i]
    
    return qam_signal

# Пример использования
M = 16  # Количество уровней
fc = 1000  # Несущая частота
T = 1/1000  # Период символа
p_t = np.ones(1000)  # Пример импульсной формы

binary_sequence = "101010100101111011010101010100111111001011011110100110100010100110101010"  # Бинарная последовательность
qam_signal = generate_qam_signal(binary_sequence, M, fc, T, p_t)

print(qam_signal)
plt.scatter(qam_signal.real, qam_signal.imag)
plt.figure()
plt.plot(qam_signal)