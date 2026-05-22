#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2016, Dimitar Venkov       #
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
import System
from System.Drawing import Point, Color, Font
from System.Windows.Forms import *
from System import Array, Object

import ctypes
DWMWA_USE_IMMERSIVE_DARK_MODE = 20

def tolist(obj1):
    if isinstance(obj1, str): return [obj1]
    return obj1 if isinstance(obj1, list) else [obj1]

def hasInd(l1, i):
    try: l1[i]; return True
    except: return False

class NameWrap(Object):
    def __init__(self, obj1, name1=None):
        self.obj = obj1
        if name1 is None:
            if obj1 is None:
                name1 = "null"
            else:
                name1 = str(obj1)
        self.name = name1

    def ToString(self):
        return self.name

class DropDownForm(Form):
    def __init__(self, cm1):
        super().__init__()
        self.Load += self.on_load
        self.output1 = None
        self.Text = "SpringNodes: Drop-Down Selection"
        self.Width = 368
        self.Height = 180
        self.MinimumSize = System.Drawing.Size(368, 180)
        self.BackColor = Color.FromArgb(40, 40, 40)
        self.ControlBox = True
        self.TopMost = True
        self.FormBorderStyle = FormBorderStyle.SizableToolWindow
        self.StartPosition = FormStartPosition.CenterScreen
        self.Resize += self.on_resize

        self.label = Label()
        self.label.Text = cm1
        self.label.Location = Point(5, 5)
        self.label.ForeColor = Color.FromArgb(234, 234, 234)
        self.label.Font = Font("Calibri", 10)
        self.label.AutoSize = True
        self.Controls.Add(self.label)

        self.combo1 = ComboBox()
        self.combo1.Location = Point(5, 31)
        self.combo1.Width = self.ClientSize.Width - 10
        self.combo1.BackColor = Color.FromArgb(53, 53, 53)
        self.combo1.ForeColor = Color.FromArgb(234, 234, 234)
        self.combo1.Font = Font("Calibri", 11)
        self.combo1.MouseClick += self.expand
        self.Controls.Add(self.combo1)

        self.button1 = Button()
        self.button1.Text = 'Select'
        self.button1.Width = self.ClientSize.Width - 10
        self.button1.Location = Point(5, self.ClientSize.Height - 40)
        self.button1.ForeColor = Color.FromArgb(234, 234, 234)
        self.button1.Font = Font("Calibri", 10)
        self.button1.Click += self.save
        self.Controls.Add(self.button1)

    def on_load(self, sender, event):
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            int(self.Handle.ToInt64()),
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
        ctypes.windll.uxtheme.SetWindowTheme(
            int(self.combo1.Handle.ToInt64()),
            "DarkMode_Explorer",
            None
        )

    def on_resize(self, sender, event):
        self.combo1.Width = self.ClientSize.Width - 10
        self.button1.Width = self.ClientSize.Width - 10
        self.button1.Location = Point(5, self.ClientSize.Height - 40)

    def expand(self, sender, event):
        self.combo1.DroppedDown = True

    def add_range(self, l1):
        self.wrapped = list(l1)
        self.combo1.Items.AddRange(Array[Object]([w.name for w in l1]))
        if len(l1) >= 1:
            self.combo1.SelectedIndex = 0

    def save(self, sender, event):
        self.output1 = self.wrapped[self.combo1.SelectedIndex]
        self.Close()

try:
    if IN[0] is None: l1 = []
    else: l1 = tolist(IN[0])
    if IN[1] is None: names = None
    else: names = tolist(IN[1])

    for i in range(len(l1)):
        name1 = None
        if hasInd(names, i):
            candidate = names[i]
            if isinstance(candidate, str):
                name1 = candidate
        if name1 is None:
            name1 = str(l1[i])
        l1[i] = NameWrap(l1[i], name1)

    form = DropDownForm(IN[2])
    form.add_range(l1)
    form.ShowDialog()

    if l1 and form.output1 is not None:
        OUT = form.output1.obj
    else:
        OUT = "No selection"

except Exception as e:
    import traceback
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e), traceback.format_exc()
    )