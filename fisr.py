import struct

def fast_inv_sqrt(number):
    y = number
    i = struct.unpack("i", struct.pack("f", y))[0]
    i = 0x5f3759df - (i >> 1)
    y = struct.unpack("f", struct.pack("i", i))[0]
    return y * (1.5 - (number * 0.5 * y * y))