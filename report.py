"""Pretty-print conceptual design results from process()."""

from tabulate import tabulate

from process import process

# Match process.py loop tolerances for status lines
CHANGE = 0.0075
TOL = 1e-4
G = 9.81  # N per kg (same as inputs)


def _fmt(value, decimals=3):
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}"
    return str(value)


def _row(quantity, value, unit="", decimals=3, note=""):
    return [quantity, _fmt(value, decimals), unit, note]


def _print_section(title, rows):
    """rows: list of [quantity, value, unit, note]"""
    print()
    print(title)
    print("─" * max(len(title), 40))
    print(
        tabulate(
            rows,
            headers=["Quantity", "Value", "Unit", "Notes"],
            tablefmt="github",
            colalign=("left", "right", "left", "left"),
        )
    )


def _n_and_kg(n):
    if n is None:
        return None, None
    return n, n / G


def build_report(results):
    w_guess = results.get("WTO_guess")
    w_comp = results.get("W_computed")
    if w_guess and w_guess != 0 and w_comp is not None:
        delta = abs(w_comp - w_guess) / w_guess
        weight_ok = delta <= CHANGE
    else:
        delta = None
        weight_ok = False

    l_tail = results.get("l_tail")
    L_fuse = results.get("L_fuse")
    if l_tail is not None and L_fuse is not None:
        tail_ok = (l_tail - L_fuse) <= TOL
    else:
        tail_ok = bool(results.get("tail_fit_ok", False))

    sae_ok = bool(results.get("sae_ok", False))
    overall_ok = weight_ok and tail_ok and sae_ok

    # --- Convergence / status ---
    status_rows = [
        _row("Weight residual |W-Wguess|/Wguess", delta, "—", 4,
             f"limit {CHANGE}"),
        _row("Weight closed", weight_ok, "", 0),
        _row("Tail fit (l_tail <= L_fuse)", tail_ok, "", 0),
        _row("SAE L+W+H ok", sae_ok, "", 0,
             f"LHW={_fmt(results.get('LHW_total'))} m, limit 3.81 m"),
        _row("Geometry feasible", results.get("geometry_feasible"), "", 0),
        _row("OVERALL CONVERGED", overall_ok, "", 0),
    ]
    _print_section("1. CONVERGENCE STATUS", status_rows)

    # --- Weight ---
    wg_n, wg_kg = _n_and_kg(w_guess)
    wc_n, wc_kg = _n_and_kg(w_comp)
    weight_rows = [
        _row("WTO guess", wg_n, "N", 3, f"{_fmt(wg_kg)} kg"),
        _row("W computed (empty build-up)", wc_n, "N", 3, f"{_fmt(wc_kg)} kg"),
        _row("Difference (computed - guess)", (wc_n - wg_n) if (wc_n is not None and wg_n is not None) else None, "N", 3),
    ]
    _print_section("2. WEIGHT", weight_rows)

    # --- Wing ---
    wing_rows = [
        _row("Wing loading (final)", results.get("WLfinal"), "N/m^2", 3),
        _row("Wing area S_wing", results.get("S_wing"), "m^2", 4),
        _row("Aspect ratio AR_wing", results.get("AR_wing"), "—", 3),
        _row("Mean geometric chord C_wing", results.get("C_wing"), "m", 4),
        _row("Root chord C_root", results.get("C_root"), "m", 4),
        _row("Tip chord C_tip", results.get("C_tip"), "m", 4),
        _row("MAC C_wing_adj", results.get("C_wing_adj"), "m", 4),
    ]
    _print_section("3. WING", wing_rows)

    # --- Empennage / controls ---
    tail_rows = [
        _row("Tail arm l_tail", results.get("l_tail"), "m", 4),
        _row("Horizontal tail area S_ht", results.get("S_ht"), "m^2", 4),
        _row("Vertical tail area S_vt", results.get("S_vt"), "m^2", 4),
        _row("HT span", results.get("span_ht"), "m", 4),
        _row("VT span", results.get("span_vt"), "m", 4),
        _row("HT chord C_ht", results.get("C_ht"), "m", 4),
        _row("VT chord C_vt", results.get("C_vt"), "m", 4),
        _row("Aileron area", results.get("S_aileron"), "m^2", 4),
        _row("Elevator area", results.get("S_elevator"), "m^2", 4),
        _row("Rudder area", results.get("S_rudder"), "m^2", 4),
        _row("Aileron chord", results.get("C_aileron"), "m", 4),
        _row("Elevator chord", results.get("C_elevator"), "m", 4),
        _row("Rudder chord", results.get("C_rudder"), "m", 4),
    ]
    _print_section("4. TAILS & CONTROL SURFACES", tail_rows)

    # --- Propulsion / performance ---
    prop_rows = [
        _row("Thrust-to-weight TW (takeoff, dto/Ld-based)", results.get("TW"), "—", 5),
        _row("Stall speed (TO ref) v_TO_stall", results.get("v_TO_stall"), "m/s", 3),
        _row("Liftoff speed Vlo", results.get("Vlo"), "m/s", 3),
        _row("Governing power case", results.get("governing_case"), "", 0),
        _row("Max power pmax (envelope-governing)", results.get("pmax"), "W", 4),
        _row("ESC weight coeff (pmax/Vmax)", results.get("esc_wt_coeff"), "—", 4),
        _row("Propeller diameter dprop", results.get("dprop"), "m", 4),
    ]
    _print_section("5. PROPULSION & TAKEOFF", prop_rows)

    # --- Full flight-envelope power sizing ---
    envelope_rows = [
        _row("WS stall limit (upper bound)", results.get("WS_stall_limit"), "N/m^2", 3),
        _row("T/W climb", results.get("TW_climb"), "—", 5),
        _row("T/W cruise", results.get("TW_cruise"), "—", 5),
        _row("T/W ceiling", results.get("TW_ceiling"), "—", 5),
        _row("T/W turn", results.get("TW_turn"), "—", 5),
        _row("P takeoff", results.get("P_takeoff"), "W", 3),
        _row("P climb", results.get("P_climb"), "W", 3),
        _row("P cruise", results.get("P_cruise"), "W", 3),
        _row("P ceiling", results.get("P_ceiling"), "W", 3),
        _row("P turn", results.get("P_turn"), "W", 3),
    ]
    _print_section("5b. FULL FLIGHT-ENVELOPE POWER SIZING", envelope_rows)

    # --- Airframe geometry / SAE ---
    remaining = results.get("remaining_space")
    geo_rows = [
        _row("Fuselage length L_fuse", results.get("L_fuse"), "m", 4, "working (may be grown)"),
        _row("Fuselage face a", results.get("a"), "m", 4, "working"),
        _row("Fuselage face b", results.get("b"), "m", 4, "working"),
        _row("Adjusted length (+ pad)", results.get("adjusted_L"), "m", 4),
        _row("Forward fuselage length", results.get("forward_fuse_L"), "m", 4),
        _row("Aircraft width ac_W (span)", results.get("ac_W"), "m", 4),
        _row("Aircraft height ac_H", results.get("ac_H"), "m", 4),
        _row("L + W + H total", results.get("LHW_total"), "m", 4, "SAE limit 3.81 m"),
        _row("Remaining SAE space", remaining, "m", 4,
             "negative => over limit" if (remaining is not None and remaining < 0) else ""),
        _row("L_fuse max under SAE", results.get("L_fuse_max_sae"), "m", 4),
    ]
    _print_section("6. FUSELAGE GEOMETRY & SAE BOX", geo_rows)

    print()
    print("Report complete.")
    if not overall_ok:
        print(
            "Note: solution did not fully converge. "
            "Check weight residual and bounds (WTO_min / WTO_max)."
        )
    print()


def main(results=None):
    """Run process() if needed, then print the formatted report.

    Prefer: python process.py  (central entry point).
    Also works: python report.py
    """
    print()
    print("CONCEPTUAL AIRCRAFT DESIGN — RESULTS REPORT")
    print("=" * 48)
    if results is None:
        results = process()
    build_report(results)


if __name__ == "__main__":
    main()
