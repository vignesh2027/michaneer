# Michaneer: design and idea selection

Written on 6 November 2026, before any app code.

## What the judges score

Green Shift Hacks publishes one criterion (see RULES.md):

> **Environmental Impact.** "How clearly the project reduces waste, emissions, resource use, or environmental harm."

The overview adds what the story must cover: "the problem, the intended users, your approach, the expected environmental benefit, the tools you used, and any limitations", and asks entrants to "Think beyond awareness: make sustainability more actionable, measurable, and possible."

So the winning shape is: one real behaviour, a quantity a user can measure, a change that moves that quantity, and an honest account of how sure we are.

## The user

A household in Chennai with a reverse osmosis (RO) purifier on the kitchen wall. The owner is a final-year CSE student in Chennai who has lived with one at home and drunk from the RO plant at college. Every such unit has a second hose that runs to the sink or the drain. Most families have never measured how much leaves through it.

Second user: whoever runs a hostel or office RO plant. The arithmetic is the same at a larger daily volume.

## Five candidate ideas

Each idea is scored 1 to 5 on the verbatim criterion, then on four supporting checks taken from the overview text, then on originality against what is visible. The gallery for this event is unpublished, so originality is judged against Devpost project search, GitHub search, Smart India Hackathon coverage and the sibling Devpost galleries the owner has already studied.

| # | Idea | Environmental Impact (verbatim) | Measurable with public data | Identifiable firsthand user | 2 minute demo | No paid API, no card | Originality | Total /30 |
|---|---|---|---|---|---|---|---|---|
| A | **Michaneer**: an RO reject-water bucket test that measures a household's own recovery ratio and turns it into a ranked reuse and right-sizing plan | 5 | 5 | 5 | 5 | 5 | 4 | **29** |
| B | Hostel mess headcount forecaster to cut cooked-food waste | 4 | 2 | 4 | 3 | 5 | 3 | 21 |
| C | Chennai rooftop rain capture planner from daily rainfall history | 3 | 4 | 3 | 4 | 5 | 2 | 21 |
| D | College commute mode-shift planner (MTC bus, Metro, MRTS) with CO2 per trip | 3 | 3 | 4 | 4 | 5 | 2 | 21 |
| E | E-waste matcher to Tamil Nadu Pollution Control Board authorised recyclers | 3 | 2 | 3 | 4 | 5 | 2 | 19 |

### Why each score

**A. Michaneer.** Impact 5: the output is litres of drinking-grade municipal or ground water that stop going down the drain, measured on the user's own unit, before and after. Public data 5: every threshold comes from an official or standard source (BIS IS 10500:2012, BIS IS 16240:2023, MoEF&CC G.S.R. 724(E), the CPCB reject-water guidelines of 23 September 2026, FAO Irrigation and Drainage Paper 29, a Lok Sabha answer on reject volumes, the NGT order in O.A. 134/2015). User 5: a Chennai home with an RO, lived firsthand. Demo 5: one form, one result, one before and after log. Originality 4: reuse blog posts and hardware hackathon projects exist (SRM's organic filter at Smart India Hackathon 2019, a KCG College boiling unit), but no software tool we could find measures a household's own ratio and builds a plan from it. Not a perfect 5 because "reuse RO water" as advice is widely known.

**B. Mess forecaster.** Impact 4, since cooked-food waste carries large emissions. But no public mess attendance data exists, so the demo would need numbers we made up, which the brief forbids. Food-waste trackers are common in student galleries.

**C. Rain capture planner.** Rainwater harvesting has been mandatory for Chennai buildings since 2003, so the marginal behaviour change is small, and the output is a potential, not a measured saving. RWH calculators are plentiful.

**D. Commute planner.** Carbon calculators are the most common sustainability hackathon entry. Emission factors per Chennai mode exist but the behaviour change is hard to verify within a demo.

**E. E-waste matcher.** The recycler list is public, but the impact depends on a trip the user may never make, and locator maps are common entries.

**Not energy.** Ainooru (the owner's LaunchPad entry) forecasts the Tamil Nadu 500 unit electricity cliff. Michaneer is about water volume and never touches electricity tariffs or units, so the two cannot be confused.

## Decision

Build A, named **Michaneer** (from Tamil "michcha neer", leftover water, which is what the reject stream is).

### Name evidence (6 November 2026)

* GitHub repository search for "michaneer", "mitchaneer" and "michcha-neer": 0 results each.
* Web search for "Michaneer": no page uses the word. Results were spelling suggestions for "Michigander".
* Apple App Store search API (term michaneer): 1 fuzzy hit, "Michan" by PT. APP DIGI INDONESIA, unrelated.
* Google Play search for michaneer: no app with that name.
* PyPI `michaneer`: Not Found. npm `michaneer`: 404.
* Devpost project search for "michaneer": total_count 0.

## The facts the product stands on

All verified on 6 November 2026. Full citations live in `michaneer/sources.py` and render on the app's Sources page.

1. **Reject volumes vary a lot.** A Lok Sabha answer states reject quantity "varies between 1 to 3 litre per litre of permeate depending on the size and purpose of RO system", and that the ministry had not carried out a study. So a household cannot know its own ratio without measuring it. That gap is the product.
2. **Minimum recovery is now 40 percent.** BIS IS 16240:2023 raised the minimum recovery of domestic RO purifiers from 20 percent (2015 edition) to 40 percent. Units bought before the change may legally be lower.
3. **The label must state it.** MoEF&CC notification G.S.R. 724(E), 4 October 2021 (Environment (Protection) 115th Amendment Rules), requires every domestic purifier to carry a conformance label with "Rated recovery efficiency and corresponding water reject generation". Users can compare the label with their own measurement.
4. **Users must manage reject water.** The same notification says "The user shall comply with the guidelines issued by CPCB for management, storage, utilisation and disposal of reject water". CPCB issued those guidelines on 23 September 2026. They say reject water should be reused to the maximum extent for non-potable purposes such as floor cleaning, vehicle washing and toilet flushing.
5. **RO is for dissolved solids.** BIS IS 10500:2012 sets 500 mg/L TDS as the acceptable limit and 2000 mg/L as permissible in the absence of an alternate source. The NGT (O.A. 134/2015, order of 20 May 2019) directed a ban on RO where TDS is below 500 mg/L. The Supreme Court stayed the follow-up NGT direction of 1 December 2021. Michaneer reports the NGT direction as a direction that is stayed, never as law.
6. **Not all reject water is good for plants.** FAO Irrigation and Drainage Paper 29 Rev. 1, Table 1, classes irrigation water by TDS: under 450 mg/L no restriction, 450 to 2000 slight to moderate, over 2000 severe. Reject water is more concentrated than feed water, so "water your plants with it" is not always right. Michaneer computes the reject TDS by mass balance and says which class it falls in.
7. **How much a home drinks.** WHO (Howard and Bartram, 2003) estimates about 7.5 litres per person per day for drinking and food preparation. Michaneer uses this only as a hint beside an input the user can change.

## What the app does

1. **Bucket test.** Put a 1 litre bottle under the purified tap and a bucket under the reject hose. Start both together, stop when the bottle is full, read the bucket with a measuring jug. Optional: TDS pen readings of tap water and purified water, the label's rated recovery, and the seconds the bottle took.
2. **Result.** Recovery percent with a measurement range from the jug resolution, litres of reject per day and per year, reject TDS and its FAO class, and checks against the label, the BIS 40 percent floor and the IS 10500 TDS limits.
3. **Plan.** Three actions, each with litres saved per year, ranked:
   * Reuse: route reject water into a bucket for the CPCB uses, up to the litres per day the household says it can use.
   * Restore: if measured recovery is below the label or the 40 percent floor, the litres a service visit would save if it restored the rated figure.
   * Right-size: if tap TDS is within 500 mg/L, the litres saved by asking whether a non-RO mode fits, conditional on a lab test, since a TDS pen cannot detect microbes, fluoride, nitrate or arsenic.
4. **Log.** Save each test with a label such as "before service" and "after service". The log shows the measured change between the first and latest test in litres per year. This is the measurable part the brief asks for.
5. **Kitchen card.** A printable card for the wall above the purifier with the numbers and the reuse rules, in English and Tamil.

## Stack

Python 3.12 with uv, FastAPI, Jinja2 server-rendered HTML, one CSS file, no client framework, a few lines of inline JS at most. SQLite for the local log. No LLM: every number is arithmetic on the user's own readings and published thresholds, so a model adds risk and no accuracy. No paid API, no network calls at runtime.

Theme: background #F4F9FF, surface #FFFFFF, primary #2563EB, text #0B1B33, accent deep violet #4C1D95, danger #9F1239.

## Evaluation plan

`eval/run_eval.py` writes `eval/RESULTS.md` from public numbers only:

1. Mass balance closes for every point on a grid of feed TDS, recovery and salt rejection.
2. Litres sent to drain per person per year across the official range (Lok Sabha 1 to 3 litres reject per litre, BIS 20 and 40 percent floors, NGT 60 percent direction), using the WHO 7.5 litre figure.
3. How precise a kitchen bucket test is: recovery error from jug resolution, and whether the test can tell a 25 percent unit from a 40 percent unit.
4. The highest tap-water TDS for which reject water stays in FAO's no-restriction class, at each recovery level, which tests the common "use it on plants" advice.

## Limits we will state

* The bucket test measures one moment. Recovery drifts with water pressure, temperature and filter age, so the app recommends repeating it.
* A TDS pen measures dissolved solids only. Michaneer never says water is safe to drink and never advises removing an RO without a lab test.
* Savings are what the household's own readings imply. We do not estimate how many homes in Chennai own an RO, because no public count exists.
