import clr
from itertools import groupby
from operator import itemgetter
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point

def p2t(p) : return round(p.X,4), round(p.Y,4), round(p.Z,4)

pts = map(p2t, IN[0])
unique_pts = set(pts)
if not IN[1]:
	same_z = [(i[:2],i[-1]) for i in unique_pts]
	same_z.sort(key = itemgetter(0) )
	unique_pts = []
	for k, g in groupby(same_z, itemgetter(0) ):
		coord = list(k)
		coord.append(max([i[-1] for i in g]) )
		unique_pts.append(coord)
OUT = [Point.ByCoordinates(*i) for i in unique_pts]