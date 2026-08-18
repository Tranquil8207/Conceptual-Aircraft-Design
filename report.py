"""Pretty-print conceptual design results from process()."""

from tabulate import tabulate

from process import process

# Match process.py loop tolerances for status lines
CHANGE = 0.0075
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

    overall_ok = weight_ok

    # --- Convergence / status ---
    status_rows = [
        _row("Weight residual |W-Wguess|/Wguess",
             results.get("weight_residual", delta), "—", 4,
             f"limit {CHANGE}"),
        _row("Iterations", results.get("iterations"), "—", 0),
        _row("Weight closed", results.get("weight_ok", weight_ok), "", 0),
        _row("OVERALL CONVERGED", overall_ok, "", 0),
    ]
    _print_section("1. CONVERGENCE STATUS", status_rows)

    # --- Weight ---
    wg_n, wg_kg = _n_and_kg(w_guess)
    wc_n, wc_kg = _n_and_kg(w_comp)
    we_n, we_kg = _n_and_kg(results.get("W_empty"))
    wp_n, wp_kg = _n_and_kg(results.get("W_payload"))

    def _kg_row(label, n, note=""):
        _, kg = _n_and_kg(n)
        return _row(label, kg, "kg", 4, note)

    weight_rows = [
        _kg_row("Wing", results.get("W_wing")),
        _kg_row("Horiz. tail", results.get("W_ht")),
        _kg_row("Vert. tail", results.get("W_vt")),
        _kg_row("Fuselage", results.get("W_fus")),
        _kg_row("Landing gear", results.get("W_LG")),
        _kg_row("Structure sum", results.get("W_structure")),
        _kg_row("Motors", results.get("W_motor"), "Tyan from pmax"),
        _kg_row("ESC", results.get("W_esc")),
        _kg_row("Propeller(s)", results.get("W_prop")),
        _kg_row("Propulsion sum", results.get("W_propulsion")),
        _kg_row("Battery", results.get("W_batt")),
        _kg_row("Ancillary", results.get("W_ancilliary")),
        _kg_row("W_empty", we_n, "structure + propulsion + batt + ancillary"),
        _kg_row("Payload", wp_n, "inputs payload_kg"),
        _kg_row("W_computed", wc_n, "empty + payload"),
        _row("WTO guess", wg_kg, "kg", 4),
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
        _row("Thrust-to-weight TW (takeoff)", results.get("TW_takeoff"), "—", 5),
        _row("Stall speed (TO ref) v_TO_stall", results.get("v_TO_stall"), "m/s", 3),
        _row("Liftoff speed Vlo", results.get("Vlo"), "m/s", 3),
        _row("Governing power case", results.get("governing_case"), "", 0),
        _row("Max power pmax (envelope-governing)", results.get("pmax"), "W", 4),
        _row("ESC weight coeff (pmax/Vmax)", results.get("esc_wt_coeff"), "—", 4),
        _row("Propeller diameter dprop", results.get("dprop"), "m", 4),
    ]
    if results.get("Preq_VTOL") is not None:
        prop_rows.append(_row("P required VTOL", results.get("Preq_VTOL"), "W", 3))
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
        _row("Climb Velocity", results.get("V_climb"), "m/s", 3),
    ]
    _print_section("5b. FULL FLIGHT-ENVELOPE POWER SIZING", envelope_rows)

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
