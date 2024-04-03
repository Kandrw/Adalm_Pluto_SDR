# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 00:37:02 2024

@author: Andrey
"""

def convert_string_to_array(binary_string):
    # Используем генератор списков для конвертации символов в целые числа 
    binary_array = [int(bit) for bit in binary_string if bit in ['0', '1']]
    return binary_array

# Пример использования функции
binary_string = '0101010011'
binary_array = convert_string_to_array(binary_string)
print(binary_array)
