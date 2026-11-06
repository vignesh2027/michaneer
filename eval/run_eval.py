"""Evaluation for Michaneer, from public numbers only.

Run from the repository root:  uv run python -m eval.run_eval
Writes eval/RESULTS.md. Every input below is either a published figure
(named in michaneer/sources.py) or a grid of values, never a survey we made up.
"""

from __future__ import annotations

import itertools
from pathlib import Path

from michaneer import model
from michaneer.app import EXAMPLE, parse

OUT = Path(__file__).resolve().parent / "RESULTS.md"
WHO = model.WHO_DRINK_COOK_L_PER_PERSON


def fmt(x: float) -> str:
    return f"{x:,.0f}"


def mass_balance() -> list[str]:
    feeds = [50, 150, 300, 500, 800, 1500, 3000, 6000]
    recoveries = [0.10, 0.15, 0.20, 0.25, 0.33, 0.40, 0.50, 0.60, 0.75, 0.90]
    rejections = [0.80, 0.90, 0.95, 0.98, 0.99]
    worst = 0.0
    n = 0
    for f, r, k in itertools.product(feeds, recoveries, rejections):
        product = f * (1 - k)
        reject, _ = model.reject_tds(f, r, product)
        err = abs((product * r + reject * (1 - r)) - f) / f
        worst = max(worst, err)
        n += 1
    return [
        "## 1. The salt balance closes",
        "",
        f"Grid: {len(feeds)} tap TDS values from 50 to 6000 mg/L, {len(recoveries)} recovery levels from 10 to 90 percent, "
        f"{len(rejections)} membrane salt rejections from 80 to 99 percent: {n} points.",
        "",
        f"Largest relative error between salt in and salt out: {worst:.1e}. The reject TDS formula conserves mass to floating point precision.",
        "",
    ]


def per_person() -> list[str]:
    rows = [
        ("IS 16240:2015 floor (superseded)", model.RECOVERY_FLOOR_2015, "is16240"),
        ("3 L reject per litre, top of the Lok Sabha range", 0.25, "loksabha778"),
        ("2 L reject per litre, middle of the Lok Sabha range", 1 / 3, "loksabha778"),
        ("IS 16240:2023 floor", model.RECOVERY_FLOOR_2023, "is16240"),
        ("1 L reject per litre, bottom of the Lok Sabha range", 0.50, "loksabha778"),
        ("NGT direction (stayed by the Supreme Court)", model.RECOVERY_NGT_DIRECTION, "ngt134"),
    ]
    lines = [
        "## 2. Litres down the drain per person per year",
        "",
        f"One person drinking and cooking with {WHO} L of purified water a day (WHO, Howard and Bartram 2003).",
        "",
        "| Recovery level | Recovery | Reject per litre | Reject per person per year |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, r, _ in rows:
        lines.append(f"| {name} | {r*100:.0f}% | {model.reject_per_litre(r):.2f} L | {fmt(model.annual_reject_l(WHO, r))} L |")
    top = model.annual_reject_l(WHO, 0.25)
    floor = model.annual_reject_l(WHO, 0.40)
    lines += [
        "",
        f"Finding: across the official range, one person's purifier sends between {fmt(model.annual_reject_l(WHO, 0.5))} and "
        f"{fmt(top)} litres a year to the drain. Bringing a unit at the top of the range up to the 2023 floor saves "
        f"{fmt(top - floor)} litres per person per year, before any reuse. The spread is a factor of three, which is why "
        "the app measures instead of assuming a ratio.",
        "",
    ]
    return lines


def precision() -> list[str]:
    lines = [
        "## 3. How precise is a kitchen bucket test?",
        "",
        "One litre of purified water; the only error is reading the bucket on a jug marked every 50 or 100 mL "
        "(half a marking either way).",
        "",
        "| True recovery | Reject collected | Range, 50 mL jug | Range, 100 mL jug |",
        "| ---: | ---: | --- | --- |",
    ]
    bands = {}
    for r in (0.20, 0.25, 1 / 3, 0.40, 0.50, 0.60):
        reject = 1000 * (1 - r) / r
        b50 = model.recovery_bounds(1000, reject, 50)
        b100 = model.recovery_bounds(1000, reject, 100)
        bands[round(r, 3)] = b100
        lines.append(
            f"| {r*100:.0f}% | {fmt(reject)} mL | {b50[0]*100:.1f} to {b50[1]*100:.1f}% | {b100[0]*100:.1f} to {b100[1]*100:.1f}% |"
        )
    separable = bands[0.25][1] < bands[0.4][0]
    lines += [
        "",
        f"Finding: even with a coarse 100 mL jug the error band is under {max((b[1]-b[0])*100 for b in bands.values()):.1f} "
        f"percentage points, so a 25 percent unit and a 40 percent unit {'never overlap' if separable else 'can overlap'}. "
        "The bucket test is precise enough for the decision it supports. Larger real-world errors come from starting and "
        "stopping the bottle and hose at different moments and from pressure changes, which is why the app asks for a repeat.",
        "",
    ]
    return lines


def plants() -> list[str]:
    lines = [
        "## 4. Is \"water your plants with it\" good advice?",
        "",
        "Highest tap-water TDS for which the reject stream stays under FAO's 450 mg/L no-restriction line "
        "(FAO Irrigation and Drainage Paper 29, Table 1), from the salt balance.",
        "",
        "| Recovery | 90% salt rejection | 95% salt rejection | 98% salt rejection |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for r in (0.20, 0.25, 1 / 3, 0.40, 0.50, 0.60):
        cells = [f"{fmt(model.max_feed_for_plants(r, k))} mg/L" for k in (0.90, 0.95, 0.98)]
        lines.append(f"| {r*100:.0f}% | " + " | ".join(cells) + " |")
    at_limit = model.reject_tds(model.TDS_ACCEPTABLE, 0.25, model.TDS_ACCEPTABLE * 0.05)[0]
    lines += [
        "",
        f"Finding: at 25 percent recovery and 95 percent rejection, any tap water above "
        f"{fmt(model.max_feed_for_plants(0.25, 0.95))} mg/L gives reject water outside FAO's no-restriction class. Tap water "
        f"right at the IS 10500 acceptable limit of 500 mg/L becomes about {fmt(at_limit)} mg/L in the reject stream. "
        "Blanket advice to pour RO reject on plants is only safe for low-TDS supplies, so the app gives plant advice only "
        "from the computed reject TDS, and assumes the worst case when the purified-water reading is missing.",
        "",
    ]
    return lines


def worked_example() -> list[str]:
    res = model.evaluate(parse(EXAMPLE))
    lines = [
        "## 5. Worked example through the app",
        "",
        "The app's built-in example (labelled as illustrative in the UI): 3000 mL reject per 1000 mL purified, the top of "
        "the Lok Sabha range; 30 L a day of purified water; label rating 40 percent; tap 420 mg/L, purified 35 mg/L; "
        "60 L a day of reuse capacity.",
        "",
        f"* Recovery {res.recovery_pct:.1f} percent, range {res.recovery_low*100:.1f} to {res.recovery_high*100:.1f}.",
        f"* {res.daily_reject_l:.1f} L of reject a day, {fmt(res.annual_reject_l)} L a year.",
        f"* Reject TDS {res.reject_tds:.0f} mg/L, FAO class \"{res.plant_class}\".",
    ]
    for a in res.actions:
        tag = " (only after a lab test)" if a.conditional else ""
        lines.append(f"* Plan: {a.title}{tag}: {fmt(a.litres_per_year)} L a year.")
    lines += [
        f"* Total for the unconditional steps: {fmt(res.combined_litres_per_year)} L a year, which equals all of today's reject "
        "water and never more (a property test checks this across 80 input combinations).",
        "",
    ]
    return lines


def limits() -> list[str]:
    return [
        "## What this evaluation does not show",
        "",
        "* No field measurements. The owner has not yet logged a before and after test on a real unit; when he does, the "
        "numbers go in docs/SUBMISSION.md under their own heading, never mixed with these.",
        "* No city-wide total. There is no public count of RO purifiers in Chennai, so we do not multiply anything by a guess.",
        "* Recovery drifts with inlet pressure, temperature and filter age. One test is one moment.",
        "",
    ]


def main() -> None:
    lines = [
        "# Michaneer evaluation",
        "",
        "Generated by `uv run python -m eval.run_eval`. Inputs are published figures (see michaneer/sources.py) or grids.",
        "",
    ]
    for part in (mass_balance, per_person, precision, plants, worked_example, limits):
        lines += part()
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
