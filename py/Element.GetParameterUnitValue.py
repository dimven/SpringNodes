import clr

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

elems, parName = UnwrapElement(IN)
OUT = []

for e in elems:
	par = e.LookupParameter(parName)
	if par is None or par.StorageType.ToString() != "Double" or not par.HasValue:
		OUT.append("")
		continue
	val = DB.UnitUtils.ConvertFromInternalUnits(par.AsDouble(), par.DisplayUnitType)
	OUT.append(val)