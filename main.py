from modules import *
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

### Configuration ###
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600

time_scale = 2 # Time scale for the x-axis in seconds
frames_amount = 200  # Number of frames to display
anim_delay = time_scale * 1000 / frames_amount  # Animation update interval in milliseconds

resolution = 65535  # ADC resolution for a 16-bit ADC
ref_voltage = 3.3  # Reference voltage for the ADC


ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

data1 = []
data2 = []
time_list = []
max_points = frames_amount

fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Channel 1')
line2, = ax.plot([], [], label='Channel 2')

def init():
    ax.set_ylim(0, 3.3)
    ax.set_xlim(0, time_scale)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Real-time Data from Serial Port')
    ax.grid()
    ax.legend()

    return line1, line2

def update(frame):
    d1,d2 = retrieve_data(ser)

    d1,d2 = convert_to_voltage(d1, d2, vref=ref_voltage, adc_resolution=resolution)
    
    current_time = time.time()
    time_list.append(current_time)
    data1.append(d1)
    data2.append(d2)

    if len(data1) > max_points :
        data1.pop(0)
        data2.pop(0)
        time_list.pop(0)
    
    time_list_adapted = [t-time_list[0] for t in time_list]

    print(time_list_adapted)
    line1.set_data(time_list_adapted, data1)
    line2.set_data(time_list_adapted, data2)

    return line1, line2

ani = animation.FuncAnimation(fig, update, interval=anim_delay, init_func=init, frames=frames_amount, blit=True)

plt.show()