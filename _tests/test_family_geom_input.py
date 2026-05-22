"""
Standalone test for FamilyInstance.ByGeometry input validation logic.
Mocks Dynamo Solid so we can run outside Revit/Dynamo.
"""

# --- Mock Dynamo geometry ---

class Solid:
    def __init__(self, name):
        self.name = name
    def Scale(self, factor):
        return self
    def __repr__(self):
        return f'Solid({self.name})'

class DotNetList:
    """Simulates a .NET ArrayList — iterable but isinstance(x, list) is False."""
    def __init__(self, items):
        self._items = items
    def __iter__(self):
        return iter(self._items)
    def __len__(self):
        return len(self._items)
    def __repr__(self):
        return f'DotNetList({self._items})'

# --- Logic under test (copied from node) ---

def tolist(obj1):
    if hasattr(obj1, '__iter__') and not isinstance(obj1, str):
        return obj1
    return [obj1]

def validate_and_normalise(raw_in0, names):
    """Returns (normalised_list_of_lists, error_string_or_None).
    Uses hasattr(item, 'Scale') to distinguish Dynamo geometry from list containers.
    isinstance(item, list) is NOT reliable in PythonNet3 — Dynamo passes lists as
    .NET ArrayList/IList objects, which fail isinstance(..., list) even though they
    are iterable. Dynamo geometry objects (Solid, Surface, etc.) always have .Scale;
    .NET collection objects do not.
    """
    if hasattr(raw_in0, 'Scale'):
        raw_geom = [raw_in0]
    elif hasattr(raw_in0, '__iter__') and not isinstance(raw_in0, str):
        raw_geom = list(raw_in0)
    else:
        raw_geom = [raw_in0]

    if len(raw_geom) != len(names):
        return None, 'Make sure that each geometry object has a unique family name.'

    normalised = []
    val_error = None
    for item in raw_geom:
        if hasattr(item, 'Scale'):
            normalised.append([item])
        elif hasattr(item, '__iter__') and not isinstance(item, str):
            normalised.append(list(item))
        else:
            val_error = 'Input items should be a solid or list of solids'
            break

    if val_error:
        return None, val_error

    return normalised, None

# --- Test cases ---

s1, s2, s3, s4 = Solid('s1'), Solid('s2'), Solid('s3'), Solid('s4')

PASS = '\033[92mPASS\033[0m'
FAIL = '\033[91mFAIL\033[0m'

def run(desc, in0, names, expect_ok, expect_normalised=None):
    result, err = validate_and_normalise(in0, names)
    if expect_ok:
        if err:
            print(f'{FAIL} [{desc}] unexpected error: {err}')
        elif expect_normalised and result != expect_normalised:
            print(f'{FAIL} [{desc}] wrong normalised output:\n       got {result}\n  expected {expect_normalised}')
        else:
            print(f'{PASS} [{desc}] -> {result}')
    else:
        if err:
            print(f'{PASS} [{desc}] correctly errored: {err}')
        else:
            print(f'{FAIL} [{desc}] should have errored, got: {result}')

print('\n=== Input validation tests ===\n')

run('Single solid, 1 name',
    s1, ['FamA'],
    expect_ok=True,
    expect_normalised=[[s1]])

run('Flat list of 3 solids, 3 names',
    [s1, s2, s3], ['A', 'B', 'C'],
    expect_ok=True,
    expect_normalised=[[s1], [s2], [s3]])

run('List of lists (2 groups), 2 names',
    [[s1, s2], [s3]], ['A', 'B'],
    expect_ok=True,
    expect_normalised=[[s1, s2], [s3]])

run('Mixed: solid + list, 2 names',
    [s1, [s2, s3]], ['A', 'B'],
    expect_ok=True,
    expect_normalised=[[s1], [s2, s3]])

run('Single solid wrapped in list, 1 name',
    [s1], ['FamA'],
    expect_ok=True,
    expect_normalised=[[s1]])

run('Length mismatch: 2 geoms, 1 name',
    [s1, s2], ['A'],
    expect_ok=False)

run('Length mismatch: 1 geom, 2 names',
    s1, ['A', 'B'],
    expect_ok=False)

run('Non-solid scalar',
    [s1, 'not_a_solid'], ['A', 'B'],
    expect_ok=False)

run('.NET list of solids (Dynamo grouped input)',
    DotNetList([DotNetList([s1, s2]), DotNetList([s3])]), ['A', 'B'],
    expect_ok=True,
    expect_normalised=[[s1, s2], [s3]])

run('.NET flat list of 3 solids',
    DotNetList([s1, s2, s3]), ['A', 'B', 'C'],
    expect_ok=True,
    expect_normalised=[[s1], [s2], [s3]])

run('Single solid (not in a list)',
    s1, ['A'],
    expect_ok=True,
    expect_normalised=[[s1]])

print()
