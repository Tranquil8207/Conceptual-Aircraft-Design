"""
3_power_curve.py
================

Forward-flight power required at converged WTO.

All VTOL/hover power references have been removed.
"""
import matplotlib.pyplot as plt
from plot_helpers import (
    V_sweep, power_forward, characteristic_velocities, plots_path,
)


def plot_power_curve(params, results, show=False):
    V_array = V_sweep(params)
    CHAR = characteristic_velocities(params, results)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        V_array,
        power_forward(params, results, V_array, results['W_computed']),
        lw=2,
        label="Forward cruise power — WTO",
    )

    ax.axvline(
        params['V_stall'],
        linestyle=":",
        label=f"Stall = {params['V_stall']:.2f} m/s",
    )

    ax.axvline(
        CHAR["V_max_endurance"],
        linestyle="--",
        label=f"Max endurance = {CHAR['V_max_endurance']:.2f} m/s",
    )

    ax.axvline(
        CHAR["V_max_range"],
        linestyle="--",
        alpha=0.7,
        label=f"Max range = {CHAR['V_max_range']:.2f} m/s",
    )

    ax.axvline(
        params['V_cruise'],
        linestyle=":",
        label=f"Cruise = {params['V_cruise']:.2f} m/s",
    )

    ax.set_xlabel("True Airspeed [m/s]")
    ax.set_ylabel("Forward Cruise Power Required [W]")
    ax.set_title("Forward-Flight Power Required — Converged WTO")
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()

    path = plots_path("power_curve.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_power_curve(params, results, show=True)
