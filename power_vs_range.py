"""
4_power_vs_range.py
===================

Forward-flight cruise power vs battery-limited range at converged WTO.

Range is E_prop * V / P(V).
"""
import matplotlib.pyplot as plt
from plot_helpers import V_sweep, power_forward, range_forward, plots_path


def plot_power_vs_range(params, results, show=False):
    V_array = V_sweep(params)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        range_forward(params, results, V_array, results['W_computed']) / 1000.0,
        power_forward(params, results, V_array, results['W_computed']),
        lw=2,
        label="WTO cruise power",
    )

    ax.set_xlabel("Battery-Limited Total Forward Range [km]")
    ax.set_ylabel("Forward Cruise Power [W]")
    ax.set_title(
        "Forward Cruise Power vs Battery-Limited Range\n"
        "R = E_prop * V / P(V) at converged WTO"
    )
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()

    path = plots_path("power_vs_range.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_power_vs_range(params, results, show=True)
