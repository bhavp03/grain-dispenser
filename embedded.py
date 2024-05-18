import time
import machine
from machine import Pin
from ir_rx import NEC_16

motor_running = False  # Variable to track motor state

ir_key = {
    0x0C: '1',
    0x18: '2',
    0x5E: '3',
    0x08: '4',
    0x1C: '5',
    0x5A: '6',
    0x42: '7',
    0x52: '8',
    0x4A: '9'
}

def callback(data, addr, ctrl):
    global motor_running
    if data > 0:  # NEC protocol sends repeat codes.
        print('Data {:02x} Addr {:04x}'.format(data, addr))
        print(ir_key[data])
        pin = machine.Pin("D14", machine.Pin.OUT)
        pin.value(1)
        if ir_key[data] == '1':
            pin.value(0)
            time.sleep(5)
            pin.value(1)
        elif ir_key[data] == '2':
            if motor_running:  # Stop the motor if it's running
                pin.value(1)
                motor_running = False
            else:
                pin.value(0)
                time.sleep(10)
                pin.value(1)
        elif ir_key[data] == '3':
            pin.value(0)
            time.sleep(20)
            pin.value(1)

ir = NEC_16(Pin("D15", Pin.IN), callback)