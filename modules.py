import serial


def retrieve_data(port='/dev/ttyACM0', baud=9600) -> tuple [int,int]:
    """
    Retrieve data from the specified serial port, returning the two integers received.
    
    port: Serial port to connect to (e.g., '/dev/ttyACM0').
    baud: Baud rate for the serial connection.
    """

    try :
        ser = serial.Serial(port, baudrate=baud, timeout=1)
        line = ser.readline().decode('utf-8').strip()
        retrieve_data = line.split(';')

        return int(retrieve_data[0]), int(retrieve_data[1])

    except :
        print('Error while retrieving data from the serial port.')
        return 0, 0