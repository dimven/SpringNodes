import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

app = DocumentManager.Instance.CurrentUIApplication.Application

OUT = app.FamilyTemplatePath