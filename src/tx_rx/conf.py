


class RxTx:
    #sdr_con = False
    sdr = None
    #__sdr = 23
    #__rx_lo = 1
    #__tx_lo = 1
    buffer = None
    
    def __init__(self, sdr = None, rx_lo = 2e9, tx_lo = 2e9, sample_rate = 1e6):
        #sdr_con = sdr
        
        self.sdr = sdr
        if(not sdr is None):
            self.sdr.rx_lo = rx_lo
            self.sdr.tx_lo = tx_lo
            self.sdr.sample_rate = sample_rate
        else:
            self.rx_lo = rx_lo
            self.tx_lo = tx_lo
            self.sample_rate = sample_rate
        print("INIIT module RXTX")
    def set_sdr(self, sdr):
        self.sdr = sdr

    def recv(self):
        if(not self.sdr is None):
            return sdr.rx()
        else:
            self.generate_noise()
            return self.buffer

    def send(self, msg):
        if(not self.sdr is None):
            return sdr.tx(msg)
        else:
            self.buffer = msg
    
    def generate_noise(self):
        if(not self.buffer is None):
            print("NOISE")
    def set_tx_cyclic_buffer(self, con):
        self.sdr.tx_cyclic_buffer = con

    def print_test(self):
        print("Test")

    def print_parameters(self):
        if(self.sdr is None):
            print("sample rate:", self.sample_rate)
            print("tx_lo:", self.tx_lo)
            print("rx_lo:", self.rx_lo)
            


def print_test1():
        print("Test")


















