# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 21:26:19 2024

@author: Andrey
"""

import numpy as np
import matplotlib.pyplot as plt
N = 4







def formula1(value, k):
    print("\nk =", k, "v =",(k - 2 * value), "val =", value)
    return (k - 2 * value)    
def recurse_formula1(arr_values, n, len_arr):
    if(n >= len_arr/2 ):
        return 1;
    print(n, "arr:",arr_values, len(arr_values), "val =",formula1(data[1], 2**n))
    return formula1(data[1], 2**n) * recurse_formula1(arr_values[2:], n+1, len_arr)
    pass



def formula(value, k):
    #print("\nk =", k, "v =",(k - 2 * value), "val =", value)
    return (k - 2 * value)    
def recurse_formula(arr_values, n, pos):
    if(len(arr_values) < 2):
        return 1
    #if(n >= len_arr/2 ):
    #    return 1;
    #print(n, "arr:",arr_values, len(arr_values), "val =",formula(data[1], 2**n))
    #return formula(data[1], 2**n) * recurse_formula(arr_values[2:], n+1, len_arr)
    #if(n == 0):
        #return (1 - 2 * arr_values[1]) * (2 - (1 - ))
    #return 2**n - ( 1 - () * )
    #print("pos = ", pos)
    return ( 2**n - (1 - 2 * arr_values[pos]) * recurse_formula(arr_values[2:], n-1, pos))
    pass

data = np.random.randint(0, 2, 1000000)
#data = [1 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,1 ,0 ,1 ,0, 1 ,0 ,0 ,1 ,0 ,1 ,0, 1 ,0 ,0 ,1 ,0 ,1 ,0]
data = [
        0,0,0,0,
        0,0,0,1,
        0,0,1,0,
        0,0,1,1,
        0,1,0,0,
        0,1,0,1,
        0,1,1,0,
        0,1,1,1,
        1,0,0,0,
        1,0,0,1,
        1,0,1,0,
        1,0,1,1,
        1,1,0,0,
        1,1,0,1,
        1,1,1,0,
        1,1,1,1
        ]

for i in range(0, len(data), N):
    d = data[i:i + N]
def convert_string_to_array(binary_string):
    # Используем генератор списков для конвертации символов в целые числа 
    binary_array = [int(bit) for bit in binary_string if bit in ['0', '1']]
    return binary_array
def generate_data(N, L):
    array = np.arange(0, N)

    # Преобразуем каждое значение в двоичную форму, которая занимает не более 6 бит
    binary_array = np.array([np.binary_repr(x, width=L) for x in array])
    data = []
    for i in binary_array:
        #data.append(convert_string_to_array(i))
        data += convert_string_to_array(i)
        
    return data
def calc_coeff(n):
    if(n < 1):
        return 2
    return 2 + 4 * calc_coeff(n-1)

def MULTI_QAM(data_bit, N):#[0, 1, 0, 1]
    ampl = 2**14
    ad = int(np.log2(N))
    if (len(data_bit) % 2 != 0):
        print("QPSK:\nError, check bit_mass length", len(data_bit))
        raise "error"
        return
    sample = [] # массив комплексных чисел
    k1 = calc_coeff(int(np.log2(N))/2)
    print(k1)
    for i in range(0, len(data_bit), int(np.log2(N))):
        #print("i = ", i)
        #b2i = data_bit[i]
        #b2i1 = data_bit[i+1]
        sr = data_bit[i:i+int(np.log2(N))]
        sr = list(reversed(sr))
        #print("res =",recurse_formula(sr, 0, len(sr)) / np.sqrt(42))
        
        d1 = formula(sr[0], 1)
        d2 = recurse_formula(sr[2:], int(np.log2(N))/2, 0)
        
        d1i = formula(sr[1], 1)
        d2i = recurse_formula(sr[2:], int(np.log2(N))/2, 1)
        dd = (d1 * d2) /np.sqrt(k1) + ((d1i * d2i) / np.sqrt(k1)) * 1j
        #dd /=np.sqrt(42)
        #print("res =",recurse_formula(sr, 0, len(sr)) / np.sqrt(42))
        sample.append(dd)
        #print(sr)
        #real = (1 - 2 * b2i) / np.sqrt(2)
        #imag = (1 - 2 * b2i1) / np.sqrt(2)
        #sample.append(complex(real, imag))
    #sample = np.asarray(sample)
    #sample = sample * ampl
    return sample

N = 64
fd = int(np.log2(N))
data = generate_data(N, 8)
DDD = MULTI_QAM(data, N)
for i in data:
    #print(i, end = " ")
    pass
DDD = np.array(DDD)
plt.figure(1, figsize=(10,10))
plt.scatter(DDD.real, DDD.imag)

