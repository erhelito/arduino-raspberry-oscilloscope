import modules
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class SerialPlotter:
    def __init__(self, serial_port='/dev/ttyACM0', baudrate=9600, time_scale=2, frames_amount=200, resolution=65535, ref_voltage=3.3):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.time_scale = time_scale
        self.frames_amount = frames_amount
        self.resolution = resolution
        self.ref_voltage = ref_voltage
        
        # internal variables
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        self.data1 = []
        self.data2 = []
        self.time_list = []
        self.max_points = self.frames_amount

        # init plots variables
        self.fig, self.ax = plt.subplots()
        self.line1, = self.ax.plot([], [], label='Channel 1')
        self.line2, = self.ax.plot([], [], label='Channel 2')

    def init_plot(self):
        """
        Initialize the plot
        """

        self.ax.set_ylim(0, 3.3)
        self.ax.set_xlim(0, self.time_scale)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.set_title('Real-time Data from Serial Port')
        self.ax.grid()
        self.ax.legend()

        return self.line1, self.line2

    def update_plot(self, frame):
        """
        Update the plot with new data from the serial port.
        This function is called at each frame of the animation.
        """
        d1, d2 = modules.retrieve_data(self.ser)
        d1, d2 = modules.convert_to_voltage(d1, d2)
        
        current_time = time.time() # Get the current time

        self.time_list.append(current_time)
        self.data1.append(d1)
        self.data2.append(d2)

        if len(self.data1) > self.max_points:
            self.data1.pop(0)
            self.data2.pop(0)
            self.time_list.pop(0)

        time_list_adapted = [t - self.time_list[0] for t in self.time_list]

        self.line1.set_data(time_list_adapted, self.data1)
        self.line2.set_data(time_list_adapted, self.data2)

        return self.line1, self.line2

    def run(self):
        """
        Start the animation of the plot.
        """
        anim_interval = self.time_scale * 1000 / self.frames_amount

        ani = animation.FuncAnimation(self.fig,
                                      self.update_plot,
                                      interval=anim_interval,
                                      init_func=self.init_plot,
                                      frames=self.frames_amount,
                                      blit=True)
        plt.show()


if __name__ == "__main__":
    plotter = SerialPlotter(serial_port='/dev/ttyACM0',
                            baudrate=9600,
                            time_scale=2,
                            frames_amount=200)
    plotter.run()
