"""
constraint_diagram.py
=======================

Forward-flight constraint diagram at converged WTO.

Uses the T/W vs W/S arrays already built in calc_optimalwingloading:
takeoff, climb, cruise, ceiling, turn, plus stall and landing W/S limits.
"""
import matplotlib.pyplot as plt
from plot_helpers import plots_path


def plot_constraint_diagram(params, results, show=False):
    fig, ax = plt.subplots(figsize=(9, 6))

    for name, tw in results['TW_curves'].items():
        ax.plot(results['WS_sweep'], tw, lw=2, label=name)

    ax.plot(
        results['WS_sweep'],
        results['TW_envelope'],
        color='black',
        lw=2.5,
        label='Envelope',
    )

    ax.axvline(
        results['WS_stall_limit'],
        linestyle='--',
        label=f"Stall W/S = {results['WS_stall_limit']:.1f} N/m²",
    )

    if results.get('WS_landing') is not None:
        ax.axvline(
            results['WS_landing'],
            linestyle=':',
            label=f"Landing W/S = {results['WS_landing']:.1f} N/m²",
        )

    ax.scatter(
        [results['W_computed'] / results['S_wing']],
        [results['TW_opt']],
        s=60,
        zorder=5,
        color='black',
        label=f"WTO: W/S={results['W_computed'] / results['S_wing']:.1f}",
    )

    ax.set_xlabel("Wing Loading, W/S [N/m²]")
    ax.set_ylabel("Thrust-to-Weight Ratio, T/W")
    ax.set_title("Forward-Flight Constraint Diagram")
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()

    path = plots_path("constraint_diagram.png")
    fig.savefig(path, dpi=200)
    print(f"Saved {path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    from process import process
    params, results = process()
    plot_constraint_diagram(params, results, show=True)
