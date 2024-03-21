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


def OFDM_modulator(data, Nb, N_interval, symbol_ofdm):
    data = np.array(data)
    ofdm_data = []
    #step = 
    print("len input = ", len(data))
    count_ofdm = 0
    for i in range(0, len(data), Nb):
        arr = data[i : i + Nb]
        if(len(arr) < Nb):
            #pass#arr = arr + 
            print("Добивание:", Nb - len(arr))
            arr = np.concatenate([arr, np.zeros(Nb - len(arr))])
            
        
        
        ofdm = np.fft.ifft(arr)
        ofdm = np.concatenate([ofdm[len(ofdm) - N_interval:], ofdm])
        #ofdm = np.concatenate([ofdm, np.zeros(Nb - len(arr))])
        #print(ofdm_data)
        #print("i = ", i, "len= ", len(arr))
        ofdm_data = np.concatenate([ofdm_data, ofdm]) 
        count_ofdm += 1
    print("Count ofdm:", count_ofdm)
    print("len out = ", len(ofdm_data))
    return ofdm_data
    
def norm_corr1(x, y):
    x_norm = (x - np.mean(x)) / np.std(x)
    y_norm = (y - np.mean(y)) / np.std(y)
    corrR = np.vdot(x_norm.real, y_norm.real) / (np.linalg.norm(x_norm.real) * np.linalg.norm(y_norm.real))
    corrI = np.vdot(x_norm.imag, y_norm.imag) / (np.linalg.norm(x_norm.imag) * np.linalg.norm(y_norm.imag))
    
    return max(corrR, corrI)    
def norm_corr(x,y):
    #x_normalized = (cp1 - np.mean(cp1)) / np.std(cp1)
    #y_normalized = (cp2 - np.mean(cp2)) / np.std(cp2)

    c_real = np.vdot(x.real, y.real) / (np.linalg.norm(x.real) * np.linalg.norm(y.real))
    c_imag = np.vdot(x.imag, y.imag) / (np.linalg.norm(x.imag) * np.linalg.norm(y.imag))
    
    return c_real+1j*c_imag


def correlat_ofdm(rx_ofdm, cp,num_carrier):
    max = 0
    rx1 = rx_ofdm
    cor = []
    cor_max = []
    for j in range(len(rx1)):
        corr_sum =abs(norm_corr(rx1[:cp],np.conjugate(rx1[num_carrier:num_carrier+cp])))
        #print(corr_sum)
        cor.append(corr_sum)
        if corr_sum > max and (corr_sum.imag > 0.9 or corr_sum.real > 0.9):
            cor_max.append(corr_sum)
            max = corr_sum
            #print(np.round(max))
            index = j
        rx1= np.roll(rx1,-1)

    cor  = np.asarray(cor)
    #ic(cor_max)
    #plt.figure(3)
    #plt.plot(cor.real)
    #plt.plot(cor.imag)
    #print("ind",index)
    #return (index - (cp+num_carrier))
    return index

def del_prefix_while(data, Nb, N_interval):
    out_data = np.array([])
    print("Длинна входных данных",len(data))
    for i in range(N_interval, len(data), Nb):
        #print(i)
        #out_data += data[i:i + Nb]
        out_data = np.concatenate([out_data, data[i:i + Nb]])
        
    return out_data
