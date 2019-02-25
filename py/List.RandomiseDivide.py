import System
pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append('%s\IronPython 2.7\Lib' %pf_path)
import random

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

l1, rat, seed = IN
l1 = tolist(l1)
r = random.Random()
r.seed(seed)
r.shuffle(l1)
len1 = len(l1)
OUT = []
if len(rat) < 2:
	rat.append(1.0 - rat[0])
if sum(rat) < 1.0:
	rat.append(1.0 - sum(rat) )
start, end = 0, int(round(rat[0] * len1) )
len2 = len(rat)
for i in xrange(len2):
	OUT.append(l1[start : end])
	start = end
	j = (i + 1) % len2
	end += int(round(rat[j] * len1) )
if not OUT[-1]:
	del(OUT[-1])