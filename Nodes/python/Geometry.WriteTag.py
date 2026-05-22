geo, par, val,override = IN
setPreviously = False
try:
	tags = geo.Tags
	if tags.LookupTag(par) is None or override:
		tags.AddTag(par, val)
except ValueError:
	setPreviously = True
OUT = IN[0], setPreviously