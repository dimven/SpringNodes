#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Drawing import Point, Color, Font
from System.Windows.Forms import *

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]
	
def hasInd(l1, i):
	try: l1[i] ; return True
	except: return False

class CheckBoxForm(Form):
	def __init__(self, cm1):
		self.Text = "SpringNodes: Filter By Selection"
		self.Width = 367
		self.BackColor = Color.FromArgb(40,40,40)
		self.output1 = []
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

		self.button1 = Button()
		self.button1.Text = 'Save Selection'
		self.button1.AutoSize = True
		self.button1.ForeColor = Color.FromArgb(234,234,234)
		self.button1.Font = Font("Calibri", 10)
		self.button1.Click += self.save
		self.Controls.Add(self.button1)

		self.button2 = Button()
		self.button2.Text = 'Uncheck All'
		self.button2.AutoSize = True
		self.button2.ForeColor = Color.FromArgb(234,234,234)
		self.button2.Font = Font("Calibri", 10)
		self.button2.Click += self.uncheckAll
		self.Controls.Add(self.button2)

		self.button3 = Button()
		self.button3.Text = 'Check All'
		self.button3.AutoSize = True
		self.button3.ForeColor = Color.FromArgb(234,234,234)
		self.button3.Font = Font("Calibri", 10)
		self.button3.Click += self.checkAll
		self.Controls.Add(self.button3)
		
		self.panel1 = Panel()
		self.panel1.Location = Point(5, 31)
		self.panel1.Width = 350
		self.panel1.BackColor = Color.FromArgb(53,53,53)
		self.panel1.ForeColor = Color.FromArgb(234,234,234)
		self.Controls.Add(self.panel1)
		
	def add_check(self, text1, y1, b1):
		self.check1 = CheckBox()
		self.check1.Text = text1
		self.check1.Location = Point(5, y1)
		self.check1.AutoSize = True
		self.check1.Font = Font("Calibri", 10)
		self.check1.Checked = b1
		self.panel1.Controls.Add(self.check1)
	
	def btn_adjust(self,y1):
		if y1 > 700:
			y1 = 700
			self.panel1.AutoScroll = True
			self.panel1.Focus()
		self.panel1.Height = y1
		self.button1.Location = Point(5,   y1 + 38)
		self.button2.Location = Point(170, y1 + 38)
		self.button3.Location = Point(275, y1 + 38)
		self.Height = y1 + 100
			
	def save(self, sender, event):
		ctrl1 = self.panel1.Controls
		count1 = ctrl1.Count
		loc = 0
		self.output1 = [c.Checked == 1 for c in ctrl1]
		#for i in xrange(count1):
		#	if ctrl1[i].Checked == 1:
		#		self.output1.append(l1[loc])
		#	else:
		#		self.output2.append(l1[loc])
		#	loc += 1
		self.Close()
	
	def uncheckAll(self, sender, event):
		ctrl1 = self.panel1.Controls
		count1 = ctrl1.Count
		for i in xrange(count1):
			ctrl1[i].Checked = False
	
	def checkAll(self, sender, event):
		ctrl1 = self.panel1.Controls
		count1 = ctrl1.Count
		for i in xrange(count1):
			ctrl1[i].Checked = True

l1 = tolist(IN[0])
if IN[1] == None: names = None
else: names = tolist(IN[1])

form = CheckBoxForm(IN[2])
y1 = 5
for i in xrange(len(l1)):
	try:
		if hasInd(names, i): val1 = names[i].ToString()
		else: val1 = l1[i].ToString()
		form.add_check(val1, y1, IN[3])
		y1 += 25
	except: pass
form.btn_adjust(y1)

Application.Run(form)
OUT = form.output1#, form.output2
Application.Exit()