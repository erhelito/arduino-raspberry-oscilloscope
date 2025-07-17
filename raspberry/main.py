from machine import ADC, Pin # type: ignore

adc1 = ADC(Pin(26))  # GP26 = ADC0
adc2 = ADC(Pin(27))  # GP27 = ADC1

while True:
    value1 = adc1.read_u16()
    value2 = adc2.read_u16()
    print(f"{value1};{value2}")