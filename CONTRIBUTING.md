# Working on this repository

For the teaching team. Students do not need this file: they need `README.md` and
`SETUP_INSTRUCTIONS.txt`.

## Who does what

Each week has a **responsible TA** who writes the notebook, one or two **contributing TAs** who help
with the content, and two **reviewers** who test the material before release. Writing and reviewing
are deliberately different people: the responsible TA writes, the reviewers run it end to end and
flag unclear instructions, coding errors and unexpected outputs.

| Week | Topic | Responsible | Contributing | Reviewers |
|---|---|---|---|---|
| 1 | Course introduction, basic Python | Konstantin | Riccardo, Jonathan | Giulio, Jonathan |
| 2 | Math refresher and fundamental functions | Giulio, Jonathan | | Nosrat, Benjamin |
| 3 | Probability and descriptive statistics | Giulio | Riccardo, Caroline | Nosrat, Benjamin |
| 4 | Inference I: t-tests and power | Giulio | Konstantin | Caroline, Mael |
| 5 | Inference II: ANOVA and repeated measures | Caroline | Mael | Theo, Konstantin |
| 6 | Non-parametrics, permutation, bootstrap | Theo, Konstantin | Benjamin | Riccardo, Konstantin |
| 7 | Correlation and regression | Riccardo | Giulio, Konstantin | Mael, Giulio |
| 8 | Mixed-effects models | Mael | Theo | Nosrat, Jonathan |
| 9 | Linear algebra fundamentals | Nosrat | Jonathan, Caroline | Theo, Riccardo |
| 10 | Linear algebra for statistics | Nosrat | Caroline | Theo, Riccardo |
| 11 | Principal component analysis | Theo | Nosrat, Riccardo | Benjamin, Konstantin |
| 12 | Time series analysis | Benjamin | Riccardo | Giulio, Caroline |
| 13 | Fourier analysis | Benjamin | Riccardo | Giulio, Caroline |
| 14 | Exam and in-class presentations | | | |


## How review happens

Comments go in as **GitHub issues**, one per notebook, with the points as a checklist. Ticking a box
records progress without writing a comment.

## Notebook conventions

These hold for every week, so that the notebooks feel like one course rather than thirteen.

**Kernel.** `python3` as the name, `qmn` as the display name. Selecting the *registered* `qmn`
kernel in VS Code silently rewrites this on save, so select the conda environment itself.

**Paths.** Never absolute. Every notebook starts with

```python
ROOT = Path.cwd() if (Path.cwd() / "data").is_dir() else Path.cwd().parent
```

and builds paths from `ROOT`, so the notebook runs from the folder it lives in and from the
repository root alike.

**Solutions** are wrapped in two markers, both of them required:

```python
# --- SOLUTION BELOW: TO BE REMOVED IN THE STUDENT VERSION
...
# --- END SOLUTION
```

**Exercises** are boxed, titled `Task N.N` and tagged for difficulty: one star is essential, two
is intermediate, three is an optional challenge.

**Optional concepts** carry a microscope after the section heading, plus one line saying why they
are optional and whether the material comes back later. The rule is strict: nothing that is not
optional may depend on something that is. Check before marking, since a tool used in a later week
cannot be optional however advanced it feels.

## Building what the students get

```
python tools/make_student_versions.py            # every notebook
python tools/make_student_versions.py 01 02      # only these weeks
python tools/make_student_versions.py --audit    # report only, write nothing
```

This removes the solutions, clears every output, and writes `NN_topic_STUDENT.ipynb` next to the
TA version. Run it with `--audit` over the whole repository to see which notebooks have no
solution markers at all, which means they have never been prepared for release.

```
python tools/check_student_versions.py           # every student notebook
```

This checks what would embarrass us: an answer still in the file, an output that gives a task
away, a scaffold emptied by the stripping, a kernel nobody has, an absolute path. A run of
solution lines is only reported when the TA version has it nowhere outside a solution block,
since a repair task is supposed to share its code with its own fix.

```
python tools/build_cheatsheets.py                # the one page handouts, into cheatsheets/
```

