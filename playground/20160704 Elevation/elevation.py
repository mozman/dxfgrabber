
import dxfgrabber

dwg = dxfgrabber.readfile('contourlines.dxf')
msp = dwg.modelspace()
plines = (entity for entity in msp if entity.dxftype in ('POLYLINE', 'LWPOLYLINE'))
for num, pline in enumerate(plines, start=1):
    print("{0}. {1} - elevation: {2}". format(num, pline.dxftype, pline.elevation))
