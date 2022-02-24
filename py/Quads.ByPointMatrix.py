pts, ccw = IN
OUT = []

for i in xrange(len(pts) - 1):
	for j in xrange(len(pts[0]) - 1):
		if ccw:
			OUT.append([pts[i][j],
						pts[i][j+1],
						pts[i+1][j+1],
						pts[i+1][j]])
		else:
			OUT.append([pts[i][j],
						pts[i+1][j],
						pts[i+1][j+1],
						pts[i][j+1]])