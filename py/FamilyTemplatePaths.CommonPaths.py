import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

app = DocumentManager.Instance.CurrentUIApplication.Application
ver = int(app.VersionNumber)
OUT = app.FamilyTemplatePath
if ver > 2020:
	OUT += r"\English"