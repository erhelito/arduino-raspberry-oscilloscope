import serial

def retrieve_data(ser) -> tuple[int,int]:
    """
    Retrieve data from the specified serial port, returning the two integers received. This function blocks until data is available.

    :ser: Serial port object to read from.

    Returns:
        Tuple of integers (d1, d2).
    """

    while ser.in_waiting == 0:
        pass

    try :
        line = ser.readline().decode('utf-8').strip()
        data = line.split(';')

        return int(data[0]), int(data[1])

    except :
        print('Error while retrieving data from the serial port.')
        return 0, 0
    
def convert_to_voltage(d1:int, d2:int, vref:int=3.3, adc_resolution:int=65535) -> tuple[float, float]:
    """
    Convert the raw ADC values to voltage.
    
    :d1, d2: Raw ADC values.
    :vref: Reference voltage (default is 3.3V).
    :adc_resolution: ADC resolution (default is 65535 for a 16-bit ADC).
    
    Returns:
        Tuple of voltages (v1, v2).
    """
    v1 = (d1 / adc_resolution) * vref
    v2 = (d2 / adc_resolution) * vref

    return v1, v2