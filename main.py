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
ROW = []
COLS = [1,3,4,5,6,9,10,17]
fig, ([ax1, ax2, ax3], [ax4, ax5, ax6]) = plt.subplots(2, 3)
LIM = 3
plot = True

class Index:
    def stop(self, event):
        plt.pause(100000)

if __name__ == '__main__':
    while plot:
        callback = Index()
        bstop = Button(ax6,'Stop')
        bstop.on_clicked(callback.stop)
        try:
            df = pd.read_csv(FILE,sep=' ',skiprows=LIM,usecols=COLS,on_bad_lines ='skip',converters={6:lambda x: int(x, 16),1:lambda x: int(x, 16),3:lambda x: int(x, 16),5:lambda x: int(x, 16),4:lambda x: int(x, 16),10:lambda x: int(x, 16),9:lambda x: int(x, 16),17:lambda x: int(x, 16)})
            na = df.to_numpy()
        except:
            continue
        # 1: Accel Input
        # 3: Torque command
        # 4: DC voltage
        # 5: DC current
        # 6: Motor speed
        # 9: IQ Command
        # 10: IQ Feedback
        # 17: Fault
        accel = na[:, [0]] / 100
        torque = na[:, [1]] / 10
        dcv = na[:, [2]] / 10
        dci = na[:,3] / 10
        speed = na[:, [4]]
        for i in range(speed.size):
            if speed[i] > 32766:
                speed[i] -= 65535
        IQC = na[:, [5]] / 10
        IQF = na[:, [6]] / 10
        fault = na[:, [7]]
        x = np.linspace(0, speed.size, speed.size)

        ax1.plot(x, speed, color='tab:blue')
        ax2.plot(x, dcv, color='tab:green')
        ax2.plot(x, dci, color='tab:green')
        ax2.plot(x, torque, color='tab:red')
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

        if fault[fault.size-1][0]: print("FAULT")

        plt.pause(0.25)
