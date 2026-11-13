# Michaneer: design notes

Written on 6 November 2026, before any app code.

## The user

A household in Chennai with a reverse osmosis (RO) purifier on the kitchen wall. The owner is a final-year CSE student in Chennai who has lived with one at home and drunk from the RO plant at college. Every such unit has a second hose that runs to the sink or the drain. Most families have never measured how much leaves through it.

Second user: whoever runs a hostel or office RO plant. The arithmetic is the same at a larger daily volume.

## Decision

Build an RO reject-water bucket test, named **Michaneer** (from Tamil "michcha neer", leftover water, which is what the reject stream is).

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

Python 3.12 with uv, FastAPI, Jinja2 server-rendered HTML, one CSS file, no client framework, a few lines of inline JS at most. SQLite for the local log. Every number is plain arithmetic on the user's own readings and published thresholds, with nothing predicted or guessed. No paid API, no network calls at runtime.

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
