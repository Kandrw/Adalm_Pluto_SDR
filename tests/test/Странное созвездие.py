# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 21:19:15 2024

@author: Andrey
"""

import numpy as np
import matplotlib.pyplot as plt

# Параметры QAM модуляции
M = 40  # Количество точек в созвездии
symbol_length = 100  # Длина символа

# Создание созвездия QAM
constellation = np.array([np.exp(1j * np.pi / 10 * (2*k + 1)) for k in range(M)])

# Генерация случайной последовательности символов
symbols = np.random.choice(constellation, symbol_length)

# Визуализация созвездия QAM
plt.scatter(constellation.real, constellation.imag, label='Созвездие QAM')
plt.scatter(symbols.real, symbols.imag, label='Сгенерированные символы', color='orange')
plt.xlabel('I (Inphase)')
plt.ylabel('Q (Quadrature)')
plt.title('Созвездие QAM')
plt.legend()
plt.grid(True)
plt.show()
