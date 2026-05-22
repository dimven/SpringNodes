#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2016, Dimitar Venkov       #
#                                              #
# https://github.com/dimven/SpringNodes/issues #
# https://www.reope.com/                       #
#                                              #
#    ____    _____   _____   ____    _____     #
#   |  _ \ *|  ___|*|  _  |*|  _ \ *|  ___|    #
#   | |_) |*| |___ *| | | |*| |_) |*| |___     #
#   |  _ < *|  ___|*| | | |*|  __/ *|  ___|    #
#   | | | |*| |___ *| |_| |*| |    *| |___     #
#   |_| \_|*|_____|*|_____|*|_|    *|_____|    #
#                                              #
#                                              #
#-Reope-----Updated by Mark Ackerley-----------#

import clr
import math
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
    if isinstance(obj1, str): return [obj1]
    return obj1 if isinstance(obj1, list) else [obj1]

accepted_mc = "Autodesk.Revit.DB.ModelLine, Autodesk.Revit.DB.ModelArc, Autodesk.Revit.DB.ModelEllipse, Autodesk.Revit.DB.ModelHermiteSpline, Autodesk.Revit.DB.ModelNurbSpline"

def almost_eq(line, mc):
    line2 = mc.Location.Curve
    xyz1 = line.Evaluate(0.5, True)
    if not line2.IsBound:
        xyz2 = line2.Center
        try: xyz1 = line.Center
        except: pass
    else:
        xyz2 = line2.Evaluate(0.5, True)
    return xyz1.DistanceTo(xyz2) <= 0.0001

def clean1(l1):
    for i in range(len(l1)):
        l1[i] = [x for x in l1[i] if x is not None]
    return l1

def getSketch(el1):
    dep_ids = el1.GetDependentElements(None)

    sketches, mc = [], []
    for dep_id in dep_ids:
        test_el = doc.GetElement(dep_id)
        el_type = test_el.GetType().ToString()
        if el_type == "Autodesk.Revit.DB.Sketch":
            sketches.append(test_el)
        elif getModel and el_type in accepted_mc:
            mc.append(test_el)

    sketches.sort(key=lambda s: s.Id.Value)
    profile = sketches[0].Profile if sketches else CurveArrArray()

    ordered_mc = [[None] * i.Size for i in profile] if getModel else []
    curves = [[None] * i.Size for i in profile]
    for i in range(profile.Size):
        for j in range(profile[i].Size):
            curves[i][j] = profile[i][j].ToProtoType()
            if getModel:
                for k in range(len(mc)):
                    if almost_eq(profile[i][j], mc[k]):
                        ordered_mc[i][j] = mc[k].ToDSType(True)
                        del mc[k]
                        break

    return curves, clean1(ordered_mc)

try:
    is_list = isinstance(IN[0], list)
    elements = UnwrapElement(tolist(IN[0]))
    getModel = IN[1]

    TransactionManager.Instance.EnsureInTransaction(doc)
    result = list(map(getSketch, elements))
    TransactionManager.Instance.TransactionTaskDone()

    OUT = [r[0] for r in result], [r[1] for r in result]

except Exception as e:
    import traceback
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e),
        traceback.format_exc()
    )