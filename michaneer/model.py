"""The arithmetic behind Michaneer.

Everything here is a pure function of the user's own bucket-test readings and
published thresholds (see sources.py). No network, no randomness, no model.

Terms
-----
purified (permeate): water that comes out of the drinking tap.
reject (concentrate): water that leaves through the drain hose.
recovery R: purified / (purified + reject), the share of feed water you drink.
"""

from __future__ import annotations

from dataclasses import dataclass, field

DAYS_PER_YEAR = 365
CAN_LITRES = 20  # the common 20 litre drinking-water can, used only as a unit

# Thresholds, each tied to a source id in sources.py
TDS_ACCEPTABLE = 500.0  # is10500
TDS_PERMISSIBLE = 2000.0  # is10500
RECOVERY_FLOOR_2023 = 0.40  # is16240 (2023 edition)
RECOVERY_FLOOR_2015 = 0.20  # is16240 (2015 edition, superseded)
RECOVERY_NGT_DIRECTION = 0.60  # ngt134, stayed by the Supreme Court
FAO_NONE_BELOW = 450.0  # fao29
FAO_SEVERE_ABOVE = 2000.0  # fao29
WHO_DRINK_COOK_L_PER_PERSON = 7.5  # who2003

SOURCES_OF_WATER = {
    "metrowater": "Piped (Metrowater or utility)",
    "borewell": "Borewell or open well",
    "tanker": "Private tanker lorry",
    "mixed": "Mixed or not sure",
}


class InputError(ValueError):
    """A reading that cannot be right, with a message the user can act on."""


@dataclass(frozen=True)
class Readings:
    """One bucket test, exactly as the user typed it."""

    reject_ml: float
    purified_ml: float = 1000.0
    jug_resolution_ml: float = 50.0
    daily_purified_l: float = 30.0
    seconds: float | None = None
    feed_tds: float | None = None
    product_tds: float | None = None
    rated_recovery_pct: float | None = None
    reusable_l_per_day: float | None = None
    water_source: str = "mixed"

    def validate(self) -> None:
        def need(ok: bool, message: str) -> None:
            if not ok:
                raise InputError(message)

        need(100 <= self.purified_ml <= 20000, "Purified water collected should be between 100 mL and 20 litres.")
        need(0 <= self.reject_ml <= 200000, "Reject water collected should be between 0 and 200 litres.")
        need(0 <= self.jug_resolution_ml <= 1000, "Jug marking interval should be between 0 and 1000 mL.")
        need(0.1 <= self.daily_purified_l <= 20000, "Daily purified water should be between 0.1 and 20000 litres.")
        if self.seconds is not None:
            need(1 <= self.seconds <= 36000, "Fill time should be between 1 second and 10 hours.")
        for name, value in (("Tap water TDS", self.feed_tds), ("Purified water TDS", self.product_tds)):
            if value is not None:
                need(0 <= value <= 50000, f"{name} should be between 0 and 50000 mg/L.")
        if self.feed_tds is not None and self.product_tds is not None:
            need(
                self.product_tds <= self.feed_tds,
                "Purified water TDS is higher than tap water TDS. Check that the two readings are not swapped.",
            )
        if self.rated_recovery_pct is not None:
            need(1 <= self.rated_recovery_pct <= 100, "Rated recovery on the label should be between 1 and 100 percent.")
        if self.reusable_l_per_day is not None:
            need(0 <= self.reusable_l_per_day <= 100000, "Litres you can reuse a day should be between 0 and 100000.")
        need(self.water_source in SOURCES_OF_WATER, "Pick a water source from the list.")


# ---------------------------------------------------------------- core maths


def recovery(purified: float, reject: float) -> float:
    """Share of the feed water that comes out as purified water."""
    total = purified + reject
    if total <= 0:
        raise InputError("Both readings are zero.")
    return purified / total


def recovery_bounds(purified: float, reject: float, resolution: float) -> tuple[float, float]:
    """Recovery range when the reject reading is only known to half a jug marking.

    The bottle is filled to a known mark, so only the jug reading carries error.
    """
    half = resolution / 2.0
    low = purified / (purified + reject + half)
    high_reject = max(reject - half, 0.0)
    high = purified / (purified + high_reject)
    return low, high


def reject_per_litre(r: float) -> float:
    """Litres of reject per litre of purified water at recovery r."""
    if not 0 < r <= 1:
        raise InputError("Recovery must be above 0 and at most 100 percent.")
    return (1.0 - r) / r


def reject_tds(feed: float, r: float, product: float | None) -> tuple[float, bool]:
    """Reject-stream TDS from a salt mass balance.

    feed * Qf = product * Qp + reject * Qr, with Qp = r * Qf and Qr = (1 - r) * Qf.
    Without a purified-water reading, product = 0 gives the highest possible
    reject TDS, which is the safe value for plant advice. The flag says
    whether the value is that upper bound.
    """
    if r >= 1:
        return feed, False
    if product is None:
        return feed / (1.0 - r), True
    return (feed - r * product) / (1.0 - r), False


def tds_class(tds: float) -> str:
    if tds <= TDS_ACCEPTABLE:
        return "acceptable"
    if tds <= TDS_PERMISSIBLE:
        return "permissible"
    return "above"


def fao_class(tds: float) -> str:
    if tds < FAO_NONE_BELOW:
        return "none"
    if tds <= FAO_SEVERE_ABOVE:
        return "slight"
    return "severe"


def annual_reject_l(daily_purified_l: float, r: float) -> float:
    return daily_purified_l * reject_per_litre(r) * DAYS_PER_YEAR


def max_feed_for_plants(r: float, salt_rejection: float) -> float:
    """Highest tap TDS whose reject stays below FAO's no-restriction line.

    With product = feed * (1 - salt_rejection), the mass balance gives
    reject = feed * (1 - r * (1 - salt_rejection)) / (1 - r).
    """
    factor = (1.0 - r * (1.0 - salt_rejection)) / (1.0 - r)
    return FAO_NONE_BELOW / factor


# ---------------------------------------------------------------- the result


@dataclass(frozen=True)
class Action:
    key: str
    title: str
    litres_per_year: float
    detail: str
    conditional: bool = False
    sources: tuple[str, ...] = ()


@dataclass(frozen=True)
class Check:
    label: str
    status: str  # "good", "warn", "bad", "info"
    text: str
    sources: tuple[str, ...] = ()


@dataclass(frozen=True)
class Result:
    readings: Readings
    recovery: float
    recovery_low: float
    recovery_high: float
    reject_per_litre: float
    daily_reject_l: float
    annual_reject_l: float
    production_lph: float | None
    reject_tds: float | None
    reject_tds_is_upper_bound: bool
    plant_class: str | None
    feed_class: str | None
    checks: tuple[Check, ...]
    actions: tuple[Action, ...]
    combined_litres_per_year: float
    right_size_litres_per_year: float | None
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def recovery_pct(self) -> float:
        return self.recovery * 100

    @property
    def annual_cans(self) -> float:
        return self.annual_reject_l / CAN_LITRES


def evaluate(readings: Readings) -> Result:
    readings.validate()
    p, j = readings.purified_ml, readings.reject_ml
    r = recovery(p, j)
    low, high = recovery_bounds(p, j, readings.jug_resolution_ml)
    rpl = j / p
    daily_reject = readings.daily_purified_l * rpl
    annual = daily_reject * DAYS_PER_YEAR

    production = None
    if readings.seconds:
        production = (p / 1000.0) / readings.seconds * 3600.0

    checks: list[Check] = []
    notes: list[str] = []

    # Recovery against the label and the standard
    if readings.rated_recovery_pct is not None:
        rated = readings.rated_recovery_pct / 100.0
        if high < rated:
            checks.append(Check(
                "Label", "bad",
                f"Measured {r*100:.0f} percent (range {low*100:.1f} to {high*100:.1f}) is below the "
                f"{readings.rated_recovery_pct:.0f} percent printed on the label, even allowing for jug error.",
                ("gsr724",),
            ))
        elif low > rated:
            checks.append(Check(
                "Label", "good",
                f"Measured {r*100:.0f} percent is at or above the {readings.rated_recovery_pct:.0f} percent on the label.",
                ("gsr724",),
            ))
        else:
            checks.append(Check(
                "Label", "info",
                f"Measured {r*100:.0f} percent is within jug error of the {readings.rated_recovery_pct:.0f} percent on the label.",
                ("gsr724",),
            ))

    if high < RECOVERY_FLOOR_2023:
        floor_status = "bad" if high < RECOVERY_FLOOR_2015 else "warn"
        checks.append(Check(
            "BIS floor", floor_status,
            f"Below the 40 percent minimum that IS 16240:2023 sets for new domestic purifiers. "
            f"Units certified to the 2015 edition only had to reach 20 percent.",
            ("is16240",),
        ))
    elif low >= RECOVERY_FLOOR_2023:
        checks.append(Check(
            "BIS floor", "good",
            "At or above the 40 percent minimum in IS 16240:2023.",
            ("is16240",),
        ))
    else:
        checks.append(Check(
            "BIS floor", "info",
            "Within jug error of the 40 percent minimum in IS 16240:2023. Repeat the test with a finer jug.",
            ("is16240",),
        ))

    feed_cls = None
    rej_tds = None
    upper = False
    plant = None
    if readings.feed_tds is not None:
        feed_cls = tds_class(readings.feed_tds)
        text = {
            "acceptable": (
                f"Tap water reads {readings.feed_tds:.0f} mg/L, within the 500 mg/L acceptable limit of IS 10500. "
                "Dissolved solids alone do not call for RO here. A TDS pen cannot see germs, fluoride, nitrate "
                "or arsenic, so this is not a safety verdict."
            ),
            "permissible": (
                f"Tap water reads {readings.feed_tds:.0f} mg/L, above the 500 mg/L acceptable limit and within the "
                "2000 mg/L permissible limit of IS 10500. RO is doing real work on dissolved solids."
            ),
            "above": (
                f"Tap water reads {readings.feed_tds:.0f} mg/L, above the 2000 mg/L permissible limit of IS 10500. "
                "Keep the RO, and get the water tested at a lab."
            ),
        }[feed_cls]
        checks.append(Check("Tap water TDS", "good" if feed_cls == "acceptable" else "info", text, ("is10500",)))

        rej_tds, upper = reject_tds(readings.feed_tds, r, readings.product_tds)
        plant = fao_class(rej_tds)
        prefix = "at most " if upper else "about "
        plant_text = {
            "none": "FAO puts water this salty in the no-restriction class for irrigation, so plants are fine.",
            "slight": (
                "FAO puts this in the slight to moderate restriction class. Use it on hardy plants only, "
                "and water with tap water now and then to flush the soil."
            ),
            "severe": "FAO puts this in the severe restriction class. Keep it away from plants.",
        }[plant]
        checks.append(Check(
            "Reject water TDS", {"none": "good", "slight": "warn", "severe": "bad"}[plant],
            f"Reject water is {prefix}{rej_tds:.0f} mg/L by mass balance. {plant_text}",
            ("fao29",),
        ))
        if upper:
            notes.append("Add a purified water TDS reading to replace the upper bound with an estimate.")

    # ------------------------------------------------------------ the plan
    actions: list[Action] = []
    daily = readings.daily_purified_l

    target = None
    if readings.rated_recovery_pct is not None:
        target = readings.rated_recovery_pct / 100.0
        target_label = f"the {readings.rated_recovery_pct:.0f} percent on your label"
    else:
        target = RECOVERY_FLOOR_2023
        target_label = "the 40 percent IS 16240:2023 minimum"

    restored_daily_reject = daily_reject
    restore_saving = 0.0
    if high < target:
        restored_daily_reject = daily * reject_per_litre(target)
        restore_saving = (daily_reject - restored_daily_reject) * DAYS_PER_YEAR
        actions.append(Action(
            "restore",
            "Get the unit serviced back to its rating",
            restore_saving,
            f"At {target_label}, the same {daily:g} litres a day of drinking water would send "
            f"{restored_daily_reject:.1f} litres a day to the drain instead of {daily_reject:.1f}. "
            "Ask the technician to check the membrane and the reject flow restrictor, since both set this ratio. "
            "Repeat the bucket test after the visit and log both.",
            sources=("is16240", "gsr724"),
        ))

    if readings.reusable_l_per_day is not None and readings.reusable_l_per_day > 0:
        reuse_daily = min(restored_daily_reject, readings.reusable_l_per_day)
        cap_note = (
            "That is all of the reject water."
            if reuse_daily >= restored_daily_reject - 1e-9
            else f"That is the {readings.reusable_l_per_day:g} litres a day you said you can use."
        )
    else:
        reuse_daily = restored_daily_reject
        cap_note = "Assumes the household can use all of it. Enter a daily figure to cap this."
    uses = "floor cleaning, toilet flushing and vehicle washing"
    if plant == "none":
        uses += ", and plants"
    actions.append(Action(
        "reuse",
        "Catch the reject hose in a bucket and use it",
        reuse_daily * DAYS_PER_YEAR,
        f"{reuse_daily:.1f} litres a day replaces tap water for {uses}, the uses CPCB lists. {cap_note}",
        sources=("cpcb2026", "gsr724"),
    ))

    combined = restore_saving + reuse_daily * DAYS_PER_YEAR

    right_size = None
    if readings.feed_tds is not None and feed_cls == "acceptable":
        right_size = annual
        actions.append(Action(
            "right_size",
            "Ask whether you need RO at all",
            annual,
            "Your tap water is within the IS 10500 acceptable TDS limit. If a lab test at a TWAD Board or other "
            "accredited lab also clears germs and chemicals, a purifier without RO, or the non-RO mode many units have, "
            "sends nothing to the drain. Do not remove the RO on a TDS pen reading alone. The NGT directed a ban on RO "
            "below 500 mg/L in 2019, but the Supreme Court stayed the follow-up direction, so this is advice, not law.",
            conditional=True,
            sources=("is10500", "ngt134", "sc_stay"),
        ))

    actions.sort(key=lambda a: (a.conditional, -a.litres_per_year))

    if readings.water_source == "metrowater":
        notes.append(
            "Water supply agencies are required to tell consumers the TDS of the water they supply (G.S.R. 724(E), "
            "rule 4(1)). Ask Metrowater for your area's figure and compare it with your pen."
        )

    return Result(
        readings=readings,
        recovery=r,
        recovery_low=low,
        recovery_high=high,
        reject_per_litre=rpl,
        daily_reject_l=daily_reject,
        annual_reject_l=annual,
        production_lph=production,
        reject_tds=rej_tds,
        reject_tds_is_upper_bound=upper,
        plant_class=plant,
        feed_class=feed_cls,
        checks=tuple(checks),
        actions=tuple(actions),
        combined_litres_per_year=combined,
        right_size_litres_per_year=right_size,
        notes=tuple(notes),
    )


def compare(first_annual_l: float, latest_annual_l: float) -> float:
    """Measured change in litres a year between two logged tests (positive is saved)."""
    return first_annual_l - latest_annual_l
