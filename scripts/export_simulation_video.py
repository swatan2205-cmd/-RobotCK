"""Animate representative saved MATLAB runs without recomputing the controllers."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/simulation_media/robotck_simulation.mp4'
CASES = [
    ('eight_i2_w10_tstrhc', 'Số 8 · T-ST-RHC'),
    ('eight_i2_w10_lyapunov', 'Số 8 · Lyapunov'),
    ('circle_i3_w10_tstrhc', 'Đường tròn · T-ST-RHC'),
    ('circle_i3_w10_lyapunov', 'Đường tròn · Lyapunov'),
]


def main():
    runs = [loadmat(ROOT / 'results' / key / 'run.mat', simplify_cells=True)['run']
            for key, _ in CASES]
    time = runs[0]['t_state']
    assert all(np.array_equal(run['t_state'], time) and np.isfinite(run['q']).all()
               for run in runs)
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 8), layout='constrained')
    stamp = fig.suptitle('', fontsize=15, fontweight='bold')
    artists = []
    for index, (ax, run, (_, title)) in enumerate(zip(axes.flat, runs, CASES)):
        ref = run['reference']['q']
        q = run['q']
        ax.plot(ref[0], ref[1], '--', color='#d25c36', label='Tham chiếu')
        path, = ax.plot([], [], color='#126c9b', lw=1.9, label='Robot')
        dot, = ax.plot([], [], 'o', color='#126c9b', ms=5)
        limits = np.concatenate([np.concatenate((r['q'][:2], r['reference']['q'][:2]), axis=1)
                                 for r in runs[index//2*2:index//2*2+2]], axis=1)
        ax.set(xlim=(limits[0].min()-.08, limits[0].max()+.08),
               ylim=(limits[1].min()-.08, limits[1].max()+.08),
               title=title, xlabel='x (m)', ylabel='y (m)')
        ax.set_aspect('equal', adjustable='box')
        ax.grid(alpha=.25)
        ax.legend(loc='upper right', fontsize=8)
        artists.append((path, dot, q))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    writer = FFMpegWriter(fps=20, codec='libx264', extra_args=['-pix_fmt', 'yuv420p', '-movflags', '+faststart'])
    with writer.saving(fig, str(OUTPUT), dpi=100):
        for k, t in enumerate(time):
            stamp.set_text(f'Bám quỹ đạo robot hai bánh   |   t = {t:05.2f} s   |   Giới hạn bánh 10 rad/s')
            for path, dot, q in artists:
                path.set_data(q[0, :k+1], q[1, :k+1])
                dot.set_data(q[0, k:k+1], q[1, k:k+1])
            writer.grab_frame()
    plt.close(fig)
    print(OUTPUT)


if __name__ == '__main__':
    main()
