import itertools
import math

import pytest

from michaneer import model
from michaneer.model import InputError, Readings, evaluate


def test_recovery_from_bucket():
    assert model.recovery(1000, 3000) == pytest.approx(0.25)
    assert model.recovery(1000, 1000) == pytest.approx(0.5)


def test_bounds_contain_point_and_collapse_without_error():
    r = model.recovery(1000, 2400)
    low, high = model.recovery_bounds(1000, 2400, 100)
    assert low < r < high
    assert model.recovery_bounds(1000, 2400, 0) == pytest.approx((r, r))


def test_bounds_widen_with_coarser_jug():
    fine = model.recovery_bounds(1000, 2400, 50)
    coarse = model.recovery_bounds(1000, 2400, 200)
    assert coarse[0] < fine[0] and coarse[1] > fine[1]


def test_reject_per_litre():
    assert model.reject_per_litre(0.25) == pytest.approx(3.0)
    assert model.reject_per_litre(0.4) == pytest.approx(1.5)
    with pytest.raises(InputError):
        model.reject_per_litre(0)


@pytest.mark.parametrize("feed,r,rej", list(itertools.product([50, 300, 499, 1200, 4000], [0.15, 0.25, 0.4, 0.6, 0.75], [0.8, 0.9, 0.97])))
def test_mass_balance_closes(feed, r, rej):
    product = feed * (1 - rej)
    reject, upper = model.reject_tds(feed, r, product)
    assert not upper
    salt_in = feed * 1.0
    salt_out = product * r + reject * (1 - r)
    assert salt_out == pytest.approx(salt_in)
    assert reject >= feed


def test_reject_tds_upper_bound_without_product():
    value, upper = model.reject_tds(400, 0.25, None)
    assert upper
    assert value == pytest.approx(400 / 0.75)
    estimate, _ = model.reject_tds(400, 0.25, 20)
    assert estimate < value


@pytest.mark.parametrize("tds,cls", [(0, "none"), (449.9, "none"), (450, "slight"), (2000, "slight"), (2000.1, "severe")])
def test_fao_classes(tds, cls):
    assert model.fao_class(tds) == cls


@pytest.mark.parametrize("tds,cls", [(120, "acceptable"), (500, "acceptable"), (501, "permissible"), (2000, "permissible"), (2001, "above")])
def test_is10500_classes(tds, cls):
    assert model.tds_class(tds) == cls


def test_annual_reject():
    assert model.annual_reject_l(30, 0.25) == pytest.approx(30 * 3 * 365)


def test_max_feed_for_plants_matches_mass_balance():
    for r in (0.25, 0.4, 0.6):
        feed = model.max_feed_for_plants(r, 0.95)
        reject, _ = model.reject_tds(feed, r, feed * 0.05)
        assert reject == pytest.approx(model.FAO_NONE_BELOW)


def base(**kw):
    values = dict(reject_ml=3000, purified_ml=1000, jug_resolution_ml=50, daily_purified_l=30)
    values.update(kw)
    return Readings(**values)


def test_evaluate_headline_numbers():
    res = evaluate(base())
    assert res.recovery == pytest.approx(0.25)
    assert res.daily_reject_l == pytest.approx(90)
    assert res.annual_reject_l == pytest.approx(32850)
    assert res.annual_cans == pytest.approx(32850 / 20)


def test_restore_targets_label_then_floor():
    res = evaluate(base(rated_recovery_pct=40))
    restore = next(a for a in res.actions if a.key == "restore")
    assert restore.litres_per_year == pytest.approx(30 * (3 - 1.5) * 365)
    res2 = evaluate(base(rated_recovery_pct=50))
    restore2 = next(a for a in res2.actions if a.key == "restore")
    assert restore2.litres_per_year == pytest.approx(30 * (3 - 1) * 365)
    res3 = evaluate(base())
    assert next(a for a in res3.actions if a.key == "restore").litres_per_year == pytest.approx(30 * 1.5 * 365)


def test_no_restore_when_unit_meets_rating():
    res = evaluate(base(reject_ml=1200, rated_recovery_pct=45))
    assert "restore" not in {a.key for a in res.actions}


def test_reuse_is_capped_by_household_and_counts_after_restore():
    res = evaluate(base(rated_recovery_pct=40, reusable_l_per_day=20))
    reuse = next(a for a in res.actions if a.key == "reuse")
    assert reuse.litres_per_year == pytest.approx(20 * 365)
    res2 = evaluate(base(rated_recovery_pct=40, reusable_l_per_day=500))
    reuse2 = next(a for a in res2.actions if a.key == "reuse")
    assert reuse2.litres_per_year == pytest.approx(45 * 365)  # 30 L/day at 40 percent
    # restore plus full reuse removes all of today's reject, never more
    assert res2.combined_litres_per_year == pytest.approx(res2.annual_reject_l)


def test_combined_never_exceeds_current_reject():
    for reject in (500, 1500, 3000, 6000):
        for reuse in (None, 0, 5, 50, 5000):
            for rated in (None, 30, 40, 60):
                res = evaluate(base(reject_ml=reject, reusable_l_per_day=reuse, rated_recovery_pct=rated))
                assert res.combined_litres_per_year <= res.annual_reject_l + 1e-6


def test_right_size_only_below_500_and_conditional():
    low = evaluate(base(feed_tds=300, product_tds=20))
    action = next(a for a in low.actions if a.key == "right_size")
    assert action.conditional
    assert action.litres_per_year == pytest.approx(low.annual_reject_l)
    assert low.actions[-1].key == "right_size"  # conditional steps sort last
    high = evaluate(base(feed_tds=900, product_tds=40))
    assert "right_size" not in {a.key for a in high.actions}
    assert high.right_size_litres_per_year is None


def test_plants_follow_reject_tds_not_feed_tds():
    # feed 420 is under FAO's 450 line, but the reject stream is not
    res = evaluate(base(feed_tds=420, product_tds=35))
    assert res.reject_tds == pytest.approx((420 - 0.25 * 35) / 0.75)
    assert res.plant_class == "slight"
    reuse = next(a for a in res.actions if a.key == "reuse")
    assert "plants" not in reuse.detail


def test_never_claims_water_is_safe_and_marks_stayed_direction():
    res = evaluate(base(feed_tds=250, product_tds=15, water_source="metrowater"))
    text = " ".join([c.text for c in res.checks] + [a.detail for a in res.actions] + list(res.notes)).lower()
    assert "safe to drink" not in text
    assert "not a safety verdict" in text
    assert "stayed" in text
    assert "lab test" in text


@pytest.mark.parametrize("kw,fragment", [
    (dict(purified_ml=50), "Purified water collected"),
    (dict(feed_tds=100, product_tds=300), "swapped"),
    (dict(rated_recovery_pct=0), "Rated recovery"),
    (dict(water_source="river"), "water source"),
    (dict(daily_purified_l=0), "Daily purified"),
])
def test_validation_messages(kw, fragment):
    with pytest.raises(InputError) as err:
        evaluate(base(**kw))
    assert fragment.lower() in str(err.value).lower()


def test_production_rate():
    res = evaluate(base(seconds=240))
    assert res.production_lph == pytest.approx(15.0)


def test_label_check_uses_error_range():
    res = evaluate(base(reject_ml=1500, jug_resolution_ml=100, rated_recovery_pct=40))
    label = next(c for c in res.checks if c.label == "Label")
    assert label.status == "info"  # 40 percent is inside the jug error band
    res2 = evaluate(base(reject_ml=3000, rated_recovery_pct=40))
    assert next(c for c in res2.checks if c.label == "Label").status == "bad"


def test_results_are_finite():
    res = evaluate(base(reject_ml=0))
    assert res.recovery == 1.0
    assert math.isfinite(res.annual_reject_l) and res.annual_reject_l == 0
