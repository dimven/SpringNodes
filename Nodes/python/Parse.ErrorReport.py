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

def getElement(i):
	try: return doc.GetElement(ElementId(i)).ToDSType(1)
	except: return i

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
report_data = parser.data1[1:]
parser.close()
errors, elements = [], []
for data in report_data:
	isError = True
	ids = []
	for d in data:
		if isError:
			errors.append(d.strip())
			isError = False
			continue
		id = filter(str.isdigit, d.rsplit(" : ", 1)[-1])
		if id.isdigit():
			id = int(id)
		else:
			continue
		if fetch_elements:
			id = getElement(id)
		ids.append(id)
	elements.append(ids)

group_errors = Counter(errors).most_common()
unique_errors, sum_errors = zip(*group_errors)
sum_errors = list(sum_errors)
sum_errors.append("Total errors : %d" % sum(sum_errors) )
OUT = errors, elements, unique_errors, sum_errors