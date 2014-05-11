import sys
import glob
import dxfgrabber
import time
from itertools import chain

from dxfgrabber.tags import CYTHON_EXT
if "win" in sys.platform:
    DIR1 = r"D:\Source\dxftest\CADKitSamples\*.dxf"
    DIR2 = r"D:\Source\dxftest\*.dxf"
else:
    DIR1 = r"/media/sf_winsource/dxftest/CADKitSamples/*.dxf"
    DIR2 = r"/media/sf_winsource/dxftest/*.dxf"

all_files = chain(glob.glob(DIR1), glob.glob(DIR2))
overall_time = 0
ok = 0
error = 0

print('Cython acceleration is ' + ('on' if CYTHON_EXT else 'off'))
print("Stress test:")

for filename in all_files:
    try:
        start_time = time.time()
        dwg = dxfgrabber.readfile(filename)
        end_time = time.time()
        run_time = end_time - start_time
    except Exception:
        error += 1
        print('errors at opening: {}'.format(filename))
    else:
        ok += 1
        overall_time += run_time
        print('ok ({:.2f} seconds for opening: {})'.format(run_time, filename))

print("{:.2f} seconds for {} files".format(overall_time, ok))
print("{} errors".format(error))
print('success' if error == 0 else 'failed')