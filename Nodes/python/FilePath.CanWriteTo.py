from System.IO import File, Path, Directory, FileOptions

def tolist(x):
    if hasattr(x,'__iter__'): return x
    return [x]

def getDirectory(p):
	if File.Exists(p):
		return Path.GetDirectoryName(p)
	if Directory.Exists:
		return p
	return

def canWriteToDir(d):
	try:
		with File.Create(Path.Combine(d, "__test_file_name__"),
		1, FileOptions.DeleteOnClose) as f:
			return True
	except:
		return False

paths = tolist(IN[0])
OUT = []
for p in paths:
	d = getDirectory(p)
	if d is not None:
		OUT.append(canWriteToDir(d))
	else:
		OUT.append(False)