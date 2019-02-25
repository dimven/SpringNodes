#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
#Inspired from the "Group Curves" node by Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Geometry

pts = IN[0]
margin = IN[1]
dist1 = Geometry.DistanceTo

Groups, Queue = [], []
while pts:
	group = []
	Queue.append(pts.pop() )
	while Queue:
		p1 = Queue.pop()
		group.append(p1)
		for i in xrange(len(pts)-1,-1,-1):
			if dist1(p1, pts[i]) <= margin:
				Queue.append(pts.pop(i) )
	Groups.append(group)

OUT = Groups