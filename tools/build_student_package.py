# -*- coding: utf-8 -*-
"""Assemble the zip a student receives: notebooks, data, guide, environment, cheat sheets.

    python tools/build_student_package.py

Writes QMN_practicals_1to4.zip next to the repository. It contains only what Weeks 1 to 4 need,
so the EEG datasets of Weeks 10 to 13, 74 MB of them, stay out.

The notebooks go in under their plain names. The _STUDENT suffix exists to tell them apart from
the TA copies inside our repository, and it means nothing to a student.
"""
import io, os, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, 'notebooks')
OUT = os.path.join(ROOT, 'QMN_practicals_1to4')
ZIP = OUT + '.zip'

WEEKS = ['01_programming_fundamentals', '02_math_refresher',
         '03_probability_descriptive', '04_inference_ttests_power']

README = """QMN practicals 1 to 4
Quantitative Methods in Neuroscience, Master in Neuroscience, University of Geneva, 2026-27

WHAT TO DO BEFORE THE FIRST PRACTICAL

1. Unzip this folder somewhere you will find it again, for example your Documents folder.
   Keep it together: the notebooks look for the data next to themselves.

2. Set up Python. Follow QMN_setup_guide_students.pdf, which has screenshots, or
   SETUP_INSTRUCTIONS.txt, which is the same thing as text. It takes about thirty minutes
   and you only do it once. You will use environment.yml, which is in this folder.

3. Check it worked. With the qmn environment active, from this folder:

       python notebooks/src/check_env.py

   It prints one line per package and one per dataset. The two EEG files are meant to say
   "later": they belong to Weeks 10 to 13 and are handed out then.

4. Open notebooks/01_programming_fundamentals.ipynb in VS Code, choose the qmn environment
   as the kernel, and start reading. Everything is explained in the notebook itself.

WHAT IS IN HERE

   notebooks/            the four practicals, and the data and images they use
   cheatsheets/          one page of syntax per week, to keep beside you while you work
   QMN_setup_guide_students.pdf    the illustrated install guide
   SETUP_INSTRUCTIONS.txt          the same, as text
   environment.yml                 the list of packages, used in step 2

HOW TO READ A NOTEBOOK

   Markdown cells explain the idea, code cells do it. Task boxes are the exercises, tagged
   one to three stars by difficulty. Sections marked with a microscope go further than the
   course requires and can be skipped.

   Some cells are broken on purpose and say so: running them and reading the error is the
   exercise.

IF YOU GET STUCK

   Bring it to the practical, that is what the sessions are for. If you want to try before
   then, giulio.matteucci@unige.ch.
"""


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


if os.path.isdir(OUT):
    shutil.rmtree(OUT)
if os.path.exists(ZIP):
    os.remove(ZIP)

for week in WEEKS:
    copy(os.path.join(NB, week + '_STUDENT.ipynb'),
         os.path.join(OUT, 'notebooks', week + '.ipynb'))

for name in ['ibl_2afc.csv.gz', 'ibl_2afc_subjects.csv', 'ibl_2afc_datadictionary.md']:
    copy(os.path.join(NB, 'data', name), os.path.join(OUT, 'notebooks', 'data', name))

for folder in ['01', '02', '03']:
    source = os.path.join(NB, 'assets', folder)
    for name in os.listdir(source):
        copy(os.path.join(source, name), os.path.join(OUT, 'notebooks', 'assets', folder, name))

for name in ['__init__.py', 'qmn_utils.py', 'check_env.py']:
    copy(os.path.join(NB, 'src', name), os.path.join(OUT, 'notebooks', 'src', name))

for week in '1234':
    copy(os.path.join(ROOT, 'cheatsheets', 'QMN_week%s_cheatsheet.pdf' % week),
         os.path.join(OUT, 'cheatsheets', 'QMN_week%s_cheatsheet.pdf' % week))

for name in ['QMN_setup_guide_students.pdf', 'SETUP_INSTRUCTIONS.txt', 'environment.yml']:
    copy(os.path.join(ROOT, name), os.path.join(OUT, name))

io.open(os.path.join(OUT, 'README.txt'), 'w', encoding='utf-8', newline='\r\n').write(README)

with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for folder, _, files in os.walk(OUT):
        for name in sorted(files):
            full = os.path.join(folder, name)
            z.write(full, os.path.relpath(full, os.path.dirname(OUT)))

total = sum(os.path.getsize(os.path.join(f, n)) for f, _, fs in os.walk(OUT) for n in fs)
print('%s' % ZIP)
print('  %d files, %.1f MB unpacked, %.1f MB zipped'
      % (sum(len(fs) for _, _, fs in os.walk(OUT)), total / 1e6, os.path.getsize(ZIP) / 1e6))
