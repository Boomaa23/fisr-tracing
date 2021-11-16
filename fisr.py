import struct
import math
from datetime import datetime
import multiprocessing

def fast_inv_sqrt(number):
    y = number
    i = struct.unpack("i", struct.pack("f", y))[0]
    i = 0x5f3759df - (i >> 1)
    y = struct.unpack("f", struct.pack("i", i))[0]
    return y * (1.5 - (number * 0.5 * y * y))

def tester(lower, upper):
    start = datetime.now()
    for num in range(lower, upper):
        fast_inv_sqrt(num)
    print(f"FISR struct time: {datetime.now() - start}")

    start = datetime.now()
    for num in range(lower, upper):
        1 / math.sqrt(num)
    print(f"math.sqrt time: {datetime.now() - start}")

if __name__ == "__main__":
    for _ in range(24):
        multiprocessing.Process(target=tester, args=(1, 10000000)).start()