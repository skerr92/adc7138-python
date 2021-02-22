# ADS7138 8 channel analog to digital converter driver
# Author: Seth Kerr
# License: MIT License

"""
`odt_at42qt1070`
====================================================
CircuitPython driver for the AT42QT1070 capacitive touch acorn.
See usage in the examples/simpletest.py file.
* Author(s): Seth Kerr
Implementation Notes
--------------------
**Hardware:**
* Oak Dev Tech `7-Key Capacitive Touch Sensor Breakout - AT42QT1070
  <>`
  **Software and Dependencies:**
  * Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
    https://github.com/adafruit/circuitpython/releases
    * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time

import adafruit_bus_device.i2c_device as i2c_device
from micropython import const

__version__ = "0.0.0-audo.0"
__repo__ = ""

# default i2c address
ADS7138_I2CADDR = (0x10)

# Register Addresses

SYSTEM_STATUS = (0x0)
GENERAL_CFG = (0x1)
DATA_CFG = (0x2)
OSR_CFG = (0X3)
OPMODE_CFG = (0X4)
PIN_CFG = (0X5)
GPIO_CFG = (0X6)

class ADS7138:
    """Driver for ADS7138"""

    def __init__(self, i2c, address=ADS7138_I2CADDR):
        self._i2c = i2c_device.I2CDevice(i2c,address)
        self._buffer = bytearray(2)
        self.reset()

    def _write_register_byte(self, register, value):
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_register_bytes(self, register, result, length=None):
        if length is None:
            length = len(result)
        with self._i2c:
            self._i2c.write_then_readinto(bytes([register]), result, in_end=length)

    def reset(self):
        # write to the reset bit of general config register
        self._write_register_byte(GENERAL_CFG, 0x01)
        time.sleep(
                0.001)


    def cal(self):
        # write to calibration bit of general config register
        self._write_register_byte(GENERAL_CFG, 0x02)
        time.sleep(
                0.001)

    def get_status(self):
        self._read_register_bytes(SYSTEM_STATUS, self._buffer)
        return self._buffer[1]


