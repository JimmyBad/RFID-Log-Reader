import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from scipy.interpolate import interp1d
import csv
import os

# Config
EPC_number = 1555
time_limit = 40
linear_index = 8
cubic_index = 100

# Initialization
filenames = []

filter_name = '.csv'
for file in os.listdir('.'):
    if file[len(file)-len(filter_name):len(file)]==filter_name:
        filenames.append(file)

filenames = sorted(filenames)
colors = cm.rainbow(np.linspace(0, 1, len(filenames)))
color_slot = 0

for file in filenames:
    RSSI = []
    time = []
    power = 0
    initial_time = 0
    with open(file,'r') as csvfile:
        line = csv.reader(csvfile, delimiter = ',')
        next(line)
        for row in line:
            EPC_check = row[1][len(row[1])-len(str(EPC_number)):len(row[1])]
            if initial_time==0 and EPC_check==str(EPC_number):
                initial_time = float(row[0][17:27])
            if EPC_check==str(EPC_number):
                current_time = float(row[0][17:27])
                if current_time>=initial_time:
                    delta_t = current_time-initial_time
                if current_time<initial_time:
                    delta_t = current_time-initial_time+60
                if delta_t<=time_limit:
                    time.append(delta_t)
                    RSSI.append(float(row[4]))
                else:
                    break
            if row[5][:len(' Power')]==' Power' and power==0:
                power = row[5][len(row[5])-2:len(row[5])]
        
        x1 = np.linspace(.1, time_limit-.5, linear_index)
        y_f1 = interp1d(time, RSSI, kind='linear')
        x2 = np.linspace(.1, time_limit-.5, cubic_index)
        y_f2 = interp1d(x1, y_f1(x1), kind='cubic')
        plt.plot(time, RSSI, linestyle = '-', color=colors[color_slot], alpha=0.05)
        plt.plot(x2, y_f2(x2), linestyle = '-',label=str(power)+' Dbm', color=colors[color_slot])
        color_slot += 1

plt.grid()
plt.xlabel('Time')
plt.ylabel('RSSI')
plt.xlim(0, time_limit)
plt.title('RSSI vs. Time', fontsize = 20)
plt.legend(loc='lower left', fancybox=True, shadow=True, fontsize = 7)
plt.twiny()
plt.xticks(np.linspace(0, 360, 9))
plt.xlabel("Angle")
plt.show()