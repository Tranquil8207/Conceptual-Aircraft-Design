"""
2_drag_curve.py
===============

Forward-flight drag at converged WTO.
"""

import matplotlib.pyplot as plt
from plot_helpers import (
    V_sweep, drag_forward, characteristic_velocities, plots_path,
)


def plot_drag_curve(params, results, show=False):
    V_array = V_sweep(params)
    CHAR = characteristic_velocities(params, results)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        V_array, drag_forward(params, results, V_array, results['W_computed']),
        lw=2,
        label="WTO"
    )

    ax.axvline(
        params['V_stall'], linestyle=":",
        label=f"Specified stall = {params['V_stall']:.2f} m/s"
    )

    ax.axvline(
        CHAR["V_max_range"], linestyle="--",
        label=f"Max range = {CHAR['V_max_range']:.2f} m/s"
    )

    ax.axvline(
        params['V_cruise'], linestyle=":",
        label=f"Cruise = {params['V_cruise']:.2f} m/s"
    )

    ax.set_xlabel("True Airspeed [m/s]")
    ax.set_ylabel("Aerodynamic Drag [N]")
    ax.set_title("Forward-Flight Drag — Converged WTO")
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()

    path = plots_path("drag_curve.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_drag_curve(params, results, show=True)
