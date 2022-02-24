import clr
import System
pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append("%s\IronPython 2.7\Lib" %pf_path)

from sgmllib import SGMLParser
from collections import Counter


class ReportParser(SGMLParser):
	def __init__(self, verbose=0):
		SGMLParser.__init__(self, verbose)
		self.data1 = []
		self.temp_data = []
	def handle_data(self, data):
		if data != "\n" and data not in known_errors:
			self.temp_data.append(data)
	def unknown_starttag(self, tag, attrs):
		if tag == "tr":
			self.data1.append(self.temp_data)
			self.temp_data = []

interference_cats = {"Structural Columns", "Air Terminals", "Assemblies", "Cable Tray Fittings", "Cable Tray Runs", "Cable Trays", "Casework", "Ceilings", "Columns", "Conduit Fittings", "Conduit Runs", "Conduits", "Curtain Panels", "Curtain Systems", "Curtain Wall Mullions","Doors", "Ducts", "Duct Accessories", "Duct Fittings", "Duct Insulations", "Duct Linings", "Duct Placeholders", "Duct Systems", "Electrical Circuits", "Electrical Equipment", "Electrical Fixtures", "Fabrication Parts", "Flex Ducts", "Flex Pipes", "Floors", "Furniture", "Furniture Systems", "Generic Models", "Gutters", "Lighting Devices", "Lighting Fixtures", "Mass Floors", "Mass", "Mechanical Equipment", "Pads", "Parts", "Pipe Accessories", "Pipe Fittings", "Pipe Insulations", "Pipe Placeholders", "Pipes", "Piping Systems",  "Plumbing Fixtures", "Railings", "Ramps", "Roofs", "Roof Soffits", "Shaft Openings", "Slab Edges", "Specialty Equipment", "Sprinklers", "Stairs", "Structural Connections", "Structural Foundations", "Structural Framing", "Structural Trusses", "Wall Sweeps", "Walls", "Windows", "Wires"}

def getElement(i):
	try: return doc.GetElement(ElementId(i)).ToDSType(1)
	except: return i

def fetchCat(items, interference_cats=interference_cats):
	for i in items:
		if i in interference_cats:
			return i

report1, fetch_elements = IN

if fetch_elements:	#imports moved here to be able to process externally
	clr.AddReference("RevitServices")
	from RevitServices.Persistence import DocumentManager
	doc = DocumentManager.Instance.CurrentDBDocument
	clr.AddReference("RevitAPI")
	from Autodesk.Revit.DB import ElementId
	clr.AddReference('RevitNodes')
	import Revit
	clr.ImportExtensions(Revit.Elements)

known_errors = {"  ", "td>  "}
parser = ReportParser()
with System.IO.File.OpenText(report1) as f:
	while not f.EndOfStream:
		parser.feed(f.ReadLine().replace("&", ""))
parser.data1.append(parser.temp_data)
report_data = parser.data1[2:]
parser.close()
parser = None
cases, elements, = [], []
for d in report_data:
	left, right = map(str.strip, d[1].split(" : ")), map(str.strip, d[2].split(" : "))
	leftId, rightId = int(filter(str.isdigit, left[-1])), int(filter(str.isdigit, right[-1]))
	if fetch_elements:
		leftId, rightId = getElement(leftId), getElement(rightId)
	elements.append((leftId, rightId))
	
	leftCat, rightCat = fetchCat(left), fetchCat(right)
	case = "%s - %s" % (leftCat, rightCat) if leftCat is not None and rightCat is not None else "Unidentified"
	cases.append(case)

group_cases = Counter(cases).most_common()
unique_cases, sum_cases = zip(*group_cases)
sum_cases = list(sum_cases)
sum_cases.append("Total interferences : %s" % sum(sum_cases) )
OUT = cases, elements, unique_cases, sum_cases