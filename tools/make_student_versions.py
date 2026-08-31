# -*- coding: utf-8 -*-
"""Build the student version of a notebook: solutions removed, outputs cleared.

    python tools/make_student_versions.py                 # every TA notebook
    python tools/make_student_versions.py 01 02 03 04     # only these weeks
    python tools/make_student_versions.py --audit         # report only, write nothing

A solution is everything between the two markers agreed for the course:

    # --- SOLUTION BELOW: TO BE REMOVED IN THE STUDENT VERSION
    ...
    # --- END SOLUTION

Anything before the first marker stays, which is what leaves the students the TODO scaffold with
its blanks. Anything after the closing marker stays too. Outputs are cleared everywhere, so the
students have to run the notebook to see anything, and no expected answer can leak through a
stored figure.

The audit line at the end is the useful part when it is run over the whole repository: a notebook
reported with no markers has never been prepared for release, whatever its issue checklist says.
"""
import io, json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks')
OPEN_MARK = '# --- SOLUTION BELOW: TO BE REMOVED IN THE STUDENT VERSION'
CLOSE_MARK = '# --- END SOLUTION'


def student_name(stem):
    """01_programming_fundamentals_TA -> 01_programming_fundamentals_STUDENT"""
    return re.sub(r'_TA(_[A-Za-z0-9]+)?$', '', stem) + '_STUDENT'


def strip_cell(source):
    """Remove every solution block. Returns the source, how many blocks went, and whether one
    of them had no closing marker, in which case everything to the end of the cell is taken as
    solution. Week 8 does it that way throughout, so this cannot be a hard error."""
    out, removed, inside, unclosed = [], 0, False, False
    for line in source.split('\n'):
        if not inside and line.strip().startswith(OPEN_MARK):
            inside, removed = True, removed + 1
            continue
        if inside:
            if line.strip().startswith(CLOSE_MARK):
                inside = False
            continue
        out.append(line)
    if inside:
        unclosed = True
    while out and not out[-1].strip():
        out.pop()
    return '\n'.join(out), removed, unclosed


def build(path, write=True):
    nb = json.load(io.open(path, encoding='utf-8'))
    blocks, emptied, cleared, unclosed = 0, [], 0, []
    for i, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            if OPEN_MARK in source:
                source, n, open_ended = strip_cell(source)
                blocks += n
                if open_ended:
                    unclosed.append(i)
                if not source.strip():
                    emptied.append(i)
                cell['source'] = source.splitlines(keepends=True)
            if cell.get('outputs'):
                cleared += 1
            cell['outputs'] = []
            cell['execution_count'] = None
        assert 'SOLUTION' not in ''.join(cell['source']), 'cell %d still mentions a solution' % i

    name = os.path.basename(path)[:-6]
    out_path = os.path.join(os.path.dirname(path), student_name(name) + '.ipynb')
    if write:
        io.open(out_path, 'w', encoding='utf-8').write(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
    return blocks, cleared, emptied, unclosed, out_path


args = [a for a in sys.argv[1:] if not a.startswith('--')]
write = '--audit' not in sys.argv

wanted = sorted(f for f in os.listdir(BASE)
                if f.endswith('.ipynb') and '_TA' in f
                and (not args or any(f.startswith(a) for a in args)))

print('%-42s %8s %8s  %s' % ('notebook', 'blocks', 'outputs', 'written'))
unprepared = []
for f in wanted:
    blocks, cleared, emptied, unclosed, out_path = build(os.path.join(BASE, f), write)
    if not blocks:
        unprepared.append(f)
    print('%-42s %8d %8d  %s' % (f, blocks, cleared,
                                 os.path.basename(out_path) if write else 'audit only'))
    for i in emptied:
        print('    warning: cell %d is empty once the solution is gone, it needs a scaffold' % i)
    if unclosed:
        print('    warning: no closing marker in cell%s %s, so the rest of the cell was taken '
              'as solution' % ('' if len(unclosed) == 1 else 's',
                               ', '.join(str(i) for i in unclosed)))

if unprepared:
    print('\nNo solution markers at all, so nothing was removed from these:')
    for f in unprepared:
        print('  ' + f)
