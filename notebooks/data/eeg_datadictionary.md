# Data dictionary for the course EEG bundle

## What is in the bundle

Two independent public EEG datasets, repackaged into **one common format** so
that both load with a single `np.load` and no EEG library.

| File | Size | Contents |
|---|---|---|
| `alphawaves.npz` | 24 MB | EEG Alpha Waves: resting state, eyes closed vs eyes open, 200 blocks |
| `erpcore_n170.npz` | 50 MB | ERP CORE N170: face perception, 1,733 stimulus-locked epochs |

Each package is **self-contained**: the signal and everything that labels it sit
in the same `.npz`.

## The shared format

Both files hold the same **seven arrays**, with the same names, meanings and
units. Nothing is pickled, so a plain `np.load` is enough.

| Array | Shape | Type | Units | Meaning |
|---|---|---|---|---|
| `X` | (n_epochs, n_channels, n_times) | float32 | microvolts | The signal itself. One row per epoch, one column per electrode. |
| `condition` | (n_epochs,) | str | - | Experimental condition of each epoch. Values differ per dataset (see below). |
| `subject` | (n_epochs,) | str | - | Which participant each epoch came from. |
| `times` | (n_times,) | float32 | seconds | Time axis of the third dimension of `X`, shared by every epoch. |
| `ch_names` | (n_channels,) | str | - | Electrode names, in the order of the second dimension of `X`. |
| `ch_xy` | (n_channels, 2) | float32 | - | Approximate 2D scalp position of each electrode, for topographies: x to the right, y towards the nose, scaled to the unit disc. |
| `sfreq` | scalar | float32 | Hz | Sampling rate. 256 Hz in both datasets. |

`alphawaves.npz` adds **two arrays of its own**, both one value per block, in the
same order as `condition` and `subject`:

| Array | Shape | Type | Units | Meaning |
|---|---|---|---|---|
| `block` | (n_epochs,) | int16 | - | Position of the block in its session, 1 to 10. Recovers the alternating eyes-closed / eyes-open order the subject actually experienced. |
| `onset_s` | (n_epochs,) | float32 | seconds | When the block started in the original continuous recording. |

The `ch_xy` positions come from the standard 10-20 montage and are the same
source for both datasets, so topographies are comparable across the two. They
are schematic positions for plotting, not measured electrode locations.

## Dataset 1: EEG Alpha Waves (`alphawaves.npz`)

### Provenance

The EEG Alpha Waves dataset of Cattan, Rodrigues and Congedo, recorded at
GIPSA-lab, Grenoble, in 2017. Zenodo record 2348892, DOI
10.5281/zenodo.2348892, licensed CC BY 4.0. Primary reference: Cattan, Andreev,
Mendoza and Congedo (2018), "The Impact of Passive Head-Mounted Virtual Reality
Devices on the Quality of EEG Signals", Eurographics Workshop on Virtual
Reality Interaction and Physical Simulation.

### Protocol

Resting state, no task. Each participant sat through ten blocks of ten seconds:
five with the eyes closed and five with the eyes open, alternating, with the
experimenter announcing each block beforehand. Recorded on a g.USBamp with 16
wet electrodes placed by the 10-20 system, reference on the right earlobe,
ground at AFz, at 512 Hz with no digital filter.

### Contents

200 blocks: 20 subjects x 10 blocks, 16 channels, 2,560 samples (10 s at
256 Hz). `condition` is `eyes_closed` or `eyes_open`, 100 blocks each, and
`block` gives each one its position in the session so the alternation is
recoverable. The release contains 20 subjects but numbers them `subject_00` to
`subject_20`: `subject_07` does not exist upstream, which is why the numbering
has a gap.

Channels, in array order: FP1, FP2, FC5, FC6, FZ, T7, CZ, T8, P7, P3, PZ, P4,
P8, O1, Oz, O2.

### Preprocessing

Each continuous recording was downsampled from 512 Hz to 256 Hz with a
zero-phase FIR anti-alias filter, and the ten blocks were then cut out of it.
That is the only processing.

### Consequences, and what students will hit

- **The signal is DC-coupled.** Each channel sits on a constant offset of
  several thousand microvolts, so a raw plot is a flat line far from zero and a
  raw spectrum is dominated by its DC term. Detrending or high-passing each
  channel is the first thing anyone has to do.
- **Eyeblinks are present.** Large and obvious on FP1 and FP2 and
  largely absent at Oz. Useful for teaching what an artifact looks like before
  teaching how to remove one.
- **`subject_19` has an extreme artifact:** a 240 mV excursion on P4, roughly
  ten times any other subject's peak. It will ruin any group average that
  does not exclude or clip it, which is the point of keeping it.
- **50 Hz line noise is present.** As expected from an unfiltered recording.

### The effect it is used for

Occipital alpha blocking: 8-12 Hz power over O1, Oz and O2 is much higher with
the eyes closed than with the eyes open. Across the 20 subjects the median
closed/open ratio is about 6, ranging from 0.9 to 16. **19 of 20 subjects show
the effect;** one does not, which is a more honest starting point for talking
about individual variability than a dataset where it always works.

## Dataset 2: ERP CORE N170 (`erpcore_n170.npz`)

### Provenance

A reduced subset of the N170 face-perception paradigm of ERP CORE. Kappenman,
Farrens, Zhang, Stewart and Luck (2021), "ERP CORE: An open resource for human
event-related potential research", *NeuroImage* 225:117465. DOI
10.18115/D5JW4R, OSF project `thsqg`.

**Licensed CC BY-SA 4.0.** Attribution is required, and any derivative of this
data has to be shared under the same licence. `erpcore_n170_LICENSE.txt` must
stay with the files wherever they are distributed.

### Protocol

Participants saw photographs of faces and cars, plus phase-scrambled versions
of both, and judged on each trial whether the image was an object or a texture.
Faces evoke the N170: a negative peak around 170 ms over the occipito-temporal
electrodes, largest at PO7 and PO8.

### Contents

1,733 epochs from 6 subjects (`sub-001`, `sub-002`, `sub-004`, `sub-005`,
`sub-006`, `sub-007`), 30 channels, 256 samples spanning -0.2 to 0.796 s
around stimulus onset at 256 Hz. Four conditions: `face` (426 epochs), `car`
(435), `scrambled_face` (437), `scrambled_car` (435).

These are 6 subjects curated from the 40 in the full release, chosen for having
enough clean epochs; `sub-003` was rejected as too artifact-heavy. The point of
the subset is that students never download or handle the full ERP CORE release.

### Preprocessing

Preprocessed at build time with MNE, so that nothing but numpy is needed to use
it: band-pass 0.5-30 Hz, average reference, epoched -0.2 to 0.8 s with a
(-0.2, 0) baseline, epochs exceeding 250 uV peak-to-peak rejected, resampled to
256 Hz, EOG channels dropped (NB: this is the opposite choice from the Alpha Waves 
package, on purpose, this one arrives clean, so a practical can get to averaging 
and to the ERP itself without spending its time on cleaning).

### The two contrasts, which do not show the same thing

This matters for how the comparison is framed, and it is worth making students
discover it rather than asserting it:

- **`face` vs `scrambled_face` is the amplitude effect.** The face peak is
  about 5 uV more negative, in all 6 subjects. This is the clean N170 to use if
  the point is "faces give a bigger response".
- **`face` vs `car` is mostly a latency effect.** Faces peak about 14 ms
  earlier, consistently in all 6 subjects, while the amplitude difference is
  small (about 1.4 uV on average) and does not hold in 2 of the 6.

The figures above are the **peak** of the PO7/PO8
average in the 110-220 ms window, per subject: face minus scrambled-face comes
out at -5.3 uV in 6 of 6 subjects, and face minus car at -1.4 uV in 4 of 6, with
the latency shift of -14.3 ms holding in 6 of 6. `explore_n170.ipynb` reports the
**mean** amplitude across a window instead.

Note also that the N170 is maximal at the **occipito-temporal** sites PO7 and
PO8, not strictly the occipital ones, and that its frontocentral positive
counterpart in the same epochs is the VPP.

## Why these two datasets are bundled together

Together they teach when averaging works and when it destroys the thing you are
looking for.

The N170 is an **evoked** response: it is phase-locked to stimulus onset, so it
sits at the same latency with the same sign in every epoch and survives
averaging across epochs. Averaging is exactly the right tool, and it is what
pulls a few microvolts of signal out of much larger noise.

Eyes-closed alpha is **induced**: it is an ongoing oscillation whose phase is
unrelated to the start of the block. Average the blocks together and the peaks
of one cancel the troughs of another, so the average tends to nothing even
though the oscillation is obviously there in every single block. It has to be
approached through power or correlation instead: Welch spectra, spectrograms,
band power, or a time-frequency decomposition.

The same operation, applied to two datasets, works on one and fails on the
other, for a reason students can see in the raw traces.

## Attribution

Both datasets are other people's recordings, redistributed under their
licences. Any use of them in teaching material should credit the original
authors, using the references given in the two Provenance sections above. The
ERP CORE files additionally carry a **ShareAlike** obligation, and
`erpcore_n170_LICENSE.txt` is part of the data: it has to be passed on with
`erpcore_n170.npz` wherever the file goes, including into the student-facing
copy of the material.
