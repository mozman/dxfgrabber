import cProfile
import pstats

import dxfgrabber

PROFILE = "profile_ACAD_R12_dxf.txt"
FILE = r"D:\source\dxftest\ACAD_R12.dxf"

cProfile.run('dwg = dxfgrabber.readfile("{}")'.format(FILE), PROFILE)

stat = pstats.Stats(PROFILE)

stat.strip_dirs().sort_stats('time').print_stats(10)