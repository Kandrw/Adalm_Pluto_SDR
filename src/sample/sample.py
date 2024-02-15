import numpy as np


#Строку символов в бинарный вид
def data_to_byte(data):
    #print("[data_to_byte]")
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




