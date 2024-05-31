'''
Power_On_Lo_Word Accel Torque_Feedback Torque_Command DC_Voltage DC_Voltage Motor_Speed Flux_Weakening Motor_Voltage IQ_Command IQ_Feedback ID_Command ID_Feedback Modulation Module_Temp Motor_Temp Run_Lo Run_Hi Torque_Shudder Brake
'''

from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import pandas as pd
import numpy as np
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
fig, ([ax1, ax2, ax3], [ax4, ax5, ax6]) = plt.subplots(2, 3)


class Index:
    def stop(self, event):
        plt.pause(100000)

if __name__ == '__main__':
    while plot:
        callback = Index()
        bstop = Button(ax6,'Stop')
        bstop.on_clicked(callback.stop)
        try:
            df = pd.read_csv(FILE, sep=' ', skiprows=LIM, usecols=COLS, converters=CONV, on_bad_lines='skip')
            na = df.to_numpy()
        except:
            plot = False
            print("CSV conversion Error")

        t = na[:, [0]] /3          # ms, time elapsed
        accel = na[:, [1]] / 100   # V, accel pot-input
        FT = na[:, [2]] / 10       # Nm, torque feedback
        for i in range(FT.size):
            if FT[i] > 3276.6: FT[i] -= 6553.5
        CT = na[:, [3]] / 10       # Nm, torque commanded
        dcv = na[:, [4]] / 10      # V, DC Voltage
        dci = na[:,5] / 10         # A, DC Current
        speed = na[:, [6]]         # RPM, motor speed
        for i in range(speed.size):
            if speed[i] > 32766: speed[i] -= 65535
        aci = na[:, [7]] / 10     # Apk, flux weakening output
        acv = na[:, [8]] / 10     # Vpk, motor peak-peak voltage
        IQC = na[:, [9]] / 10     # Apk, IQ commanded
        IQF = na[:, [10]] / 10    # Apk, IQ feedback
        IDC = na[:, [11]] / 10    # Apk, ID commanded
        IDF = na[:, [12]] / 10    # Apk, ID feedback
        mod = na[:, [13]] / 10000 # Modulation
        Itemp = na[:, [14]] / 10  # C, inverter temp
        Mtemp = na[:, [15]] / 10  # C, motor temp
        Lfault = na[:, [16]]      # run fault lo
        Hfault = na[:, [17]]      # run fault hi
        shudd = na[:, [18]] / 10  # Nm, torque shudder
        brake = na[:, [18]] / 100 # V, brake pot-input
        x = np.linspace(0, speed.shape[0], na.shape[0])

        ax1.plot(x, speed, color='tab:blue')
        ax2.plot(x, dcv, color='tab:green')
        ax2.plot(x, dci, color='tab:green')
        ax3.plot(x, FT, color='tab:red')
        ax3.plot(x, accel, color='tab:orange')
        #ax5.plot(x, IQC, color='tab:red')
        #ax4.plot(x, IQF, color='tab:pink')

        #ax1.set_ylim(,)
        ax1.title.set_text('Speed: ' + str(speed[speed.size - 1][0]) + ' RPM')
        ax2.title.set_text('Voltage: ' + str(dcv[dcv.size - 1][0]) + ' V')
        ax3.title.set_text('Accel: ' + str((accel[accel.size - 1][0])) + ' V')

        ax1.set_ylabel('Speed (RPM)')
        ax2.set_ylabel('Busbar')
        ax3.set_ylabel('Acceleration input (V)')
        #ax5.set_ylabel('IQ (Apk)')

        if Hfault[Hfault.size-1][0]: print("FAULT")
        plt.pause(500)
