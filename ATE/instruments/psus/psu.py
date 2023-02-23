import pyvisa

from ATE.instruments.instrument import Instrument

class Psu(Instrument):
    ## class vars ##

    ## high level API ##
    def channel_select(self, ch: int = 1):
        self._wr(f'CH{ch}')

    def measure_v(self, ch: int = None):
        msg = ':MEASURE:VOLTAGE?'
        msg += f' CH{ch}'
        return self._qr(msg)
    
## demo ##
if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    psu = Psu(resources[0])

    print(psu.id)

    psu.close()
