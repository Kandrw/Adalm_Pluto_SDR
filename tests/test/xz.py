# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 00:01:18 2024

@author: Andrey
"""



import numpy as np
import matplotlib.pyplot as plt

# Заданные значения амплитуд и фаз для каждого уровня QAM
A = np.array([1, 1, 1, 1])
theta = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4])

# Символьный поток (прямоугольные импульсы)
Ts = 1  # период символа
p = np.array([1, 1, 0, 0])  # для примера возьмем 4 символа

# Несущая частота и время
fc = 1e9  # 1 ГГц
t = np.linspace(0, 10e-6, 1000)  # от 0 до 10 мкс с шагом 10 нс
s = np.zeros(len(t))

# Расчет модулированного сигнала
for m in range(4):
    s += A[m] * np.cos(2*np.pi*fc*t + theta[m]) * np.roll(np.tile(p, len(t)//4), m*len(t)//4)

# Построение графика модулированного сигнала
plt.plot(t, s)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Modulated Signal for 16-QAM')
plt.grid(True)

plt.figure(2)

plt.scatter(s.real, s.imag)

plt.show()
