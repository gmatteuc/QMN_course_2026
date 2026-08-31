# -*- coding: utf-8 -*-
"""One page of Python per practical, the sheet Week 1 promises in its closing section.

    python tools/build_cheatsheets.py            # all four
    python tools/build_cheatsheets.py 2          # only Week 2

These are programming references, not summaries of the statistics. Everything on them is syntax or
a code pattern that the week's own cells and exercises use, taken from the notebooks rather than
from a general idea of what a beginner needs. The concepts are the notebook's job.

The page count is checked afterwards. A sheet that spills onto a second page needs cutting.
"""
import io, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'cheatsheets')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LENS = '\U0001f52c'

# Week 1 has the most syntax on it, so it is set a little smaller to stay on one page.
CSS = """
  @page { size: A4; margin: 8mm 8mm 6mm 8mm; }
  body { font-family: "Segoe UI", Calibri, Arial, sans-serif; font-size: %(size).1fpt;
         line-height: %(lead).2f; color: #1a1a1a; margin: 0; }
  h1 { font-size: 13pt; margin: 0; }
  .sub { color: #555; font-size: 7.6pt; margin: 1px 0 5px 0;
         padding-bottom: 3px; border-bottom: 1.4px solid #c8102e; }
  .cols { column-count: 2; column-gap: 6mm; }
  .b { margin: 0 0 5px 0; }
  h2 { font-size: 8.4pt; margin: 0 0 1px 0; color: #c8102e; break-after: avoid; }
  table { break-inside: avoid; }
  pre { orphans: 3; widows: 3; }
  code { font-family: Consolas, "Courier New", monospace; font-size: %(mono).1fpt; }
  pre { font-family: Consolas, "Courier New", monospace; font-size: %(mono).1fpt;
        background: #f5f5f7; border-left: 2px solid #bbb; padding: 3px 5px;
        margin: 2px 0; white-space: pre-wrap; line-height: %(lead).2f;
        orphans: 3; widows: 3; }
  p { margin: 2px 0; }
  .foot { margin-top: 4px; padding-top: 3px; border-top: 1px solid #ddd;
          font-size: 6.8pt; color: #666; }
  table { border-collapse: collapse; width: 100%%; font-size: %(mono).1fpt; }
  td { padding: 0 4px 0 0; vertical-align: top; }
  td.k { font-family: Consolas, monospace; white-space: nowrap; }
"""


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def pre(code):
    return '<pre>%s</pre>' % esc(code.strip('\n'))


def tab(rows):
    return '<table>%s</table>' % ''.join(
        '<tr><td class="k">%s</td><td>%s</td></tr>' % (esc(k), v) for k, v in rows)


def sheet(title, blocks, size=7.6):
    body = '\n'.join('<div class="b"><h2>%s</h2>%s</div>' % (h, c) for h, c in blocks)
    foot = ('Quantitative Methods in Neuroscience, University of Geneva, 2026-27. '
            'Everything here is used somewhere in the Week notebook. ' + LENS +
            ' marks what came from an optional section.')
    css = CSS % {'size': size, 'mono': size - 0.4, 'lead': 1.28 if size >= 7.4 else 1.21}
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>'
            '<h1>%s</h1><div class="sub">%s</div><div class="cols">%s</div>'
            '<div class="foot">%s</div></body></html>'
            % (css, title,
               'Python syntax and code patterns. Keep it next to you while you work.',
               body, foot))


# --------------------------------------------------------------------------- Week 1
W1 = [
 ('Running cells', '<p>A variable exists only once its cell has run. <b>Run All</b> runs them '
  'in order from the top, <b>Restart</b> discards every variable, <b>Clear All Outputs</b> keeps '
  'your code and removes the results. When a notebook misbehaves: Restart, then Run All.</p>'),

 ('Variables and types', pre("""
n_trials = 240           # int
rt = 0.42                # float
cohort = "CSHL-WT"       # str
correct = True           # bool
missing = None           # NoneType

type(rt)                 # <class 'float'>
int("7"), float("0.5"), str(7)   # convert""")),

 ('Arithmetic', tab([
    ('+ - * /', '/ always gives a float'),
    ('//', 'integer division: 7 // 2 is 3'),
    ('%', 'remainder: 7 % 2 is 1'),
    ('**', 'power: 2 ** 3 is 8'),
    ('x += 1', 'shorthand for x = x + 1'),
 ])),

 ('print and f-strings', pre("""
print("value =", rt, type(rt))     # commas add spaces
print(n, end=" ")                  # no new line

f"mean RT {rt:.3f} s"        # 0.420
f"accuracy {acc:.1%}"        # 82.0%
f"{n_trials:,.0f} trials"    # 694,182
f"contrast {c:+.4f}"         # +0.2500
f"{lab:<15} {group:<4} {n}"  # pad left, columns line up
f"{n:>5}"                    # pad right
f"p = {p:.4g}"               # 4 significant digits""")),

 ('Text', pre("""
name = "CSHL" + "_051"
len(name)                    # 8 characters
name.upper(), name.lower()
name.split("_")              # ['CSHL', '051']
"CSHL" in name               # True""")),

 ('Lists', pre("""
rts = [0.31, 0.42, 0.28]
rts[0], rts[-1]              # first, last
rts[0:2]                     # from 0, up to but NOT 2
rts.append(0.55)             # add at the end
rts.sort(); rts.reverse()    # in place, returns nothing
last = rts.pop()             # remove and hand back
len(rts), sum(rts), max(rts), min(rts)
sorted(rts)                  # a sorted copy
0.42 in rts                  # True""")),

 ('Dictionaries', pre("""
mouse = {"id": "CSHL051", "lab": "CSHL"}
mouse["id"]                  # look up by key
mouse["age"] = 14            # add or overwrite
"lab" in mouse               # True
mouse.keys(), mouse.values()

for key, value in mouse.items():
    print(key, value)""")),

 ('Tuples', pre("""
point = (0.25, 0.83)
x, y = point                 # unpacking
key = (lab, group)           # usable as a dict key""")
  + '<p>A tuple cannot be changed after it is built, which is why it can be a key and a list cannot.</p>'),

 ('Conditionals', pre("""
if signed_contrast > 0:
    side = "right"
elif signed_contrast < 0:
    side = "left"
else:
    side = "zero contrast\"""") + tab([
    ('== !=', 'equal, not equal'),
    ('< > <= >=', 'comparisons'),
    ('and or not', 'combine conditions'),
    ('is True, is None', 'identity, used for True and None'),
 ])),

 ('Loops', pre("""
for rt in rts:                    # each item
    print(rt)

for i in range(5):                # 0 1 2 3 4
for n in range(0, 21, 2):         # start, stop, step
for _ in range(100):              # repeat, index unused

for i, rt in enumerate(rts):      # index and item
for lab, grp in zip(labs, groups):  # two lists at once

while trials_left > 0:
    trials_left -= 1

break        # leave the loop now
continue     # skip to the next item""")),

 ('Pattern: count into a dictionary', pre("""
counts = {}
for trial in trials:
    mouse = trial["mouse"]
    if mouse not in counts:
        counts[mouse] = 0
    counts[mouse] += 1

for mouse, n in counts.items():
    print(f"{mouse}: {n} trials")""")),

 ('Pattern: average per group', pre("""
total = {}
n = {}
for i in range(len(labs)):
    lab = labs[i]
    if lab not in total:
        total[lab] = 0
        n[lab] = 0
    total[lab] += ages[i]
    n[lab] += 1

for lab in total:
    print(f"{lab:<12} {total[lab] / n[lab]:.1f} weeks")""")),

 ('Pattern: count with conditions', pre("""
n_correct = 0
n_wrong = 0
for trial in trials:
    if trial["mouse"] != "CSHL046":
        continue                # skip the rest of this turn
    if trial["correct"] is True:
        n_correct += 1
    else:
        n_wrong += 1

accuracy = n_correct / (n_correct + n_wrong)""")),

 ('Reading an error', '<p>Read the <b>last</b> line first: it names the problem.</p>' + tab([
    ('NameError', 'a name never defined, often a typo'),
    ('TypeError', 'an operation between incompatible types'),
    ('IndexError', 'a position that does not exist'),
    ('KeyError', 'a key or column that is not there'),
    ('SyntaxError', 'Python cannot read the line at all'),
    ('IndentationError', 'a block indented inconsistently'),
 ])),

 ('Imports and help', pre("""
help(round)      # the full documentation
round?           # a quick summary, in Jupyter

import math, random
import numpy as np
from pathlib import Path
from src.qmn_utils import sigmoid

math.sqrt(50), math.log(1000), math.pi
random.seed(1); random.choice(rts)
Path.cwd(), Path("data") / "file.csv\"""")),

 ('Files ' + LENS, pre("""
with open("summary.txt", "w") as f:
    for key, value in summary.items():
        f.write(f"{key}: {value}\\n")

with open("summary.txt", "r") as f:
    text = f.read()""") + '<p>"w" overwrites, "a" appends, "r" reads. The file closes itself.</p>'),

 ('A first look at pandas ' + LENS, pre("""
mice = pd.read_csv(path)
mice.head(), mice.shape, mice.info()
mice["lab"]                  # one column
mice["lab"].tolist()         # as a plain list
mice["age"].mean()
mice.iloc[0]                 # by position
mice.loc[0, "lab"]           # by label""")),
]

# --------------------------------------------------------------------------- Week 2
W2 = [
 ('Writing a function', pre("""
def sigmoid(x, slope=1.0, midpoint=0.0):
    \"\"\"One line saying what it does.\"\"\"
    return 1 / (1 + np.exp(-slope * (x - midpoint)))

sigmoid(0.5)                 # defaults used
sigmoid(0.5, slope=4)        # say which one you mean
sigmoid(0.5, 4, 0.1)         # or give them in order

def two_things(x):
    return x.mean(), x.std(ddof=1)

m, s = two_things(values)    # unpack what comes back""")),

 ('Your own module ' + LENS, pre("""
from src.qmn_utils import sigmoid, gaussian

# after editing the .py file, reload it:
import importlib, src.qmn_utils
importlib.reload(src.qmn_utils)""")),

 ('Making arrays', pre("""
np.array([1.0, 2.0, 3.0])
np.linspace(0, 6, 600)       # 600 points, both ends included
np.arange(0, 6, 0.01)        # step 0.01, end excluded
np.zeros(10), np.ones(10)
np.full_like(t, 0.05)        # same shape, one value
x.shape, x.size, len(x)
dt = t[1] - t[0]             # the spacing of a grid""")),

 ('Maths on a whole array', pre("""
y = 2 * x + 1                # every element at once
np.exp(x), np.log(x), np.sqrt(x)
np.sin(x), np.cos(x)
np.abs(x), np.pi, np.e
x.mean(), x.max(), x.min(), x.sum()
x.std(ddof=1)
np.allclose(a, b)            # equal to rounding error""")),

 ('Picking parts out', pre("""
x[0], x[-1], x[10:20]
mask = x > 2                 # array of True and False
x[mask]                      # only where True
x[(x > 0) & (x < 1)]         # brackets, & not "and"
np.argmax(y), np.argmin(y)   # position of the extreme
t[np.argmax(y)]              # where the peak happens
np.abs(x)[error <= 0.02].max()""")),

 ('The shapes of the week', pre("""
y = amp * np.exp(-t / tau)                    # decay
y = np.exp(-(x - mu)**2 / (2 * sigma**2))     # Gaussian
y = 1 / (1 + np.exp(-k * (x - x0)))           # sigmoid
y = amp * np.sin(2 * np.pi * f * t)           # sine""")),

 ('One figure', pre("""
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, y, lw=2, ls="--", color="#d62728",
        label="tau = 1.5 s")
ax.axhline(0, color="gray", lw=0.8)
ax.axvline(x0, color="gray", lw=0.8)
ax.set_xlabel("time (s)")
ax.set_ylabel("amplitude")
ax.set_title("what this panel shows")
ax.set_xlim(0, 2); ax.set_ylim(-1, 1)
ax.legend(frameon=False, loc="lower left")
fig.tight_layout()
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.show()""")),

 ('Other kinds of panel', tab([
    ('ax.scatter(x, y)', 'one dot per observation'),
    ('ax.hist(v, bins=20, alpha=0.7)', 'a distribution'),
    ('ax.bar(names, heights)', 'a value per category'),
    ('ax.errorbar(x, y, yerr=e)', 'value with uncertainty'),
    ('ax.text(x, y, "label")', 'writing on the axes'),
 ])),

 ('Several panels', pre("""
fig, axes = plt.subplots(2, 1, figsize=(9, 5),
                         sharex=True)
axes[0].plot(t, signal); axes[0].set_ylabel("signal")
axes[1].plot(t, rate);   axes[1].set_xlabel("time (s)")
fig.suptitle("one title for both")
fig.tight_layout()""")),

 ('Pattern: one curve per parameter', pre("""
fig, ax = plt.subplots()
for tau in [0.5, 1.5]:
    ax.plot(t, exp_decay(t, tau=tau), lw=2,
            label=f"tau = {tau} s")
ax.legend(frameon=False)""")),

 ('Checking yourself', pre("""
assert abs(a - b) < 1e-12, f"differ at x={value}"
np.allclose(a, b)            # True if equal to rounding

print(f"tau=0.5 gives {f(0.5):.3f}, "
      f"tau=1.5 gives {f(1.5):.3f}")   # one f-string, two lines""")),

 ('Noise', pre("""
rng = np.random.default_rng(7)      # 7 is the seed
noise = rng.normal(0, 0.15, size=t.size)
trace = clean + noise
i0 = np.argmin(np.abs(x))    # index of the value nearest zero""")),

 ('Finding a point, finding peaks', pre("""
above = y >= 0.8             # array of True and False
if above.any():              # ask first: does it ever happen?
    first = np.argmax(above) # position of the first True
    x[first]                 # ... and where that is
# on an all False array argmax returns 0, silently

def smooth(y, w):            # moving average over w points
    pad = w // 2             # repeat the ends, never pad with zeros
    p = np.concatenate([np.full(pad, y[0]), y, np.full(pad, y[-1])])
    return np.convolve(p, np.ones(w) / w, mode="valid")

from scipy.signal import find_peaks
rate = np.gradient(smooth(y, 5), x)   # smooth, then differentiate
peaks, properties = find_peaks(rate, height=0.005, distance=8)
x[peaks], rate[peaks]        # where the peaks are, how tall""")),

 ('Calculus, numerically', pre("""
dy = np.gradient(y, x)       # slope at every point
d2y = np.gradient(dy, x)     # curvature

area = np.trapezoid(y, x)    # np.trapz on older NumPy
running = np.cumsum(y) * dt  # the accumulation
np.diff(y)                   # differences between neighbours""")),

 ('Pattern: repeat an estimate', pre("""
rng = np.random.default_rng(7)

def estimate_many(noise_sd, n_repeats=100):
    estimates = []
    for _ in range(n_repeats):
        t, trace = make_transient(noise_sd, rng)
        estimates.append(recover_tau(t, trace))
    return np.array(estimates)

values = estimate_many(0.10)
print(f"mean {values.mean():.3f}, "
      f"spread {values.std(ddof=1):.3f}")""")),
]

# --------------------------------------------------------------------------- Week 3
W3 = [
 ('Opening a table', pre("""
trials = pd.read_csv(ROOT / "data" / "ibl_2afc.csv.gz")
trials.head()                # first five rows
trials.shape                 # (rows, columns)
trials.info()                # names, types, how many filled
trials.dtypes                # kind of value per column
len(trials)                  # number of rows
trials["rt_s"].describe().round(3).to_string()""")),

 ('Columns', pre("""
trials["rt_s"]               # a Series
trials[["rt_s", "correct"]]  # a smaller DataFrame
trials["fast"] = trials["rt_s"] < 0.5     # a new column
trials["rt_ms"] = trials["rt_s"] * 1000
trials.columns               # all the names""")),

 ('Rows', pre("""
trials.iloc[0]               # by position
trials.iloc[0:5]
trials.loc[0, "rt_s"]        # by label, rows then columns
trials.loc[mask, "rt_s"]     # a column, only those rows""")
  + '<p>Label and position coincide on a freshly loaded table and stop coinciding the moment you filter.</p>'),

 ('Filtering', pre("""
fast = trials[trials["rt_s"] < 0.5]

one = trials[(trials["subject_id"] == "CSHL051")
             & (trials["phase"] == "trained")]

trials[trials["rt_s"].between(0.08, 10.0)]
trials[trials["cohort"].isin(["CSHL-WT", "NYU-WT"])]
trials[~trials["correct"].isna()]""") + tab([
    ('&amp;', 'and, each condition in its own brackets'),
    ('|', 'or'),
    ('~', 'not'),
 ])),

 ('Counting', pre("""
(trials["rt_s"] < 0).sum()   # how many satisfy it
trials["cohort"].value_counts()
trials["subject_id"].unique()
trials["subject_id"].nunique()
trials["rt_s"].isna().sum()  # how many are missing
trials.dropna(subset=["rt_s"])""")),

 ('Joining two tables', pre("""
merged = trials.merge(mice, on="subject_id", how="left")""")
  + '<p>One row per trial, with the columns of that mouse attached to each of its trials.</p>'),

 ('Grouping', pre("""
trials.groupby("cohort")["correct"].mean()

by_phase = trials.groupby("phase")["correct"].agg(
    n="size", accuracy="mean")
by_phase.reset_index()       # the group back as a column

per_mouse = (trials
    .groupby(["cohort", "subject_id"])["rt_s"]
    .median()
    .reset_index())""")),

 ('Out of pandas, into NumPy', pre("""
values = per_mouse["rt_s"].to_numpy()
labs = mice["lab"].tolist()
per_mouse.sort_values("rt_s")
df.head().to_string(index=False)   # printing tidily""")),

 ('Random numbers', pre("""
rng = np.random.default_rng(0)     # 0 is the seed
rng.normal(loc=0, scale=1, size=100)
rng.uniform(0, 1, size=100)
rng.binomial(n=1, p=0.7, size=100)
rng.poisson(lam=3, size=100)
rng.choice(values, size=20, replace=True)""")
  + '<p>The same seed gives the same numbers every run.</p>'),

 ('Summary numbers', pre("""
x.mean(), x.median()
np.std(x, ddof=1), np.var(x, ddof=1)    # always ddof=1
np.percentile(x, [25, 50, 75])
sem = np.std(x, ddof=1) / np.sqrt(len(x))
round(float(value), 3)""")),

 ('Figures with seaborn', pre("""
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(data=df, x="rt_s", bins=40, ax=ax)
sns.boxplot(data=df, x="cohort", y="rt_s", ax=ax,
            order=COHORT_ORDER, width=0.5, fliersize=0)
sns.stripplot(data=df, x="cohort", y="rt_s", ax=ax,
              color="black", size=5)
sns.violinplot(data=df, x="cohort", y="rt_s", ax=ax)
ax.set_ylabel("median RT per mouse (s)")""")
  + '<p>Everything seaborn draws is a Matplotlib figure, so <code>ax.set_xlabel</code> still works.</p>'),

 ('Building a table yourself', pre("""
pd.DataFrame({"n": sizes, "power": curve})
pd.Series(values, name="rt_s")
df.round(3).to_string(index=False)     # print it tidily""")),

 ('Error bars per group', pre("""
summary = (per_mouse.groupby("cohort")["rt_s"]
           .agg(mean="mean", sd="std", n="size")
           .reset_index())
summary["sem"] = summary["sd"] / np.sqrt(summary["n"])

ax.errorbar(summary["cohort"], summary["mean"],
            yerr=summary["sem"], fmt="o", capsize=4)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45)""")),

 ('Pattern: repeat the experiment', pre("""
def sampling_distribution(population, n, repeats, rng):
    means = []
    for _ in range(repeats):
        means.append(rng.choice(population, size=n).mean())
    return np.array(means)

for n in [5, 20, 80, 320]:
    means = sampling_distribution(pop, n, 2000, rng)
    print(f"{n:>5} {means.std(ddof=1):>10.4f}")""")),
]

# --------------------------------------------------------------------------- Week 4
W4 = [
 ('The import', pre("""
from scipy import stats""")),

 ('The three tests', pre("""
# two independent groups, the default choice
stats.ttest_ind(a, b, equal_var=False)      # Welch
stats.ttest_ind(a, b, equal_var=True)       # Student

# the same units measured twice
stats.ttest_rel(before, after)

# one group against a fixed value
stats.ttest_1samp(x, popmean=0.5)
stats.ttest_1samp(x, popmean=0.5,
                  alternative="greater")    # one-sided""")),

 ('Reading the result', pre("""
res = stats.ttest_ind(a, b, equal_var=False)
res.statistic        # t
res.pvalue           # p, two-sided unless you say otherwise
res.df               # degrees of freedom

print(f"t = {res.statistic:.3f}, df = {res.df:.1f}, "
      f"p = {res.pvalue:.4g}")""")),

 ('Deciding', pre("""
decision = "reject" if res.pvalue < alpha else "do not reject"

for null_value in [0.5, 0.55]:
    res = stats.ttest_1samp(x, popmean=null_value)
    print(f"H0 mean = {null_value}: p = {res.pvalue:.4g}")

alpha_corrected = 0.05 / n_tests        # Bonferroni""")),

 ('The statistic by hand', pre("""
n = len(x)
se = np.std(x, ddof=1) / np.sqrt(n)
t = np.mean(x) / se
df = n - 1
p = 2 * stats.t.sf(np.abs(t), df)       # two-sided""")),

 ('Two groups by hand', pre("""
n_a, n_b = len(a), len(b)
pooled_var = ((n_a - 1) * np.var(a, ddof=1)
              + (n_b - 1) * np.var(b, ddof=1)) / (n_a + n_b - 2)
pooled_sd = np.sqrt(pooled_var)
se = pooled_sd * np.sqrt(1 / n_a + 1 / n_b)
t = (np.mean(a) - np.mean(b)) / se
df = n_a + n_b - 2""")),

 ('Effect size and interval', pre("""
d = (np.mean(a) - np.mean(b)) / pooled_sd     # Cohen's d

critical = stats.t.ppf(0.975, df)             # two-sided 95%
margin = critical * se
low, high = difference - margin, difference + margin""")),

 ('The distributions', tab([
    ('stats.t.sf(x, df)', 'upper tail area, double it for two-sided'),
    ('stats.t.ppf(q, df)', 'the inverse, gives critical values'),
    ('stats.t.pdf(x, df)', 'the curve, for plotting'),
    ('stats.norm.sf / ppf / pdf', 'the same for the Normal'),
    ('stats.levene(a, b)', 'do the two spreads differ?'),
 ])),

 ('Pattern: power by simulation', pre("""
def simulate_power(d, n, rng, repeats=2000, alpha=0.05):
    hits = 0
    for _ in range(repeats):
        a = rng.normal(0, 1, size=n)
        b = rng.normal(d, 1, size=n)
        if stats.ttest_ind(a, b, equal_var=False).pvalue < alpha:
            hits += 1
    return hits / repeats

sizes = [10, 20, 30, 40, 60]
curve = []
for n in sizes:
    curve.append(simulate_power(d, n, rng))

enough = []
for n, p in zip(sizes, curve):
    if p >= 0.8:
        enough.append(n)""")),

 ('Pattern: a function returning a report', pre("""
def compare_groups(a, b, alpha=0.05):
    equal = stats.levene(a, b).pvalue >= alpha
    res = stats.ttest_ind(a, b, equal_var=equal)
    low, high = difference_ci(a, b)
    return {"test": "Student" if equal else "Welch",
            "t": round(float(res.statistic), 3),
            "p": round(float(res.pvalue), 4),
            "ci95": (round(float(low), 3),
                     round(float(high), 3))}""")),

 ('Pattern: from table to test', pre("""
valid = trained[trained["rt_s"].between(0.08, 2.0)]
per_mouse = (valid
    .groupby(["cohort", "subject_id"])["rt_s"]
    .median()
    .reset_index())

cshl = per_mouse.loc[per_mouse["cohort"] == "CSHL-WT",
                     "rt_s"].to_numpy()
nyu = per_mouse.loc[per_mouse["cohort"] == "NYU-WT",
                    "rt_s"].to_numpy()
res = stats.ttest_ind(cshl, nyu, equal_var=False)""")
  + '<p>One number per mouse, never one per trial.</p>'),

 ('Pattern: several comparisons', pre("""
comparisons = [("genotype", wt, asd),
               ("laboratory", cshl, nyu),
               ("sex", male, female)]

for name, a, b in comparisons:
    res = stats.ttest_ind(a, b, equal_var=False)
    print(f"{name:<12} t = {res.statistic:6.3f}  "
          f"p = {res.pvalue:.4f}")""")),

 ('Drawing a null distribution', pre("""
fig, ax = plt.subplots()
ax.hist(null_values, bins=40, alpha=0.7)
ax.axvline(observed, color="red", lw=2, label="observed")
ax.legend(frameon=False)

np.isclose(ours, theirs)     # our answer against scipy's""")),

 ('Drawing a power curve', pre("""
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(sizes, curve, "o-", lw=2, ms=6, label="observed d")
ax.axhline(0.8, color="black", lw=1.5, ls="--",
           label="80% power")
ax.set_xlabel("mice per group"); ax.set_ylabel("power")
ax.set_ylim(0, 1); ax.legend(frameon=False)""")),
]

SHEETS = {
 '1': ('Week 1: Python basics', W1, 6.9),
 '2': ('Week 2: functions, arrays, figures, calculus', W2, 7.6),
 '3': ('Week 3: pandas, random numbers, seaborn', W3, 7.6),
 '4': ('Week 4: scipy.stats, tests and simulations', W4, 7.6),
}

if not os.path.isdir(OUT):
    os.makedirs(OUT)

for week in ([a for a in sys.argv[1:] if a in SHEETS] or sorted(SHEETS)):
    title, blocks, size = SHEETS[week]
    html_path = os.path.join(OUT, '_week%s.html' % week)
    pdf_path = os.path.join(OUT, 'QMN_week%s_cheatsheet.pdf' % week)
    io.open(html_path, 'w', encoding='utf-8').write(sheet(title, blocks, size))
    if os.path.exists(pdf_path):
        os.remove(pdf_path)          # Chrome reports success over a stale file
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pdf_path, html_path],
                   check=True, capture_output=True, timeout=180)
    pages = '?'
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(pdf_path).pages)
    except ImportError:
        pass
    flag = '' if pages in (1, '?') else '   <-- too long, cut something'
    print('week %s: %2d blocks, %s page(s), %3.0f kB%s'
          % (week, len(blocks), pages, os.path.getsize(pdf_path) / 1e3, flag))
