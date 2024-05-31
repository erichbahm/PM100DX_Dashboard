'''
Power_On_Lo_Word Accel Torque_Feedback Torque_Command DC_Voltage DC_Voltage Motor_Speed Flux_Weakening Motor_Voltage IQ_Command IQ_Feedback ID_Command ID_Feedback Modulation Module_Temp Motor_Temp Run_Lo Run_Hi Torque_Shudder Brake
'''

from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import pandas as pd
import numpy as np
from math import pi
import time


FILE = 'capture.txt'
W = True
plot = True
ROW = []
COLS = []
CONV = {}
LIM = 3

for i in range(20): COLS.append(i)
for i in range(20): CONV.update({i:lambda x: int(x, 16)})
fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2, 2)


class Index:
    def stop(self, event):
        plt.pause(100000)

def norm(arr, scale, neg=False):
    for i in range(arr.size):
        if arr[i] > 32766 / scale: arr[i] -= 65535 / scale
    if neg: return - arr
    else: return arr

if __name__ == '__main__':
    while plot:
        callback = Index()
        bstop = Button(ax4,'Stop')
        bstop.on_clicked(callback.stop)
        try:
            df = pd.read_csv(FILE, sep=' ', skiprows=LIM, usecols=COLS, converters=CONV, on_bad_lines='skip')
            na = df.to_numpy()
        except:
            plot = False
            print("CSV conversion Error")

        t = na[:, 0] /3         # ms, time elapsed
        accel = na[:, 1] / 100  # V, accel pot-input
        FT = na[:, 2] / 10      # Nm, torque feedback
        FT = norm(FT,10)
        CT = na[:, 3] / 10      # Nm, torque commanded
        dcv = na[:, 4] / 10     # V, DC Voltage
        dci = na[:, 5] / 10     # A, DC Current
        speed = na[:, 6]        # RPM, motor speed
        speed = norm(speed,1)
        aci = na[:, 7] / 10     # Apk, flux weakening output
        acv = na[:, 8] / 10     # Vpk, motor peak-peak voltage
        IQC = na[:, 9] / 10     # Apk, IQ commanded
        IQC = norm(IQC, 10)
        IQF = na[:, 10] / 10    # Apk, IQ feedback
        IQF = norm(IQF,10)
        IDC = na[:, 11] / 10    # Apk, ID commanded
        IDC = norm(IDC, 10)
        IDF = na[:, 12] / 10    # Apk, ID feedback
        IDF = norm(IDF, 10)
        mod = na[:, 13] / 10000 # Modulation
        Itemp = na[:, 14] / 10  # C, inverter temp
        Mtemp = na[:, 15] / 10  # C, motor temp
        Lfault = na[:, 16]      # run fault lo
        Hfault = na[:, 17]      # run fault hi
        shudd = na[:, 18] / 10  # Nm, torque shudder
        brake = na[:, 18] / 100 # V, brake pot-input
        x = np.linspace(0, speed.shape[0], na.shape[0])
        #dcp = dcv * dci
        #acp = acv * aci
        outp = abs(FT * speed * 2 * pi / 60)
        ICF = (IQF ** 2 + IDF ** 2) ** 0.5
        cfp = ICF * acv

        ax1.plot(x, speed, color='tab:blue', label='Speed (RPM)')
        ax1.plot(x, FT, color='tab:orange', label='Torque (Nm)')
        #ax2.plot(x, CT, color='tab:olive')
        ax2.plot(x, accel, color='tab:red', label='Accel Input (V)')
        ax3.plot(x, outp, color='tab:green', label='Output Power (W)')
        #ax4.plot(x, Itemp, color='tab:pink', label='Inverter Temp (C)')

        ax1.legend(loc="best")
        ax2.legend(loc="best")
        ax3.legend(loc="best")

        ax1.title.set_text('Speed: ' + str(speed[speed.size - 1]) + ' RPM')
        ax2.title.set_text('Accel: ' + str((accel[accel.size - 1])) + ' V')
        ax3.title.set_text('Input DCV: ' + str(dcv[dcv.size - 1]) + ' V')

        #ax1.set_ylabel('')
        #ax2.set_ylabel('')
        #ax3.set_ylabel('')

        if Hfault[Hfault.size-1]: print("FAULT")
        plt.pause(500)
