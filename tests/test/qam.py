# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 00:34:43 2024

@author: Andrey
"""

import numpy as np


def convert_string_to_array(binary_string):
    # Используем генератор списков для конвертации символов в целые числа 
    binary_array = [int(bit) for bit in binary_string if bit in ['0', '1']]
    return binary_array

def generate_data(N, L):
    array = np.arange(1, N)

    # Преобразуем каждое значение в двоичную форму, которая занимает не более 6 бит
    binary_array = np.array([np.binary_repr(x, width=L) for x in array])
    data = []
    for i in binary_array:
        #data.append(convert_string_to_array(i))
        data += convert_string_to_array(i)
        
    return data


data = generate_data(64, 6)

# Создаем массив значений от 1 до 64
#array = np.arange(1, 64)

# Преобразуем каждое значение в двоичную форму, которая занимает не более 6 бит
#binary_array = np.array([np.binary_repr(x, width=6) for x in array])

#print(binary_array)
