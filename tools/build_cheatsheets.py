# -*- coding: utf-8 -*-
"""One page of syntax per practical, the sheet Week 1 promises in its closing section.

    python tools/build_cheatsheets.py            # all four
    python tools/build_cheatsheets.py 2          # only Week 2

Each sheet lists what that week's notebook actually uses, taken from an inventory of the calls in
its cells rather than from a general idea of what a beginner needs. Anything from an optional
section is labelled, so a student who skipped it is not left wondering.

The page count is checked afterwards. A sheet that spills onto a second page is a sheet that needs
cutting, not a bigger sheet.
"""
import io, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'cheatsheets')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

CSS = """
  @page { size: A4; margin: 11mm 10mm 9mm 10mm; }
  body { font-family: "Segoe UI", Calibri, Arial, sans-serif; font-size: 8.4pt;
         line-height: 1.34; color: #1a1a1a; margin: 0; }
  h1 { font-size: 15pt; margin: 0; }
  .sub { color: #555; font-size: 8.4pt; margin: 2px 0 7px 0;
         padding-bottom: 5px; border-bottom: 1.5px solid #c8102e; }
  .cols { column-count: 2; column-gap: 7mm; }
  .b { break-inside: avoid; margin: 0 0 7px 0; }
  h2 { font-size: 9.2pt; margin: 0 0 2px 0; color: #c8102e; }
  code { font-family: Consolas, "Courier New", monospace; font-size: 8pt; }
  pre { font-family: Consolas, "Courier New", monospace; font-size: 7.9pt;
        background: #f5f5f7; border-left: 2px solid #bbb; padding: 4px 6px;
        margin: 3px 0; white-space: pre-wrap; line-height: 1.3; }
  p { margin: 3px 0; }
  ul { margin: 3px 0 3px 13px; padding: 0; }
  li { margin: 1px 0; }
  .opt { color: #666; font-weight: normal; font-size: 8pt; }
  .foot { margin-top: 6px; padding-top: 4px; border-top: 1px solid #ddd;
          font-size: 7.4pt; color: #666; }
  table { border-collapse: collapse; width: 100%; font-size: 7.9pt; }
  td { padding: 1px 4px 1px 0; vertical-align: top; }
  td.k { font-family: Consolas, monospace; white-space: nowrap; width: 38%; }
"""

LENS = '\U0001f52c'


def sheet(title, subtitle, blocks, foot):
    body = '\n'.join(
        '<div class="b"><h2>%s</h2>%s</div>' % (h, c) for h, c in blocks)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>'
            '<h1>%s</h1><div class="sub">%s</div><div class="cols">%s</div>'
            '<div class="foot">%s</div></body></html>' % (CSS, title, subtitle, body, foot))


def table(rows):
    return '<table>%s</table>' % ''.join(
        '<tr><td class="k">%s</td><td>%s</td></tr>' % (k, v) for k, v in rows)


FOOT = ('Quantitative Methods in Neuroscience, Master in Neuroscience, University of Geneva, '
        '2026-27. Sections marked ' + LENS + ' were optional in the notebook.')

# --------------------------------------------------------------------------- Week 1
W1 = [
 ('Running a notebook', table([
    ('Run cell', 'the play button on the left of the cell'),
    ('Run All', 'runs every cell from the top, in order'),
    ('Restart', 'throws away every variable the kernel holds'),
    ('Clear All Outputs', 'removes results and figures, keeps your code'),
 ]) + '<p>A variable exists only once its cell has been run. If a notebook behaves strangely, '
      '<b>Restart</b> then <b>Run All</b>.</p>'),
 ('Variables and types', '<pre>n_trials = 240        # int\nrt = 0.42            # float\nname = "CSHL-WT"     # str\nis_correct = True    # bool, a truth value\nnothing = None       # NoneType\n\ntype(rt)             # ask what something is</pre>'),
 ('Arithmetic', table([
    ('+ - * /', 'the usual, / always gives a float'),
    ('//', 'integer division, 7 // 2 is 3'),
    ('%', 'remainder, 7 % 2 is 1'),
    ('**', 'power, 2 ** 3 is 8'),
 ])),
 ('Text and f-strings', '<pre>label = "mouse " + "CSHL_001"\nf"accuracy {acc:.2f}"      # two decimals\nf"{n} trials"\nlen(name)                  # how many characters\nname.upper(), name.split("-")</pre>'),
 ('Lists', '<pre>rts = [0.31, 0.42, 0.28]\nrts[0]        # first, counting starts at 0\nrts[-1]       # last\nrts[0:2]      # from 0 up to but not including 2\nrts.append(0.55)\nlen(rts), sum(rts), sorted(rts)\n0.42 in rts   # True or False</pre>'),
 ('Dictionaries', '<pre>mouse = {"id": "CSHL_001", "lab": "CSHL"}\nmouse["id"]                # look up by key\nmouse["age_weeks"] = 14    # add a new one\nmouse.keys(), mouse.values()\nfor key, value in mouse.items():\n    print(key, value)</pre>'),
 ('Tuples', '<pre>point = (0.25, 0.83)\nx, y = point          # unpacking\n</pre><p>A tuple cannot be changed after it is made, which is why it can be a dictionary key and a list cannot.</p>'),
 ('Conditionals', '<pre>if contrast == 0:\n    print("guess")\nelif contrast &lt; 0.25:\n    print("hard")\nelse:\n    print("easy")</pre>' + table([
    ('== !=', 'equal, not equal'),
    ('&lt; &gt; &lt;= &gt;=', 'comparisons'),
    ('and or not', 'combine conditions'),
 ])),
 ('Loops', '<pre>for rt in rts:\n    print(rt)\n\nfor i in range(5):          # 0 1 2 3 4\n    print(i)\n\nfor i, rt in enumerate(rts):    # index and value\n    print(i, rt)\n\nfor a, b in zip(labs, groups):  # two lists at once\n    print(a, b)\n\nwhile trials_left &gt; 0:\n    trials_left = trials_left - 1</pre>'),
 ('Reading an error', '<p>Read the <b>last</b> line first: it names the problem.</p>' + table([
    ('NameError', 'a name that was never defined, often a typo'),
    ('TypeError', 'an operation between incompatible types'),
    ('IndexError', 'a position that does not exist'),
    ('KeyError', 'a dictionary or column key that is not there'),
    ('SyntaxError', 'Python cannot even read the line'),
    ('IndentationError', 'a block is not indented consistently'),
 ])),
 ('Getting help', '<pre>help(round)      # the full documentation\nround?           # a quick summary, in Jupyter</pre>'
  '<p>And the official docs: docs.python.org, numpy.org, pandas.pydata.org.</p>'),
 ('Imports', '<pre>import numpy as np\nimport pandas as pd\nfrom pathlib import Path</pre>'
  '<p>A <b>module</b> is one file of Python, a <b>library</b> is a collection of them.</p>'),
 ('Files ' + LENS, '<pre>with open("report.txt", "w") as f:\n    f.write("one line\\n")\n\nwith open("report.txt") as f:\n    text = f.read()</pre>'),
 ('A first look at pandas ' + LENS, '<pre>mice = pd.read_csv(path)\nmice.head()        # the first five rows\nmice.shape         # (rows, columns)\nmice.info()        # column names and types\nmice["lab"]        # one column\nmice.iloc[0]       # by position\nmice.loc[0, "lab"] # by label</pre><p>Week 3 starts again from the beginning.</p>'),
]

# --------------------------------------------------------------------------- Week 2
W2 = [
 ('Writing a function', '<pre>def sigmoid(x, slope=1.0, midpoint=0.0):\n    """One line saying what it does."""\n    return 1 / (1 + np.exp(-slope * (x - midpoint)))\n\nsigmoid(0.5)                  # slope and midpoint default\nsigmoid(0.5, slope=4)         # or say which you mean</pre>'),
 ('Your own module ' + LENS, '<pre>from src.qmn_utils import sigmoid</pre>'
  '<p>Helpers live in a <code>.py</code> file so that two notebooks cannot end up with two versions of the same function.</p>'),
 ('Making arrays', '<pre>np.array([1.0, 2.0, 3.0])\nnp.linspace(0, 6, 600)   # 600 points, ends included\nnp.arange(0, 6, 0.01)    # step of 0.01, end excluded\nx.shape, x.size</pre>'),
 ('Arithmetic without loops', '<pre>y = 2 * x + 1        # every element at once\nnp.exp(x), np.log(x), np.sqrt(x)\nnp.sin(x), np.cos(x), np.pi, np.e\nnp.abs(x), x.max(), x.mean()</pre>'),
 ('Picking parts out', '<pre>x[0], x[-1], x[10:20]\nmask = x &gt; 2          # an array of True and False\nx[mask]               # only where it is True\nnp.argmax(y)          # position of the largest value\n</pre>'),
 ('The functions of the week', table([
    ('exponential decay', 'y = A * np.exp(-t / tau)'),
    ('Gaussian', 'y = np.exp(-(x - mu)**2 / (2 * sigma**2))'),
    ('sigmoid', 'y = 1 / (1 + np.exp(-k * (x - x0)))'),
    ('sine', 'y = A * np.sin(2 * np.pi * f * t)'),
 ])),
 ('Anatomy of a figure', '<pre>fig, ax = plt.subplots(figsize=(6, 4))\nax.plot(x, y, lw=1.5, label="signal")\nax.set_xlabel("time (s)")\nax.set_ylabel("amplitude")\nax.set_title("what this panel shows")\nax.legend()\nfig.tight_layout()\nplt.show()</pre>'),
 ('Other kinds of panel', table([
    ('ax.scatter(x, y)', 'one dot per observation'),
    ('ax.hist(v, bins=30)', 'a distribution'),
    ('ax.bar(names, heights)', 'a value per category'),
    ('ax.errorbar(x, y, yerr=e)', 'a value with its uncertainty'),
    ('ax.axhline(0), ax.axvline(0)', 'a reference line'),
 ])),
 ('Several panels, and saving', '<pre>fig, axes = plt.subplots(2, 1, figsize=(8, 5),\n                         sharex=True)\naxes[0].plot(t, signal)\naxes[1].plot(t, rate)\nfig.savefig("figure.png", dpi=200,\n            bbox_inches="tight")</pre>'),
 ('Derivatives, numerically', '<pre>dy = np.gradient(y, x)        # slope at every point\nd2y = np.gradient(dy, x)      # curvature</pre>'
  '<p>Positive slope rising, zero at a peak or a trough, and the second derivative says which of the two.</p>'),
 ('Integrals, numerically', '<pre>area = np.trapezoid(y, x)     # the total\nrunning = np.cumsum(y) * dx   # the accumulation</pre>'
  '<p>On older NumPy the first one is called <code>np.trapz</code>.</p>'),
 ('Measuring a decay', '<pre>level = baseline + (peak - baseline) / np.e\n# tau is the time from the peak to that level</pre>'
  '<p>The <b>1/e rule</b>: after one time constant, a decay has fallen to about 37% of the way from baseline to peak.</p>'),
]

# --------------------------------------------------------------------------- Week 3
W3 = [
 ('Opening a table', '<pre>trials = pd.read_csv(ROOT / "data" / "ibl_2afc.csv.gz")\ntrials.head()      # the first five rows\ntrials.shape       # (rows, columns)\ntrials.info()      # names, types, how many are filled\ntrials.dtypes      # what kind of values each holds\ntrials["rt_s"].describe()</pre>'),
 ('Columns', '<pre>trials["rt_s"]              # a Series, one column\ntrials[["rt_s", "correct"]] # a smaller DataFrame\ntrials["fast"] = trials["rt_s"] &lt; 0.5   # a new one</pre>'
  '<p>The double brackets are a list of names, not a typo.</p>'),
 ('Rows', '<pre>trials.iloc[0]         # by position, like a list\ntrials.loc[0, "rt_s"]  # by label, the index value</pre>'
  '<p>The two coincide on a freshly loaded table and stop coinciding the moment you filter.</p>'),
 ('Filtering', '<pre>fast = trials[trials["rt_s"] &lt; 0.5]\nboth = trials[(trials["rt_s"] &lt; 0.5)\n              &amp; (trials["correct"] == 1)]</pre>' + table([
    ('&amp;', 'and, with brackets around each condition'),
    ('|', 'or'),
    ('~', 'not'),
 ])),
 ('Missing values', '<pre>trials["rt_s"].isna().sum()   # how many are missing\ntrials.dropna(subset=["rt_s"])</pre>'
  '<p>Most calculations skip them silently, so count them before trusting an average.</p>'),
 ('Joining two tables', '<pre>merged = trials.merge(mice, on="subject_id",\n                      how="left")</pre>'
  '<p>One row per trial, with the columns of the mouse attached to each of its trials.</p>'),
 ('Grouping', '<pre>trials.groupby("cohort")["correct"].mean()\n\ntrials.groupby("subject_id").agg(\n    accuracy=("correct", "mean"),\n    n=("correct", "count"),\n).reset_index()</pre>'
  '<p>Split into groups, compute per group, put the result back together.</p>'),
 ('Random numbers', '<pre>rng = np.random.default_rng(0)   # 0 is the seed\nrng.normal(loc=0, scale=1, size=100)\nrng.uniform(0, 1, size=100)\nrng.binomial(n=1, p=0.7, size=100)\nrng.choice(values, size=10, replace=True)</pre>'
  '<p>The same seed gives the same numbers, which is what makes a result reproducible.</p>'),
 ('Centre and spread', table([
    ('x.mean()', 'pulled by outliers and by a long tail'),
    ('x.median()', 'the middle value, barely moved by them'),
    ('np.std(x, ddof=1)', 'spread of the data, the n - 1 version'),
    ('np.percentile(x, [25, 75])', 'the quartiles'),
 ]) + '<p>Always <code>ddof=1</code> on a sample.</p>'),
 ('SD against SEM', '<pre>sem = np.std(x, ddof=1) / np.sqrt(len(x))</pre>'
  '<p>The <b>SD</b> says how spread out the observations are and does not shrink with more data. '
  'The <b>SEM</b> says how precisely you know the mean and shrinks as the square root of n. '
  'Error bars mean nothing until you say which one they are.</p>'),
 ('Distributions in one line', '<pre>sns.histplot(data=df, x="rt_s", ax=ax)\nsns.violinplot(data=df, x="cohort", y="rt_s", ax=ax)\nsns.boxplot(data=df, x="cohort", y="rt_s", ax=ax)\nsns.stripplot(data=df, x="cohort", y="rt_s", ax=ax)</pre>'
  '<p>Everything seaborn draws is a Matplotlib figure, so <code>ax.set_xlabel</code> still works.</p>'),
 ('The two results of the week', '<p><b>Law of large numbers.</b> As n grows, the sample mean settles onto the true mean.</p>'
  '<p><b>Central limit theorem.</b> Whatever the shape of the data, the distribution of the '
  '<i>mean</i> over repeated samples becomes Normal, with spread SD/&#8730;n.</p>'),
]

# --------------------------------------------------------------------------- Week 4
W4 = [
 ('The words', table([
    ('H&#8320;', 'the null: there is no effect'),
    ('H&#8321;', 'the alternative: there is one'),
    ('&#945;', 'the risk of a false alarm you accept, usually 0.05'),
    ('p-value', 'how often chance alone would give a result this extreme, <i>if</i> H&#8320; were true'),
    ('type I', 'rejecting a true null, a false alarm'),
    ('type II', 'missing a real effect'),
    ('power', '1 minus type II, the chance of finding a real effect'),
 ])),
 ('What a p-value is not', '<p>It is not the probability that the null is true, and not the size of the effect. '
  'A small p from a small sample says "worth a second look", not "settled".</p>'),
 ('The three tests', '<pre>from scipy import stats\n\n# two independent groups, the default choice\nstats.ttest_ind(a, b, equal_var=False)   # Welch\n\n# the same subjects measured twice\nstats.ttest_rel(before, after)\n\n# one group against a fixed value\nstats.ttest_1samp(x, popmean=0.5)</pre>'
  '<p>Each returns the statistic and the p-value, two-sided.</p>'),
 ('The statistic', '<p>A difference, divided by how much a difference of that size wanders by chance:</p>'
  '<pre>t = (mean_a - mean_b) / standard_error</pre>'
  '<p>Bigger sample, smaller standard error, larger t for the same difference.</p>'),
 ('Assumptions', '<ul><li><b>Independence.</b> One number per mouse, never one per trial.</li>'
  '<li><b>Normality</b> of the quantity being averaged, or a sample large enough for the CLT.</li>'
  '<li><b>Equal variance</b> for the pooled version. Welch does not need it, which is why it is the default.</li></ul>'
  '<pre>stats.levene(a, b)   # do the two spreads differ?</pre>'),
 ('Effect size', '<pre>sd_pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb)\n                    / (na + nb - 2))\nd = (mean_a - mean_b) / sd_pooled</pre>'
  '<p>Cohen\'s d is the difference in standard deviations, so it does not grow with the sample the way t does. '
  'Roughly: 0.2 small, 0.5 medium, 0.8 large.</p>'),
 ('Confidence interval', '<pre>t_crit = stats.t.ppf(0.975, df)\nlow  = diff - t_crit * se\nhigh = diff + t_crit * se</pre>'
  '<p>The range of differences the data do not rule out. It says more than a p-value, because its width shows how much doubt is left.</p>'),
 ('Distributions by hand', table([
    ('stats.t.sf(x, df)', 'area in the upper tail, double it for two-sided'),
    ('stats.t.ppf(q, df)', 'the inverse, where critical values come from'),
    ('stats.t.pdf(x, df)', 'the curve itself, for plotting'),
    ('stats.norm', 'the same three, for the Normal'),
 ])),
 ('Power, by simulation', '<pre>hits = 0\nfor _ in range(2000):\n    a = rng.normal(mu_a, sd, size=n)\n    b = rng.normal(mu_b, sd, size=n)\n    if stats.ttest_ind(a, b, equal_var=False).pvalue &lt; 0.05:\n        hits = hits + 1\npower = hits / 2000</pre>'
  '<p>No formula to remember: invent the experiment many times and count how often it works.</p>'),
 ('Several tests at once', '<p>Run m tests at &#945; = 0.05 and the chance of at least one false alarm is far above 5%. '
  'The blunt fix is <b>Bonferroni</b>: compare each p against &#945; / m, and say in the text how many tests you ran.</p>'),
 ('Reporting a comparison', '<ul><li>the design, and what one observation is</li>'
  '<li>the sample size in each group</li><li>the null, and one-sided or two-sided</li>'
  '<li>which test, and why that one</li><li>the statistic, the degrees of freedom, the p-value</li>'
  '<li>the effect size and a confidence interval</li>'
  '<li>one sentence of plain language saying what it means</li></ul>'),
]

SHEETS = {
 '1': ('Week 1 cheat sheet: Python basics', W1),
 '2': ('Week 2 cheat sheet: functions, arrays, figures, calculus', W2),
 '3': ('Week 3 cheat sheet: pandas and describing data', W3),
 '4': ('Week 4 cheat sheet: tests, effect size and power', W4),
}

SUB = 'Quantitative Methods in Neuroscience, 2026-27. Keep it next to you while you work.'

if not os.path.isdir(OUT):
    os.makedirs(OUT)

wanted = [a for a in sys.argv[1:] if a in SHEETS] or sorted(SHEETS)
for week in wanted:
    title, blocks = SHEETS[week]
    html_path = os.path.join(OUT, '_week%s.html' % week)
    pdf_path = os.path.join(OUT, 'QMN_week%s_cheatsheet.pdf' % week)
    io.open(html_path, 'w', encoding='utf-8').write(sheet(title, SUB, blocks, FOOT))
    if os.path.exists(pdf_path):
        os.remove(pdf_path)          # Chrome happily reports success over a stale file
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pdf_path, html_path],
                   check=True, capture_output=True, timeout=180)
    pages = '?'
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(pdf_path).pages)
    except ImportError:
        pass
    flag = '' if pages in (1, '?') else '   <-- too long, needs cutting'
    print('week %s: %d blocks, %s page(s), %.0f kB%s'
          % (week, len(blocks), pages, os.path.getsize(pdf_path) / 1e3, flag))
