## imports ##
import pyvisa
import easy_scpi as scpi

from time import sleep
from csv import writer

## oscope class ##
class Oscope(scpi.Instrument):
    def __init__(self, port = None) -> None:
        super().__init__(
            port = port,
            timeout = 5,
            read_termination = '\n',
            write_termination = '\n'
        )

    # api
    def run(self) -> None:
        self.write(':RUN')

    def single(self) -> None:
        self.write(':SINGLE')

    def stop(self) -> None:
        self.write(':STOP')

## demo ##
if __name__ == "__main__":
    rm = pyvisa.ResourceManager()               # open scope
    scope = Oscope(rm.list_resources()[0])
    scope.connect()
    print(f"*IDN? {scope.id}")

    scope.stop()
    scope.reset()                               # reset
    scope.clr
    sleep(1)

    scope.timebase.range(0.005)                 # settings for 1.2khz 2.5V square wave
    scope.timebase.delay(0)

    scope.channel1.probe(10)
    scope.channel1.range(4)
    scope.channel1.offset(1)

    scope.trigger.sweep('NORMAL')
    scope.trigger.level(1)
    scope.trigger.slope('POSITIVE')

    scope.measure.clear                         # measurement settings
    scope.measure.source('CHANNEL1')
    scope.measure.frequency('CHANNEL1')
    scope.measure.vamplitude('CHANNEL1')
    scope.measure.dutycycle('CHANNEL1')
    scope.measure.statistics(1)
    scope.measure.counter
    sleep(1)

    scope.run()                                 # start
    sleep(1)

    scope.measure.statistics.reset              # take measurements
    sleep(3)
    print(scope.measure.results())

    scope.write(':DIGITIZE')
    scope.waveform.format('ASCII')              # save last capture to file
    wave_ascii = scope.waveform.data().split(',')
    
    wave_id, point_zero = wave_ascii[0].split(' ')
    wave_ascii[0] = point_zero
    wave_float = [float(point) for point in wave_ascii]
    # print(wave_float)

    with open('oscope.csv', newline='', mode='w') as f:
        fwriter = writer(f)
        for point in wave_float:
            fwriter.writerow([point])

    scope.stop()                                # stop
    sleep(1)

    scope.disconnect()                          # close