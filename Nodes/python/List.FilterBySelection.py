#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2017, Dimitar Venkov       #
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
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Drawing import Point, Color, Font
from System.Windows.Forms import *

import ctypes
DWMWA_USE_IMMERSIVE_DARK_MODE = 20

def tolist(obj1):
    if isinstance(obj1, str): return [obj1]
    return obj1 if isinstance(obj1, list) else [obj1]

def hasInd(l1, i):
    try: l1[i]; return True
    except: return False

class CheckBoxForm(Form):
    def __init__(self, cm1):
        super().__init__()
        self.Load += self.on_load
        self.Text = "SpringNodes: Filter By Selection"
        self.Width = 450
        self.BackColor = Color.FromArgb(40, 40, 40)
        self.output1 = None
        self.objects = []
        self.ControlBox = True
        self.TopMost = True
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.Resize += self.on_resize
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormClosing += self.DisableForceClose

        self.label = Label()
        self.label.Text = cm1
        self.label.Location = Point(5, 5)
        self.label.ForeColor = Color.FromArgb(234, 234, 234)
        self.label.Font = Font("Calibri", 10)
        self.label.AutoSize = True
        self.Controls.Add(self.label)

        self.clb = CheckedListBox()
        self.clb.Location = Point(5, 31)
        self.clb.Width = self.Width - 20
        self.clb.BackColor = Color.FromArgb(53, 53, 53)
        self.clb.ForeColor = Color.FromArgb(234, 234, 234)
        self.clb.Font = Font("Calibri", 10)
        self.clb.BorderStyle = getattr(BorderStyle, 'None')
        self.clb.CheckOnClick = True
        self.clb.IntegralHeight = False
        self.clb.Anchor = AnchorStyles.Top | AnchorStyles.Left
        self.Controls.Add(self.clb)

        self.button1 = Button()
        self.button1.Text = 'Save Selection'
        self.button1.ForeColor = Color.FromArgb(234, 234, 234)
        self.button1.Font = Font("Calibri", 10)
        self.button1.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button1.Click += self.save
        self.Controls.Add(self.button1)

        self.button2 = Button()
        self.button2.Text = 'Uncheck All'
        self.button2.ForeColor = Color.FromArgb(234, 234, 234)
        self.button2.Font = Font("Calibri", 10)
        self.button2.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button2.Click += self.uncheckAll
        self.Controls.Add(self.button2)

        self.button3 = Button()
        self.button3.Text = 'Check All'
        self.button3.ForeColor = Color.FromArgb(234, 234, 234)
        self.button3.Font = Font("Calibri", 10)
        self.button3.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button3.Click += self.checkAll
        self.Controls.Add(self.button3)

    def on_load(self, sender, event):
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            int(self.Handle.ToInt64()),
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
        ctypes.windll.uxtheme.SetWindowTheme(
            int(self.clb.Handle.ToInt64()),
            "DarkMode_Explorer",
            None
        )

    def btn_adjust(self, count):
        clb_h = min(count * 20 + 10, 300)
        self.clb.Height = clb_h
        self.clb.ScrollAlwaysVisible = True
        btn_y = 31 + clb_h + 8
        btn_width = (self.Width - 40) // 3
        self.button1.Width = btn_width
        self.button2.Width = btn_width
        self.button3.Width = btn_width
        self.button1.Location = Point(5, btn_y)
        self.button2.Location = Point(5 + btn_width + 5, btn_y)
        self.button3.Location = Point(5 + (btn_width + 5) * 2, btn_y)
        self.Height = btn_y + 70
        self.clb.Anchor = (AnchorStyles.Top | AnchorStyles.Bottom
                         | AnchorStyles.Left | AnchorStyles.Right)

    def on_resize(self, sender, event):
        self.clb.Width = self.Width - 20
        btn_width = (self.Width - 40) // 3
        btn_y = self.clb.Bottom + 8
        self.button1.Width = btn_width
        self.button2.Width = btn_width
        self.button3.Width = btn_width
        self.button1.Location = Point(5, btn_y)
        self.button2.Location = Point(5 + btn_width + 5, btn_y)
        self.button3.Location = Point(5 + (btn_width + 5) * 2, btn_y)

    def save(self, sender, event):
        self.output1 = [self.objects[i] for i in range(self.clb.Items.Count)
                        if self.clb.GetItemChecked(i)]
        self.Close()

    def uncheckAll(self, sender, event):
        for i in range(self.clb.Items.Count):
            self.clb.SetItemChecked(i, False)

    def checkAll(self, sender, event):
        for i in range(self.clb.Items.Count):
            self.clb.SetItemChecked(i, True)

    def DisableForceClose(self, sender, event):
        if self.output1 is None:
            self.output1 = None

try:
    l1 = tolist(IN[0])
    if IN[1] is None: names = None
    else: names = tolist(IN[1])

    form = CheckBoxForm(IN[2])
    for i in range(len(l1)):
        try:
            if hasInd(names, i):
                candidate = names[i]
                val1 = candidate if isinstance(candidate, str) else str(l1[i])
            else:
                val1 = str(l1[i])
            form.clb.Items.Add(val1)
            form.clb.SetItemChecked(i, IN[3])
            form.objects.append(l1[i])
        except: pass
    form.btn_adjust(len(l1))

    form.ShowDialog()

    if form.output1 is None:
        OUT = "No selection"
    else:
        OUT = form.output1

except Exception as e:
    import traceback
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e),
        traceback.format_exc()
    )