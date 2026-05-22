# Copyright(c) 2020, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('MeshToolkit')
import Autodesk.Dynamo.MeshToolkit.Mesh as tkMesh

def tolist(x):
    if hasattr(x,'__iter__'): return x
    return [x]

def orientation(v):
    area = 0.0
    for i in range(len(v)):
        area += v[i-1].X*v[i].Y - v[i-1].Y*v[i].X
    return area < 0.0 # if true, it is clockwise

def determinant(p1, p2, p3):
    determ = (p2.X - p1.X) * (p3.Y - p1.Y) - (p3.X - p1.X) * (p2.Y - p1.Y)
    return determ >= 0

def no_interior(p1, p2, p3, v, poly_or):
    for ip in v:
        p = ip[1]
        if p.IsAlmostEqualTo(p1) or p.IsAlmostEqualTo(p2) or p.IsAlmostEqualTo(p3):
            continue # Don't bother checking against yourself
        if determinant(p1, p2, p) == poly_or or \
            determinant(p3, p1, p) == poly_or or \
            determinant(p2, p3, p) == poly_or:
                continue  # This point is outside
        return False # The point is inside
    return True # No points inside this triangle

def draw_poly(poly):
    t1 = poly.GetType().ToString()
    if 'Polygon' in t1 or 'Rectangle' in t1:
        pts = poly.Points
    else:
        pts = [c.StartPoint for c in poly.Curves()]
    indices = []
    poly_orientation = orientation(pts)
    v = list(enumerate(pts))
    while len(v) > 3:
        for cur in range(len(v)):
            prev = cur - 1
            next = (cur + 1) % len(v)
            if determinant(v[cur][1], v[prev][1], v[next][1]) == poly_orientation and \
                no_interior(v[prev][1], v[cur][1], v[next][1], v, poly_orientation):
                    indices.extend((v[prev][0], v[cur][0], v[next][0]))
                    del(v[cur])
                    break
        else:
            raise('Error: Didn\'t find a triangle.\n')

    # Output the final triangle
    indices.extend([i[0] for i in v])
    return tkMesh.ByVerticesAndIndices(pts, indices)

OUT = map(draw_poly, tolist(IN[0]))