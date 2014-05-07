import time
import dxfgrabber

FILE = r"D:\source\dxftest\cnc machine.dxf"

start_time = time.time()
dwg = dxfgrabber.readfile(FILE)
end_time = time.time()

print("Runtime: {:.3f} Sec.".format(end_time-start_time))

