import pyvisa

from ATE.instruments.instrument import Instrument

from time import time, sleep

class Psu(Instrument):
    ## class vars ##
    CHANNELS = [1, 2]

    def __init__(self, resource_id) -> None:
        super().__init__(resource_id)
        self._channel = self.CHANNELS[0]

    def close(self) -> None:
        for i in range(1,4):
            self.output_disable(i)
        super().close()

    ## high level API ##
    # system


    def error(self):
        return self._qr('SYSTEM:ERROR?')

    # output settings
    @property
    def channel(self):
        return self._rd(':INSTRUMENT?')
    
    @channel.setter
    def channel(self, ch_val: int) -> None:
        self._wr(f':INSTRUMENT CH{ch_val}')
        self._channel = ch_val

    def voltage_limit_write(self, ch_val: int, v_setpoint: float) -> None:
        self._wr(f'CH{ch_val}:VOLTAGE {v_setpoint}')

    def voltage_limit_read(self, ch_val: int) -> float:
        return self._qr(f'CH{ch_val}:VOLTAGE?')

    def current_limit_write(self, ch_val: int, i_setpoint: float) -> None:
        self._wr(f'CH{ch_val}:CURRENT {i_setpoint}')

    def current_limit_read(self, ch_val: int) -> float:
        return self._qr(f'CH{ch_val}:CURRENT?')
    
    def measure_voltage(self, ch_val: int) -> float:
        return float(self._qr(f'MEASURE:VOLTAGE? CH{ch_val}'))
    
    def measure_current(self, ch_val: int) -> float:
        return float(self._qr(f'MEASURE:CURRENT? CH{ch_val}'))
    
    def measure_power(self, ch_val: int) -> float:
        return self._qr(f'MEASURE:POWER? CH{ch_val}')
    
    def output_enable(self, ch_val: int) -> None:
        self._wr(f'OUTPUT CH{ch_val},ON')

    def output_disable(self, ch_val: int) -> None:
        self._wr(f'OUTPUT CH{ch_val},OFF')

    # measurements

    # @property
    # def voltage_setpoint()
    
## demo ##
if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    # open connection
    psu = Psu(resources[0])
    print(f'Device ID: {psu.id}')

    # set voltage and current limits
    psu.voltage_limit_write(1, 5)
    print(f'Channel 1 Voltage Limit = {psu.voltage_limit_read(1)}')

    psu.current_limit_write(1, 1.5)
    print(f'Channel 1 Current Limit = {psu.current_limit_read(1)}')

    # enable outputs
    psu.output_enable(1)
    print('Enabling output and starting log.  Press Ctrl+C to stop.')
    # sleep(0.1)
    t0 = time()

    # datalog loop
    # for i in range(10):
    while True:
        try:
            t_samp = time() - t0
            v_meas = psu.measure_voltage(1)
            i_meas = psu.measure_current(1)
            print(f't={t_samp:.3f}: v={v_meas} i={i_meas}')
            sleep(0.1)
        except KeyboardInterrupt:
            print('stopping log')
            break

    print('disabling output')
    psu.close()
