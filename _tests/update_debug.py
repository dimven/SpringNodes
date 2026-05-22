import json

path = r'C:\Me\CODE\Github\SpringNodes\Nodes\FamilyInstance.ByGeometry.dyf'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

node = data['Nodes'][0]
code = node['Code']

# The section to replace starts here
marker = 'if len(geom) == len(names) == len(category)'
idx = code.find(marker)
assert idx != -1, 'Dispatch block not found'

keep = code[:idx]

debug = "\r\n".join([
    "def inspect(obj, label='', depth=0):",
    "    pad = '  ' * depth",
    "    lines = []",
    "    t = type(obj)",
    "    lines.append(f'{pad}{label} :: type={t.__module__}.{t.__name__}')",
    "    lines.append(f'{pad}  hasattr Scale={hasattr(obj, \"Scale\")}')",
    "    lines.append(f'{pad}  hasattr __iter__={hasattr(obj, \"__iter__\")}')",
    "    lines.append(f'{pad}  isinstance list={isinstance(obj, list)}')",
    "    lines.append(f'{pad}  isinstance str={isinstance(obj, str)}')",
    "    try:",
    "        lines.append(f'{pad}  len={len(obj)}')",
    "    except Exception as ex:",
    "        lines.append(f'{pad}  len=ERROR:{ex}')",
    "    try:",
    "        lines.append(f'{pad}  repr={repr(obj)[:120]}')",
    "    except Exception as ex:",
    "        lines.append(f'{pad}  repr=ERROR:{ex}')",
    "    if depth < 2 and hasattr(obj, '__iter__') and not isinstance(obj, str):",
    "        try:",
    "            items = list(obj)",
    "            for i, child in enumerate(items[:5]):",
    "                lines.extend(inspect(child, label=f'[{i}]', depth=depth+1).split('\\n'))",
    "            if len(items) > 5:",
    "                lines.append(f'{pad}  ... ({len(items) - 5} more)')",
    "        except Exception as ex:",
    "            lines.append(f'{pad}  iteration ERROR: {ex}')",
    "    return '\\n'.join(lines)",
    "",
    "debug = []",
    "debug.append('=== IN[0] ===')",
    "debug.append(inspect(IN[0]))",
    "debug.append('=== IN[1] fam_path ===')",
    "debug.append(repr(IN[1]))",
    "debug.append('=== IN[2] names raw ===')",
    "debug.append(inspect(IN[2]))",
    "debug.append('=== IN[3] category raw ===')",
    "debug.append(inspect(IN[3]))",
    "debug.append('=== IN[4] material raw ===')",
    "debug.append(inspect(IN[4]))",
    "debug.append('=== IN[5] isVoid raw ===')",
    "debug.append(inspect(IN[5]))",
    "debug.append('=== IN[6] subcat raw ===')",
    "debug.append(inspect(IN[6]))",
    "",
    "OUT = '\\n'.join(debug)",
    "satOpt.Dispose()",
    "opt1.Dispose()",
    "SaveAsOpt.Dispose()",
])

node['Code'] = keep + debug

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done. Code tail:')
print(repr(node['Code'][-200:]))
