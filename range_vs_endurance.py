"""
5_range_vs_endurance.py
=======================

Battery-limited range vs endurance at converged WTO.
"""
import matplotlib.pyplot as plt
from plot_helpers import V_sweep, range_forward, endurance_forward, plots_path


def plot_range_vs_endurance(params, results, show=False):
    V_array = V_sweep(params)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        endurance_forward(params, results, V_array, results['W_computed']) / 60.0,
        range_forward(params, results, V_array, results['W_computed']) / 1000.0,
        lw=2,
        label="WTO",
    )

    ax.set_xlabel("Total Forward Cruise Endurance [min]")
    ax.set_ylabel("Total Horizontal Forward Range [km]")
    ax.set_title(
        "Forward-Flight Range vs Endurance\n"
        "R = E_prop * V / P(V),  t = E_prop / P(V)"
    )
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()

    path = plots_path("range_vs_endurance.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_range_vs_endurance(params, results, show=True)
