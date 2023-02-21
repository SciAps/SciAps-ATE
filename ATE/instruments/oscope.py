## imports ##
import pyvisa
# import easy_scpi as scpi

from time import sleep
from csv import writer

## oscope class ##
# class Oscope(scpi.Instrument):
class Oscope():
    def __init__(self, resource_id = None) -> None:
        # private vars
        self._resource_id = resource_id
        self._inst = None
        
        # public
        self.id = None
        self.probe_gain = 10

        # setup
        if self._resource_id:
            self.open()

        # self._inst = scpi.Instrument(
        #     port = resource,
        #     timeout = 5,
        #     read_termination = '\n',
        #     write_termination = '\n'
        # )

    ## instrument connection ##
    def open(self, resource_id: str = None) -> None:
        if resource_id:
            self._resource_id = resource_id

        self._inst = pyvisa.ResourceManager().open_resource(self._resource_id)
        self._inst.timeout = 5000

        id_keys = ['mfg', 'model', 'serial', 'version']
        id_vals = self.idn().replace('\n', '').split(',')

        self.id = dict(zip(id_keys, id_vals))
    
    def close(self) -> None:
        if self._inst:
            self._inst.close()

    ## high level control
    def reset(self) -> None:
        self._inst.write('*RST')
        self._inst.write('*CLS')
        self.stop()

    def timescale(self, t_range = 0.001, t_delay = 0) -> None:
        self._inst.write(':TIMEBASE:MODE MAIN', termination='\n')
        self._inst.write(f':TIMEBASE:RANGE {t_range:e}')
        self._inst.write(f':TIMEBASE:DELAY {t_delay:e}')

    def channel(self, chan_num: int = 1, v_range: float = 4, v_offset: float = 1.5) -> None:
        self._inst.write(f':CHANNEL{chan_num}:PROBE {self.probe_gain}')
        self._inst.write(f':CHANNEL{chan_num}:RANGE {v_range:e}')
        self._inst.write(f':CHANNEL{chan_num}:OFFSET {v_offset:e}')

    def trigger(self, v_level: float = 1.0) -> None:
        self._inst.write(':TRIGGER:SWEEP NORMAL')
        self._inst.write(f':TRIGGER:LEVEL {v_level}')
        self._inst.write(':TRIGGER:SLOPE POSITIVE')

    def acquisition(self) -> None:
        self._wr(':ACQUIRE:TYPE NORMAL')
        self._wr(':ACQUIRE:COMPLETE 100')
        self._wr(':DIGITIZE CHANNEL1')

    def screenshot(self, fname: str) -> None:
        self._wr(':DISPLAY:DATA? PNG, SCREEN, COLOR')
        dat = self._inst.read_raw()
        with open(fname, 'wb') as f:
            f.write(dat)

        # self._wr(':WAVEFORM:FORMAT ASCII')
        # print(self._wr(':HARDCOPY:PRINTER:LIST?'))

    # def label(self, lbls : [str]) -> None:
    #     for lbl in lbls:
    #         self._inst.write(f'{}\n')


    ## scpi commands ##
    # star commands
    def idn(self) -> str:
        return self._inst.query('*IDN?')

    # root commands



    def run(self) -> None:
        self._inst.write(':RUN')

    def single(self) -> None:
        self._inst.write(':SINGLE')

    def stop(self) -> None:
        self._inst.write('STOP')

    ## helpers ##
    def _wr(self, dat: str = '') -> None:
        self._inst.write(dat)

## demo ##
if __name__ == "__main__":
    rm = pyvisa.ResourceManager()               # open scope
    scope = Oscope(rm.list_resources()[0])
    scope.open()
    print(f"*IDN? {scope.id}")

    # scope.stop()
    # scope.reset()                               # reset
    # scope.clr
    scope.reset()
    # sleep(2)

    # scope.timebase.range(0.005)                 # settings for 1.2khz 2.5V square wave
    # scope.timebase.delay(0)
    # scope.stop()
    scope.timescale(0.005)

    # scope.channel1.probe(10)
    # scope.channel1.range(4)
    # scope.channel1.offset(1)
    scope.channel(1)

    # scope.trigger.sweep('NORMAL')
    # scope.trigger.level(1)
    # scope.trigger.slope('POSITIVE')
    scope.trigger(1.5)
    scope.acquisition()

    # scope.measure.clear                         # measurement settings
    # scope.measure.source('CHANNEL1')
    # scope.measure.frequency('CHANNEL1')
    # scope.measure.vamplitude('CHANNEL1')
    # scope.measure.dutycycle('CHANNEL1')
    # scope.measure.statistics(1)
    # scope.measure.counter
    # sleep(1)

    scope.run()                                 # start
    # sleep(1)

    # scope.measure.statistics.reset              # take measurements
    sleep(1)
    # print(scope.measure.results())
    scope.stop()
    scope.screenshot('scope.txt')

    # scope.write(':DIGITIZE')
    # scope.waveform.format('ASCII')              # save last capture to file
    # wave_ascii = scope.waveform.data().split(',')
    
    # wave_id, point_zero = wave_ascii[0].split(' ')
    # wave_ascii[0] = point_zero
    # wave_float = [float(point) for point in wave_ascii]
    # # print(wave_float)

    # with open('oscope.csv', newline='', mode='w') as f:
    #     fwriter = writer(f)
    #     for point in wave_float:
    #         fwriter.writerow([point])

    # scope.stop()                                # stop
    sleep(1)

    scope.close()                          # close