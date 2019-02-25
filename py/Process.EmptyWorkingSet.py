import System
from System.Diagnostics import Process

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append('%s\IronPython 2.7\Lib' %pf_path)
import ctypes

#flush = ctypes.windll.psapi.EmptyWorkingSet #before Windows 7
flush = ctypes.windll.kernel32.K32EmptyWorkingSet
try_flush = flush(Process.GetCurrentProcess().Handle)
OUT = try_flush != 0