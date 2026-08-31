# -*- coding: utf-8 -*-
"""Is a student version actually fit to hand out?

    python tools/check_student_versions.py            # every one that exists

Checks the things that would embarrass us if they were wrong: an answer left in the file, an
output that gives a task away, a scaffold that was emptied by the stripping, a kernel nobody has,
a path that only works on one machine. It does not run the notebooks; make_student_versions and
the usual execution check do that.
"""
import io, json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks')
ANSWER = re.compile(r'SOLUTION|# Then answer here.*\n\s*#\s*\w', re.I)

problems = 0
names = sorted(f for f in os.listdir(BASE) if f.endswith('_STUDENT.ipynb'))
if len(sys.argv) > 1:
    names = [f for f in names if any(f.startswith(a) for a in sys.argv[1:])]

for name in names:
    path = os.path.join(BASE, name)
    nb = json.load(io.open(path, encoding='utf-8'))
    cells = nb['cells']
    text = '\n'.join(''.join(c['source']) for c in cells)
    code = [(i, ''.join(c['source'])) for i, c in enumerate(cells) if c['cell_type'] == 'code']

    ta_path = os.path.join(BASE, name.replace('_STUDENT', '_TA'))
    ta = json.load(io.open(ta_path, encoding='utf-8')) if os.path.exists(ta_path) else None

    said, notes = [], []
    if 'SOLUTION' in text:
        said.append('the word SOLUTION is still in the file')
    with_outputs = [i for i, c in enumerate(cells) if c['cell_type'] == 'code' and c.get('outputs')]
    if with_outputs:
        said.append('cells still carrying an output: %s' % with_outputs)
    ks = nb['metadata'].get('kernelspec', {})
    if (ks.get('name'), ks.get('display_name')) != ('python3', 'qmn'):
        said.append('kernel is %s / %s' % (ks.get('name'), ks.get('display_name')))
    empty = [i for i, s in code if not s.strip()]
    if empty:
        said.append('empty code cells, the scaffold went with the solution: %s' % empty)

    # A task may legitimately have two TODO cells, as Week 1's pair of broken snippets does, and
    # one task asks the student to make the cell themselves. So a TODO with no task box is a
    # problem, while a task with no TODO is only worth a note.
    todos = set(re.findall(r'# TODO (\d+\.\d+)', text))
    tasks = set(re.findall(r'Task (\d+\.\d+) ⭐', text))
    if todos - tasks:
        said.append('TODO cells with no task box: %s' % sorted(todos - tasks))
    if tasks - todos:
        notes.append('no TODO cell for task %s, which should be the one asking for a new cell'
                     % ', '.join(sorted(tasks - todos)))

    absolute = [i for i, s in code if re.search(r'[A-Z]:\\|/Users/|/home/', s)]
    if absolute:
        said.append('absolute paths in cells %s' % absolute)

    if ta is not None:
        ta_code = sum(1 for c in ta['cells'] if c['cell_type'] == 'code')
        if ta_code != len(code) or len(ta['cells']) != len(cells):
            said.append('cell counts differ from the TA version, %d vs %d'
                        % (len(cells), len(ta['cells'])))
        # Shared lines prove nothing on their own. A repair task hands the student the broken
        # code and the fix differs by one argument, so whole runs of plotting boilerplate are
        # meant to coincide. A run is only evidence of a leak if the TA version has it *nowhere
        # except* inside a solution block.
        ta_text = '\n'.join(''.join(c['source']) for c in ta['cells'])
        ta_outside = re.sub(r'# --- SOLUTION BELOW.*?# --- END SOLUTION', '', ta_text, flags=re.S)
        ta_outside = '\n'.join(l.strip() for l in ta_outside.split('\n')
                               if l.strip() and not l.strip().startswith('#'))
        student_code = '\n'.join(l.strip() for _, s in code for l in s.split('\n')
                                 if l.strip() and not l.strip().startswith('#'))
        leak = None
        for block in re.findall(r'# --- SOLUTION BELOW.*?# --- END SOLUTION', ta_text, re.S):
            body = [l.strip() for l in block.split('\n')[1:-1]
                    if l.strip() and not l.strip().startswith('#')]
            for start in range(max(0, len(body) - 2)):
                run = '\n'.join(body[start:start + 3])
                if len(run) > 60 and run in student_code and run not in ta_outside:
                    leak = run
                    break
            if leak:
                break
        if leak:
            said.append('a run of solution lines the TA version has nowhere else: %r' % leak[:70])

    print('%-46s %s' % (name, 'ready' if not said else 'PROBLEMS'))
    for s in said:
        print('    ' + s)
    for s in notes:
        print('    note: ' + s)
    problems += len(said)

print()
print('%d problem(s) across %d student notebook(s)' % (problems, len(names)))
