import numpy as np


#Строку символов в бинарный вид
def data_to_byte(data):
    bin_str = ''.join(format(ord(i), '08b') for i in data)
    return np.array(list(map(int, list(bin_str))))
def encode_QPSK(data, mode):
    ampl = 2**1
    if (len(data) % 2 != 0):
        print("QPSK:\nError, check data length", len(data))
        raise "error"
    else:
        sample = [] # массив комплексных чисел
        N = 2
        for i in range(0, len(data), N):
            b2i = data[i]
            b2i1 = data[i+1]
            real = (1 - N * b2i) / np.sqrt(N)
            imag = (1 - N * b2i1) / np.sqrt(N)
            sample.append(complex(real, imag))
        sample = np.asarray(sample)
        sample = sample * ampl
        return sample
def duplication_sample(data, N):
    dup_buff = []
    
    for i in data:
        for i2 in range(N):
            dup_buff.append(i)
    return dup_buff

def formula(value, k):
    return (k - 2 * value)    
def recurse_formula(arr_values, n, pos):
    if(len(arr_values) < 2):
        return 1
    return ( 2**n - (1 - 2 * arr_values[pos]) * recurse_formula(arr_values[2:], n-1, pos))


def calc_coeff(n):
    if(n < 1):
        return 2
    return 2 + 4 * calc_coeff(n-1)

def encode_QAM(data_bit, N):#[0, 1, 0, 1, ....], уровень QAM
    ampl = 2**14
    ad = int(np.log2(N))
    if (len(data_bit) % 2 != 0):
        print("QPSK:\nError, check bit_mass length", len(data_bit))
        raise "error"
        return
    sample = [] # массив комплексных чисел
    k1 = calc_coeff(int(np.log2(N))/2)
    print("k1 = ", k1)
    for i in range(0, len(data_bit), int(np.log2(N))):
        sr = data_bit[i:i+int(np.log2(N))]
        sr = list(reversed(sr))
        d1 = formula(sr[0], 1)
        d2 = recurse_formula(sr[2:], int(np.log2(N))/2, 0)
        d1i = formula(sr[1], 1)
        d2i = recurse_formula(sr[2:], int(np.log2(N))/2, 1)
        dd = (d1 * d2) /np.sqrt(k1) + ((d1i * d2i) / np.sqrt(k1)) * 1j
        sample.append(dd)
    return sample




