# Copyright(c) 2020, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Drawing import Point, Color, Font
from System.Windows.Forms import *
from cStringIO import StringIO

str_file = StringIO()
size1 = [30, 23] #height, width

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def write_str(str1, GCL, str_file=str_file, size1=size1):
	ln1 = len(str1)
	if ln1 > size1[1]:
		size1[1] = ln1
	
	str_file.write("%s%s\n" % ("".join(GCL), str1) )

def list2str(l1, writeInd, GCL=None, GCint=-1, size1=size1, isDict=False):
	if GCL is None:
		GCL = []
	GCint += 1
	GCL.append(None)
	for i, x in enumerate(l1):
		if isDict:
			i, x = x, l1[x]
			GCL[GCint] = "[%s] " % i if writeInd else "  "
		else:
			GCL[GCint] = "[%i] " % i if writeInd else "  "
		if hasattr(x, "Id"): #is element
			write_str("%s        %i" % (x.ToString(), x.Id), GCL)
		elif hasattr(x, "__iter__"):
			if not x:
				write_str("Empty List", GCL)
			else:
				list2str(x, writeInd, GCL, GCint, size1)
		elif "Dictionary" in x.GetType().ToString():
			d = x.Components()
			k, v = d["keys"], d["values"]
			list2str(dict(zip(k, v)), writeInd, GCL, GCint, size1, True)
		elif x is None:
			write_str("null", GCL)
		else:
			write_str(x.ToString(), GCL)
		size1[0] += 19
	GCL.pop(GCint)
	GCint -= 1

class WatchBox(Form):
	def __init__(self, t1):
		self.Text = "SpringNodes: Expandable Watch Window"
		self.BackColor = Color.FromArgb(40,40,40)
		self.ControlBox = False
		self.TopMost = True
		self.FormBorderStyle = FormBorderStyle.Sizable
		self.StartPosition = FormStartPosition.CenterScreen
		self.Resize += self.resize1
		self.text1 = None

		self.button1 = Button()
		self.button1.Text = 'Close'
		self.button1.Font = Font(IN[3], 10)
		self.button1.AutoSize = True
		self.button1.Width = 200
		self.button1.ForeColor = Color.FromArgb(234,234,234)
		self.button1.Click += self.save
		self.Controls.Add(self.button1)
		
		self.box1 = RichTextBox()
		self.box1.Multiline = True
		self.box1.Location = Point(5, 5)
		self.box1.Font = Font(IN[3], 12)
		self.box1.BackColor = Color.FromArgb(53,53,53)
		self.box1.ForeColor = Color.FromArgb(234,234,234)
		self.box1.DetectUrls = True
		self.box1.Text = t1
		self.Controls.Add(self.box1)

	def adjust_controls(self, height1, width1):
		if height1 > 800:
			height1 = 800
			self.box1.ScrollBars = RichTextBoxScrollBars.Vertical
		if width1 < 23 : width1 = 23
		if width1 > 88: width1 = 88
		self.Width = 10 + (width1 + 2) * 9 #character width seems to vary between PCs
		self.Height = height1 + 90
		self.box1.Width = self.Width - 17
		self.box1.Height = self.Height - 80
		self.button1.Location = Point(self.Width/2 - 103, self.Height - 70)
	
	def resize1(self, sender, event):
		if self.Width < 210: self.Width = 230
		if self.Height < 120: self.Height = 120
		self.box1.Width = self.Width - 17
		self.box1.Height = self.Height - 80
		self.button1.Location = Point(self.Width/2 - 103, self.Height - 70)
	
	def save(self, sender, event):
		self.text1 = self.box1.Text
		self.Close()

l1 = [] if IN[0] is None else tolist(IN[0])
list2str(l1, IN[1])
str_content = str_file.getvalue()
str_file.close()

width1 = 100
form = WatchBox(str_content)
form.adjust_controls(*size1)

Application.Run(form)
OUT = form.text1
Application.Exit()
form.Dispose()