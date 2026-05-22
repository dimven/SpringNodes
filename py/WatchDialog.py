#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2020, Dimitar Venkov       #
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


import sys
import clr

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import System
from System.Windows.Forms import Application, Form, RichTextBox, RichTextBoxScrollBars, AnchorStyles
from System.Drawing import Point, Color, Font
from io import StringIO
import traceback

import ctypes
DWMWA_USE_IMMERSIVE_DARK_MODE = 20


str_file = StringIO()
size1 = [30, 23]  # height, width

def tolist(obj1):
    return obj1 if isinstance(obj1, list) else [obj1]

def write_str(str1, GCL, str_file=str_file, size1=size1):
    ln1 = len(str1)
    if ln1 > size1[1]:
        size1[1] = ln1
    str_file.write("%s%s\n" % ("".join([x for x in GCL if x]), str1))

def safe_type_name(x):
    try:
        return x.GetType().ToString()
    except AttributeError:
        return type(x).__name__

def safe_to_string(x):
    try:
        return x.ToString()
    except AttributeError:
        return str(x)

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

        if hasattr(x, "Id"):
            write_str("%s        %i" % (x.ToString(), x.Id), GCL)
        elif isinstance(x, list):
            if not x:
                write_str("Empty List", GCL)
            else:
                list2str(x, writeInd, GCL, GCint, size1)
        elif "Dictionary" in safe_type_name(x):
            d = x.Components()
            k, v = d["keys"], d["values"]
            list2str(dict(zip(k, v)), writeInd, GCL, GCint, size1, True)
        elif x is None:
            write_str("null", GCL)
        else:
            write_str(safe_to_string(x), GCL)

        size1[0] += 19

    GCL.pop(GCint)
    GCint -= 1


class WatchBox(Form):
    def __init__(self, t1):
        super().__init__()  # REQUIRED in PythonNet3
        self.Load += self.on_load
        self.Text = "SpringNodes: Watch Window"
        self.BackColor = Color.FromArgb(40, 40, 40)
        self.ControlBox = True
        self.TopMost = True
        self.Width = 800
        self.Height = 600

        self.box1 = RichTextBox()
        self.box1.Multiline = True
        self.box1.Location = Point(5, 5)
        self.box1.Font = Font("Arial", 12)
        self.box1.BackColor = Color.FromArgb(53, 53, 53)
        self.box1.ForeColor = Color.FromArgb(234, 234, 234)
        self.box1.DetectUrls = True
        self.box1.WordWrap = False
        self.box1.Text = t1
        self.box1.Width = self.ClientSize.Width - 10
        self.box1.Height = self.ClientSize.Height - 10
        self.box1.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self.Controls.Add(self.box1)

    def on_load(self, sender, event):
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            int(self.Handle.ToInt64()),
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
        ctypes.windll.uxtheme.SetWindowTheme(
            int(self.box1.Handle.ToInt64()),
            "DarkMode_Explorer",
            None
        )


try:
    l1 = [] if IN[0] is None else tolist(IN[0])
    list2str(l1, IN[1])
    str_content = str_file.getvalue()
    str_file.close()

    form = WatchBox(str_content)
    # form.FormClosing += on_close  # removed: on_close was undefined

    Application.Run(form)
    OUT = str_content

except Exception as e:
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e),
        traceback.format_exc()
    )