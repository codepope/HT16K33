from ._HT16K33 import Device

# This is a library for the Adafruit Trellis w/HT16K33
#
#   Designed specifically to work with the Adafruit Trellis 
#   ----> https://www.adafruit.com/products/1616
#   ----> https://www.adafruit.com/products/1611
#
#   These displays use I2C to communicate, 2 pins are required to  
#   interface
#   Adafruit invests time and resources providing this open source code, 
#   please support Adafruit and open-source hardware by purchasing 
#   products from Adafruit!
#
#   Written by Limor Fried/Ladyada for Adafruit Industries.  
#   MIT license, all text above must be included in any redistribution
#
#   Python port created by Tony DiCola (tony@tonydicola.com
# 
#   Re-ported to the HT16K33 package by Dj Walker-Morgan (codepope@gmail.com)
#

__all__ = ['Trellis']


class Trellis(Device):
    '''
       AdaFruit Trellis
       - - -
    '''

    ledLUT =  [ 0x3A, 0x37, 0x35, 0x34, 
    			0x28, 0x29, 0x23, 0x24, 
    			0x16, 0x1B, 0x11, 0x10, 
    			0x0E, 0x0D, 0x0C, 0x02 ]
    buttonLUT = [ 0x07, 0x04, 0x02, 0x22,
    			  0x05, 0x06, 0x00, 0x01,
    			  0x03, 0x10, 0x30, 0x21,
    			  0x13, 0x12, 0x11, 0x31 ]

    def setUp(self,**kwargs):
        super().setUp()
        self.displaybuffer=[0]*8
        self._keys=[0]*6
        self._lastkeys=[0]*6
        self.bus.write_byte_data(self.address,0xa1,0)
        return self

    def writeDisplay(self):
        """Write the LED display buffer values to the hardware."""
        #self._check_i2c()
        data = []
        for buf in self.displaybuffer:
        	data.append(buf & 0xFF)
        	data.append(buf >> 8)
        self.bus.write_i2c_block_data(self.address, 0, data)

    def clear(self):
        """Clear all the LEDs in the display buffer."""
        self.displaybuffer = [0] * 8

    def isKeyPressed(self, k):
        """Check if the specified key was pressed during the last readSwitches call."""
        if k > 16 or k < 0: return False
        return (self._keys[self.buttonLUT[k] >> 4] & (1 << (self.buttonLUT[k] & 0x0F))) > 0

    def wasKeyPressed(self, k):
        """Check if the specified key was pressed before the last readSwitches call."""
        if k > 16 or k < 0: return False
        return (self._lastkeys[self.buttonLUT[k] >> 4] & (1 << (self.buttonLUT[k] & 0x0F))) > 0

    def isLED(self, x):
        """Return True if the specified LED is illuminated in the display buffer."""
        if x > 16 or x < 0: return False
        return (self.displaybuffer[self.ledLUT[x] >> 4] & (1 << (self.ledLUT[x] & 0x0F))) > 0

    def setLED(self, x):
        """Turn on the specified LED in the display buffer."""
        if x > 16 or x < 0: return  
        self.displaybuffer[self.ledLUT[x] >> 4] |= (1 << (self.ledLUT[x] & 0x0F))

    def clrLED(self, x):
        """Turn off the specified LED in the display buffer."""
        if x > 16 or x < 0: return
        self.displaybuffer[self.ledLUT[x] >> 4] &= ~(1 << (self.ledLUT[x] & 0x0F))

    def readSwitches(self):
    	"""Read the state of the buttons from the hardware.
    	Returns True if a button is pressed, False otherwise.
    	"""
    	#self._check_i2c()
    	self._lastkeys = self._keys
    	self._keys = self.bus.read_i2c_block_data(self.address,0x40, 6)
    	return any(map(lambda key, lastkey: key != lastkey, self._keys, self._lastkeys))
    
    def justPressed(self, k):
    	"""Return True if the specified key was first pressed in the last readSwitches call."""
    	return self.isKeyPressed(k) and not self.wasKeyPressed(k)
    
    def justReleased(self, k):
    	"""Return True if the specified key was just released in the last readSwitches call."""
    	return not self.isKeyPressed(k) and self.wasKeyPressed(k)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
