import modules
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
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

        # slider axes (vertical, on the left; horizontal under the plot)
        plt.subplots_adjust(left=0.30, bottom=0.20)
        self.ax_ylim_min = plt.axes([0.05, 0.15, 0.03, 0.65])
        self.ax_ylim_max = plt.axes([0.15, 0.15, 0.03, 0.65])
        self.ax_xlim_max = plt.axes([0.35, 0.05, 0.55, 0.03])

        self.slider_ylim_min = Slider(self.ax_ylim_min, 'Y min',
                                      valmin=-self.ref_voltage, valmax=self.ref_voltage,
                                      valinit=-self.ref_voltage,
                                      orientation='vertical')
        self.slider_ylim_max = Slider(self.ax_ylim_max, 'Y max',
                                      valmin=-self.ref_voltage, valmax=self.ref_voltage,
                                      valinit=self.ref_voltage,
                                      orientation='vertical')
        self.slider_xlim_max = Slider(self.ax_xlim_max, 'X max',
                                      valmin=0, valmax=self.time_scale,
                                      valinit=self.time_scale)

    def init_plot(self):
        """
        Initialize the plot
        """

        self.ax.set_ylim(self.slider_ylim_min.val, self.slider_ylim_max.val)
        self.ax.set_xlim(0, self.slider_xlim_max.val)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.set_title('Real-time Data from Serial Port')
        self.ax.grid()
        self.ax.legend()

        # Connect sliders to update lim
        self.slider_ylim_min.on_changed(self.update_ylim)
        self.slider_ylim_max.on_changed(self.update_ylim)
        self.slider_xlim_max.on_changed(self.update_xlim)

        return self.line1, self.line2

    def update_ylim(self, val):
        """
        Update the Y limits of the plot based on slider values.
        Prevents the minimum Y limit from being greater than or equal to the maximum Y limit.
        """

        min_ylim = self.slider_ylim_min.val
        max_ylim = self.slider_ylim_max.val

        # prevent min >= max
        if min_ylim >= max_ylim:
            max_ylim = min_ylim + 0.01
            self.slider_ylim_max.set_val(max_ylim)
        self.ax.set_ylim(min_ylim, max_ylim)
        self.fig.canvas.draw_idle()

    def update_xlim(self, val):
        """
        Update the X limits of the plot based on the slider value.
        """

        max_xlim = self.slider_xlim_max.val
        self.ax.set_xlim(0, max_xlim)
        self.fig.canvas.draw_idle()

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

        # Limit the number of points to the maximum defined
        if len(self.data1) > self.max_points:
            self.data1.pop(0)
            self.data2.pop(0)
            self.time_list.pop(0)

        # Adapt the time list to start from 0
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
                            frames_amount=200,
                            resolution=65535,
                            ref_voltage=3.3)
    plotter.run()
