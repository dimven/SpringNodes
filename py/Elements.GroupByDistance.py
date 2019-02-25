#Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net
#Inspired from the "Group Curves" node by Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Geometry

elem, loc, margin = IN

pts = zip(elem, loc)
dist1 = Geometry.DistanceTo
Groups, Queue = [], []
while pts:
	group = []
	Queue.append(pts.pop() )
	while Queue:
		p1 = Queue.pop()
		group.append(p1)
		for i in xrange(len(pts)-1,-1,-1):
			if dist1(p1[1], pts[i][1]) <= margin:
				Queue.append(pts.pop(i) )
	Groups.append(group)

elem1 = [ [j[0] for j in i] for i in Groups]
pts1 = [ [j[1] for j in i] for i in Groups]
OUT = elem1, pts1