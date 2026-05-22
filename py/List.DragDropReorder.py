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
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System
import System.Threading as Threading
from System.Drawing import Point, Font, Color, Size
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

class DragDrop(Form):
    def __init__(self, cm1):
        super().__init__()
        self.Load += self.on_load
        self.Text = "SpringNodes: Drag and Drop Reorder"
        self.Width = 367
        self.Height = n + 170
        self.MinimumSize = Size(367, 250)
        self.ControlBox = False
        self.TopMost = True
        self.BackColor = Color.FromArgb(40, 40, 40)
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormClosing += self.DisableForceClose
        self.SafeToClose = False

        self.label = Label()
        self.label.Text = cm1
        self.label.Location = Point(5, 5)
        self.label.ForeColor = Color.FromArgb(234, 234, 234)
        self.label.Font = Font("Calibri", 10)
        self.label.AutoSize = True
        self.Controls.Add(self.label)

        self.box1 = ListBox()
        self.box1.Location = Point(5, 32)
        self.box1.Width = 340
        self.box1.Height = n
        self.box1.BackColor = Color.FromArgb(53, 53, 53)
        self.box1.ForeColor = Color.FromArgb(234, 234, 234)
        self.box1.Font = Font("Calibri", 11)
        self.box1.BorderStyle = getattr(BorderStyle, 'None')
        self.box1.AllowDrop = True
        self.box1.HorizontalScrollbar = True
        self.box1.ScrollAlwaysVisible = True
        self.box1.Anchor = (AnchorStyles.Top | AnchorStyles.Bottom
                          | AnchorStyles.Left | AnchorStyles.Right)
        self.box1.MouseDown += self.Drag1
        self.box1.DragOver += self.Over1
        self.box1.DragDrop += self.Drop1
        self.Controls.Add(self.box1)

        self.button1 = Button()
        self.button1.Text = 'Save Order'
        self.button1.Width = 150
        self.button1.ForeColor = Color.FromArgb(234, 234, 234)
        self.button1.Font = Font("Calibri", 10)
        self.button1.Location = Point(20, n + 55)
        self.button1.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button1.Click += self.save
        self.Controls.Add(self.button1)

        self.button2 = Button()
        self.button2.Text = 'Close'
        self.button2.Width = 150
        self.button2.ForeColor = Color.FromArgb(234, 234, 234)
        self.button2.Font = Font("Calibri", 10)
        self.button2.Location = Point(190, n + 55)
        self.button2.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button2.Click += self.cancel
        self.Controls.Add(self.button2)

    def on_load(self, sender, event):
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
        int(self.Handle.ToInt64()),
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value))
        
        ctypes.windll.uxtheme.SetWindowTheme(int(self.box1.Handle.ToInt64()),"DarkMode_Explorer",None)
        
        if self.box1.Items.Count > 0:
            max_w = max(
                TextRenderer.MeasureText(str(item), self.box1.Font).Width
                for item in self.box1.Items
            )

    def add_range(self, l1):
        self.wrapped = list(l1)
        self.order = list(range(len(l1)))
        self.box1.Items.AddRange(Array[Object]([w.name for w in l1]))

    def save(self, sender, event):
        self.output1 = [self.wrapped[i] for i in self.order]
        self.SafeToClose = True
        self.Close()

    def cancel(self, sender, event):
        self.output1 = None
        self.SafeToClose = True
        self.Close()

    def Drag1(self, sender, event):
        if self.box1.SelectedItem is None:
            pass
        else:
            self.box1.DoDragDrop(self.box1.SelectedItem, DragDropEffects.Move)

    def Over1(self, sender, event):
        event.Effect = DragDropEffects.Move

    def Drop1(self, sender, event):
        pt1 = self.box1.PointToClient(Point(event.X, event.Y))
        ind1 = self.box1.IndexFromPoint(pt1)
        if ind1 < 0: ind1 = self.box1.Items.Count - 1
        src = self.box1.SelectedIndex
        data1 = event.Data.GetData(str)
        self.box1.Items.Remove(data1)
        self.box1.Items.Insert(ind1, data1)
        self.order.insert(ind1, self.order.pop(src))

    def DisableForceClose(self, sender, event):
        if not self.SafeToClose:
            event.Cancel = True

try:
    if IN[0] is None: l1 = []
    else: l1 = tolist(IN[0])
    if IN[1] is None: names = None
    else: names = tolist(IN[1])

    n = 22 * len(l1) + 5
    if not l1: n = 27
    if n > 700: n = 700

    for i in range(len(l1)):
        name1 = None
        if hasInd(names, i):
            candidate = names[i]
            if isinstance(candidate, str):
                name1 = candidate
        if name1 is None:
            name1 = str(l1[i])
        l1[i] = NameWrap(l1[i], name1)

    form_holder = [None]

    def run_form():
        f = DragDrop(IN[2])
        f.add_range(l1)
        f.ShowDialog()
        form_holder[0] = f

    t = Threading.Thread(Threading.ThreadStart(run_form))
    t.SetApartmentState(Threading.ApartmentState.STA)
    t.Start()
    t.Join()

    form = form_holder[0]
    if form.output1 is not None:
        OUT = [w.obj for w in form.output1]
    else:
        OUT = [w.obj for w in form.wrapped]

except Exception as e:
    import traceback
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e), traceback.format_exc()
    )