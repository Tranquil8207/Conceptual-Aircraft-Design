"""
6_velocity_vs_range.py
======================

True airspeed vs battery-limited range at converged WTO.
"""
import matplotlib.pyplot as plt
from plot_helpers import V_sweep, range_forward, characteristic_velocities, plots_path


def plot_velocity_vs_range(params, results, show=False):
    V_array = V_sweep(params)
    CHAR = characteristic_velocities(params, results)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        V_array,
        range_forward(params, results, V_array, results['W_computed']) / 1000.0,
        lw=2,
        label="WTO battery-limited range",
    )

    ax.axvline(
        params['V_stall'],
        linestyle=":",
        label=f"Stall = {params['V_stall']:.2f} m/s",
    )

    ax.axvline(
        CHAR["V_max_range"],
        linestyle="--",
        label=f"Max range = {CHAR['V_max_range']:.2f} m/s",
    )

    ax.axvline(
        params['V_cruise'],
        linestyle=":",
        label=f"Cruise = {params['V_cruise']:.2f} m/s",
    )

    ax.set_xlabel("True Airspeed [m/s]")
    ax.set_ylabel("Battery-Limited Total Forward Range [km]")
    ax.set_title("Velocity vs Forward-Flight Range")
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()

    path = plots_path("velocity_vs_range.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_velocity_vs_range(params, results, show=True)
