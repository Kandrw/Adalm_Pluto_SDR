import numpy as np


#Строку символов в бинарный вид
def data_to_byte(data):
	#print("[data_to_byte]")
	bin_str = ''.join(format(ord(i), '08b') for i in data)
	return np.array(list(map(int, list(bin_str))))

	













