## imports ##
from ATE.instruments.oscope import Oscope
from pyvisa import ResourceManager

import matplotlib.pyplot as plt
import numpy as np

import argparse
from time import time, strftime, gmtime
import csv

def main():
    # command line args
    parser = argparse.ArgumentParser(
        prog='python -m scopeshot',
        description='''
        Utility script for taking screenshots and reading out data from an oscilloscope.
        ''')
    parser.add_argument('-n', '--filename', type=str, required=False, default=None)
    parser.add_argument('-f', '--format', type=str, required=False, default='png')
    args=parser.parse_args()

    format = args.format

    if args.filename:
        fname = args.filename
    else:
        t0 = time()
        fname = f'scope_{strftime("%m-%d-%y_%H-%M-%S", gmtime(t0))}'
    fname += '.' + format


    # open instrument
    rm = ResourceManager()
    scope = Oscope(rm.list_resources()[0])
    scope.open()
    print(f"*IDN? {scope.id}")

    # capture data
    if args.format.lower() == 'png':
        scope.screenshot(fname)
    elif args.format.lower() == 'csv':
        preamble = scope.read_preamble()
        y_vals = scope.read_data()

        x_vals = np.arange(0, 1000*preamble['xincrement'], preamble['xincrement'])[:1000]
        x_vals = x_vals + preamble['xorigin']
        x_vals *= 1000

        with open(fname, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time (ms)', 'Voltage (V)'])

            for row in list(zip(x_vals, y_vals)):
                writer.writerow(row)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_xlabel('time (ms)')
        ax.set_ylabel('Volts (V)')
        plt.show()

    scope.close()

    # show result
    

if __name__ == "__main__":
    main()