#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

rdat = IN[0].lower()
all_rev, match = [], []

fec = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Revisions)
for f in fec:
	rev1 = f.ToDSType(True)
	all_rev.append(rev1)
	par1 = f.get_Parameter(BuiltInParameter.PROJECT_REVISION_REVISION_DATE)
	if par1.AsString().lower() == rdat: match.append(rev1)
if len(match) != 0: OUT = match, all_rev
else: OUT = "No revisions found from date %s" %rdat, all_rev