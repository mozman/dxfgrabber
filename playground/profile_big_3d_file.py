import cProfile
import pstats

import dxfgrabber

PROFILE = "profile_cnc_machine.txt"
FILE = r"D:\source\dxftest\cnc machine.dxf"

cProfile.run('dwg = dxfgrabber.readfile("{}")'.format(FILE), PROFILE)

stat = pstats.Stats(PROFILE)

stat.strip_dirs().sort_stats('time').print_stats(10)