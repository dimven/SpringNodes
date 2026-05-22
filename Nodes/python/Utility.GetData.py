import System

dataKey, _ = IN
OUT = System.AppDomain.CurrentDomain.GetData("_Dyn_Wireless_%s" % dataKey)