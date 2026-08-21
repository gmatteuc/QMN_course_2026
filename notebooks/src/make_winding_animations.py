"""Render the two winding animations as mp4 files, for sharing outside a notebook.

    python src/make_winding_animations.py                     # writes next to this script
    python src/make_winding_animations.py C:/Users/me/Desktop # or wherever you like

Needs ffmpeg on the PATH, which the course environment has.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# --- the signal we wrap: a strong 10 Hz wave and a weaker 25 Hz one
SAMPLING_RATE = 2000                  # a fine grid, only so the drawings come out smooth
time = np.arange(0, 1, 1 / SAMPLING_RATE)
signal = 1.0 * np.sin(2 * np.pi * 10 * time) + 0.5 * np.sin(2 * np.pi * 25 * time)


def wind(frequency):
    """Wrap the signal around a circle, `frequency` turns per second."""
    return signal * np.exp(-2j * np.pi * frequency * time)


def writer(fps):
    return FFMpegWriter(fps=fps, extra_args=["-pix_fmt", "yuv420p", "-crf", "20"])


def add_silent_audio(path):
    """Messaging apps are happier with a video that has an audio track, even an empty one."""
    tmp = path.with_name(path.stem + "_audio.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path),
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
                    "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "64k",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(path)


def render_wrapping(path, steps=300, hold=20, dpi=130):
    """The walk along the signal, wrapped at 5 Hz and at 10 Hz side by side."""
    w5, w10 = wind(5), wind(10)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    axes[0].plot(time, signal, lw=1, color="0.8")
    trace, = axes[0].plot([], [], lw=1.4, color="C0")
    walker, = axes[0].plot([], [], "o", color="C1", ms=8)
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(-1.8, 1.8)
    axes[0].set_xlabel("time (s)")
    axes[0].set_title("the signal")

    curves, heads, centres = [], [], []
    for ax, wound, frequency in zip(axes[1:], (w5, w10), (5, 10)):
        curve, = ax.plot([], [], lw=0.9, color="C0")
        head, = ax.plot([], [], "o", color="C1", ms=7, label="where we are now")
        centre, = ax.plot([], [], "o", color="C3", ms=10, label="centre of mass so far")
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.7, 1.7)
        ax.set_aspect("equal")
        ax.axhline(0, color="0.85", lw=0.8)
        ax.axvline(0, color="0.85", lw=0.8)
        ax.set_title("wrapped at %d Hz" % frequency)
        curves.append(curve)
        heads.append(head)
        centres.append(centre)
    axes[1].legend(loc="lower center", fontsize=9, frameon=False)

    def draw(i):
        k = max(2, int(min(i + 1, steps) / steps * len(time)))
        trace.set_data(time[:k], signal[:k])
        walker.set_data([time[k - 1]], [signal[k - 1]])
        for curve, head, centre, wound in zip(curves, heads, centres, (w5, w10)):
            curve.set_data(wound.real[:k], wound.imag[:k])
            head.set_data([wound.real[k - 1]], [wound.imag[k - 1]])
            centre.set_data([wound.real[:k].mean()], [wound.imag[:k].mean()])
        return [trace, walker] + curves + heads + centres

    fig.tight_layout()
    FuncAnimation(fig, draw, frames=steps + hold).save(str(path), writer=writer(15), dpi=dpi)
    plt.close(fig)


def render_sweeping(path, dpi=130):
    """The winding speed rising slowly, drawing the spectrum as it goes."""
    sweep = np.arange(1, 30.05, 0.125)                       # winding speeds to visit
    found = [2 * abs(wind(frequency).mean()) for frequency in sweep]

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    curve, = axes[0].plot([], [], lw=0.9, color="C0")
    centre, = axes[0].plot([], [], "o", color="C3", ms=10)
    axes[0].set_xlim(-1.7, 1.7)
    axes[0].set_ylim(-1.7, 1.7)
    axes[0].set_aspect("equal")
    axes[0].axhline(0, color="0.85", lw=0.8)
    axes[0].axvline(0, color="0.85", lw=0.8)

    drawn, = axes[1].plot([], [], lw=2.2, color="C0")
    axes[1].set_xlim(0, 30)
    axes[1].set_ylim(0, 1.2)
    axes[1].set_xlabel("winding speed (Hz)")
    axes[1].set_ylabel("how much of it is there")

    def draw(i):
        wound = wind(sweep[i])
        curve.set_data(wound.real, wound.imag)
        centre.set_data([wound.real.mean()], [wound.imag.mean()])
        drawn.set_data(sweep[:i + 1], found[:i + 1])
        axes[0].set_title("wrapped at %.1f Hz" % sweep[i])
        return curve, centre, drawn

    fig.tight_layout()
    FuncAnimation(fig, draw, frames=len(sweep)).save(str(path), writer=writer(12), dpi=dpi)
    plt.close(fig)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    out.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 11,
                         "figure.facecolor": "white", "savefig.facecolor": "white"})

    for name, render in (("wrapping.mp4", render_wrapping), ("sweeping.mp4", render_sweeping)):
        path = out / name
        render(path)
        add_silent_audio(path)
        print("%-14s %5.2f MB  ->  %s" % (name, path.stat().st_size / 1e6, path))
