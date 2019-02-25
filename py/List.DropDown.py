#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point, Color, Font
from System.Windows.Forms import *
from System import Array, Object

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def hasInd(l1, i):
	try: l1[i] ; return True
	except: return False

class NameWrap(Object):
	def __init__(self, obj1, name1 = None):
		self.obj = obj1
		if obj1 == None: name1 = "null"
		if name1 == None and obj1 != None: self.name = obj1.ToString()
		else: self.name = name1
	def ToString(self):
		return self.name

class DropDownForm(Form):
	def __init__(self, cm1):
		self.Text = "SpringNodes: Drop-Down Selection"
		self.Width = 368
		self.Height = 142
		self.BackColor = Color.FromArgb(40,40,40)
		self.ControlBox = False
		self.TopMost = True
		self.FormBorderStyle = FormBorderStyle.FixedDialog
		self.StartPosition = FormStartPosition.CenterScreen
		
		self.label = Label()
		self.label.Text = cm1
		self.label.Location = Point(5, 5)
		self.label.ForeColor = Color.FromArgb(234,234,234)
		self.label.Font = Font("Calibri", 10)
		self.label.AutoSize = True
		self.Controls.Add(self.label)
		
		self.combo1 = ComboBox()
		self.combo1.Location = Point(5, 31)
		self.combo1.Width = 350
		self.combo1.BackColor = Color.FromArgb(53,53,53)
		self.combo1.ForeColor = Color.FromArgb(234,234,234)
		self.combo1.Font = Font("Calibri", 11)
		self.combo1.MouseClick += self.expand
		self.Controls.Add(self.combo1)
		
		self.button1 = Button()
		self.button1.Text = 'Select'
		self.button1.AutoSize = True
		self.button1.Width = 350
		self.button1.Location = Point(6, 72)
		self.button1.ForeColor = Color.FromArgb(234,234,234)
		self.button1.Font = Font("Calibri", 10)
		self.button1.Click += self.save
		self.Controls.Add(self.button1)
	
	def expand(self, sender, event):
		self.combo1.DroppedDown = True
	def add_range(self,l1):
		self.combo1.Items.AddRange(l1)	
		if l1.Length >= 1:
			self.combo1.SelectedIndex = 0
	def save(self, sender, event):
		self.output1 = self.combo1.SelectedItem
		self.Close()
#safety measure due to automatic mode
if IN[0] == None: l1 = []
else: l1 = tolist(IN[0])
if IN[1] == None: names = None
else: names = tolist(IN[1])

for i in xrange(len(l1)):
	name1 = None
	if hasInd(names, i): name1 = names[i]
	l1[i] = NameWrap(l1[i], name1)
l1_arr = Array[Object](l1)
form = DropDownForm(IN[2])
form.add_range(l1_arr)
Application.Run(form)
if l1: OUT = form.output1.obj
else: OUT = []
Application.Exit()