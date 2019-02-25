import System

dataKey, data = IN
System.AppDomain.CurrentDomain.SetData("_Dyn_Wireless_%s" % dataKey, data)