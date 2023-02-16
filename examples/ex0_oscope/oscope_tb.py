## imports ##
import pyvisa

## setup ##
# find attached instruments
rm = pyvisa.ResourceManager()
print(f"visa resources: {rm.list_resources()}")
oscope_path = rm.list_resources()[0]

# open connection to scope
oscope = rm.open_resource(oscope_path)
print(f"*IDN? - {oscope.query('*IDN?')}")

# scope settings
oscope.write('*CLR')
oscope.write('*RST')
oscope.write(':STOP')

oscope.write(':TIMEBASE:RANGE +5.000E-03')
oscope.write(':TIMEBASE:DELAY 0')

oscope.write(':CHANNEL1:PROBE 10')
oscope.write(':CHANNEL1:RANGE 4')
oscope.write(':CHANNEL1:OFFSET 1')

oscope.write(':TRIGGER:SWEEP NORMAL')
oscope.write(':TRIGGER:LEVEL 1')
oscope.write(':TRIGGER:SLOPE POSITIVE')

oscope.write(':RUN')


## test ##


## teardown ##
oscope.close()