# Devpost submission: Michaneer

Everything below is ready to paste into the Green Shift Hacks project form. Deadline: 17 November 2026, 10:00 PM UTC, which is **Wednesday 18 November 2026, 03:30 IST**. Plan to submit a day early.

Required by the rules (see RULES.md): a project story covering the problem, intended users, approach, expected environmental benefit, tools and limitations; all team members; a demo video or walkthrough; source code or clear build instructions.

## Project name

Michaneer

## Tagline (short pitch)

A ten minute bucket test that shows how many litres your RO purifier pours down the drain, and a plan that wins them back.

## Team members

Vignesh S (solo).

## Links

* Try it live: https://michaneer.140-245-16-129.sslip.io (press "Fill example readings", then "See my result")
* Source code: [GITHUB REPO LINK]
* Demo video: https://youtu.be/M_3_X_DmRPQ
* Or run it locally with three commands (see "How to run it" below). No keys or accounts needed.

## Built with

python, fastapi, jinja2, uvicorn, sqlite, html, css, pytest, modal

## Project story

### Inspiration

In Chennai, RO purifiers sit on kitchen walls and in college hostels, and each one has a thin hose running into the sink or the drain. As a final-year student here I have drunk from them for years without once asking how much water leaves through that second hose. When I looked, the official answer was "it depends": a Lok Sabha reply in 2020 said the reject is "1 to 3 litre per litre of permeate depending on the size and purpose of RO system", and that no study had been done. A factor of three is the difference between a careful household and a wasteful one, and the only way to know which one you are is to measure.

### The problem

RO purifiers push water through a membrane and flush the salts away in a reject stream. For one person drinking and cooking with about 7.5 litres a day (the WHO figure), the official range works out to between 2,738 and 8,212 litres a year going to the drain. Chennai buys water by the tanker lorry every dry summer, so this is drinking-grade water being thrown away in a city that runs short of it.

The rules have caught up. The Environment Ministry's notification G.S.R. 724(E) of October 2021 says users "shall comply with the guidelines issued by CPCB for management, storage, utilisation and disposal of reject water", and every purifier label must now state its rated recovery. CPCB published those guidelines on 23 September 2026: reuse reject water as far as possible for floor cleaning, toilet flushing and vehicle washing. BIS raised the minimum recovery for new purifiers from 20 to 40 percent in IS 16240:2023. Households are now expected to manage reject water, but nobody has given them a way to see how much they make or whether their unit meets its own label.

### Intended users

A Chennai family with an RO unit above the kitchen sink, on Metrowater pipes, a borewell or tanker water. Also the person who runs a hostel or office RO plant, where the same arithmetic applies at a larger scale.

### What it does

1. **Bucket test.** Empty the purifier's tank, keep the tap open, and catch one litre of purified water in a bottle while the reject hose runs into a bucket. Measure the bucket with a kitchen jug. Optional extras: a TDS pen reading of tap and purified water, the seconds it took, and the rated recovery from the label.
2. **Result.** Your recovery, with an error range from your jug's markings; litres of reject a day and a year; and checks against your label, the BIS 40 percent floor, the IS 10500 dissolved-solids limits, and FAO's irrigation classes for the reject water itself.
3. **A plan, biggest saving first,** with litres a year for each step: get the unit serviced back to its rating; catch the reject in a bucket for the uses CPCB lists, capped at what your household can actually use; and, only when tap water is within 500 mg/L and a lab test agrees, ask whether you need RO at all.
4. **A log** of your tests. Save one "before service" and one "after service", and Michaneer shows the measured change in litres a year at the same daily use.
5. **A kitchen card** in English and Tamil to print and stick above the purifier, so the whole family knows what the bucket is for.

### Expected environmental benefit

The benefit is fresh water that stops going down the drain, measured on the household's own unit.

* For one person at 7.5 litres a day, a purifier at the top of the official range (3 litres of reject per litre) sends 8,212 litres a year to the drain. Bringing it up to the 2023 BIS floor of 40 percent cuts that to 4,106 litres. Catching the remainder for mopping and flushing replaces tap water that would otherwise be drawn for those jobs.
* In the built-in example (a family using 30 litres a day, purifier at 25 percent against a 40 percent label), servicing saves 16,425 litres a year and reusing the rest saves another 16,425, which together account for all 32,850 litres the unit was wasting.
* Because the log stores real before and after tests, a household can show the saving it actually achieved instead of an estimate.

We do not claim a city-wide total, because no public count of RO purifiers in Chennai exists.

### How we built it

A Python web app (FastAPI with server-rendered Jinja2 pages and one CSS file). All arithmetic is in one small module: recovery from the bucket readings, an error range from half a jug marking, reject TDS from a salt balance, and the plan. Every threshold in the code points to a source on the app's Sources page. Test readings are stored in a local SQLite file. There are no external services, no keys and no network calls when it runs. The public demo runs the same code on one small Modal container; there the log is kept in memory for each browser and never written to disk.

### Evaluation

The repository includes an evaluation script that uses only published figures:

* The salt balance closes to 1.5e-16 relative error across 400 combinations of tap TDS, recovery and membrane rejection.
* A jug marked every 100 mL pins recovery within 3.6 percentage points, so the test always tells a 25 percent unit from a 40 percent unit.
* At 25 percent recovery, tap water above about 342 mg/L already produces reject water outside FAO's no-restriction class for irrigation. The common tip "pour it on your plants" is only right for low-TDS water, so Michaneer decides from the reject TDS it computes and assumes the worst case when a reading is missing.

130 automated tests cover the arithmetic, class boundaries, validation, the log, the Tamil card, and a check that no page loads third-party scripts.

### Challenges we ran into

* **Getting the test right.** Most home purifiers fill a storage tank and the tap drinks from the tank, so a naive test measures stored water and makes any purifier look perfect. The method now starts by emptying the tank so the stream from the tap is the membrane's live output.
* **Not overclaiming the law.** The NGT directed a ban on RO below 500 mg/L, but the Supreme Court stayed the follow-up direction. The app presents it as a stayed direction and treats right-sizing as advice that needs a lab test, never as a rule.
* **Safety.** A TDS pen cannot detect germs, fluoride, nitrate or arsenic. Michaneer never says water is safe to drink, and a test checks that no output contains that phrase.

### Accomplishments we are proud of

Turning a vague "RO wastes water" into a number a family can measure in ten minutes, with every threshold traceable to a standard, notification or report. And the plant finding: the reject from ordinary tap water is often saltier than FAO's comfortable limit for irrigation, which most reuse advice ignores.

### What we learned

Measured data beats a typical figure when the typical figure has a threefold spread. Regulations already ask households to manage reject water; the missing piece was a way to see it. And a simple salt balance answers practical questions, like whether reject water is fine for plants, better than a rule of thumb.

### Limitations

* One bucket test is one moment. Recovery changes with inlet pressure, temperature and filter age, so the app asks for repeat tests.
* The numbers in our evaluation come from published figures and grids, not from a field study of many homes.
* We cite the CPCB 2026 guidelines from a regulatory summary and the Lok Sabha answer as indexed, because neither original PDF loaded from our network.
* The public demo keeps each browser's log in server memory only, so it is wiped whenever the demo restarts. A household that wants a lasting log runs Michaneer on its own computer, where the log is a local SQLite file.

### What's next

A hostel mode that logs the daily meter readings of a large RO plant, and a short field trial with a few Chennai households, each logging a before and after test.

## Work done during the event

The event period is 19 October to 17 November 2026. Michaneer is a new repository started on 6 November 2026; all code, data tables, the logo and documents were created after that date, as the git history shows. Open-source libraries (FastAPI, Jinja2, Uvicorn, pytest) are used under their licences.

## Data and credits

Public sources only, all credited in the app and README: BIS IS 10500:2012; BIS IS 16240:2023; MoEF&CC G.S.R. 724(E) of 4 October 2021; CPCB reject-water guidelines of 23 September 2026; Lok Sabha Unstarred Question 778 of 17 September 2020; NGT O.A. 134/2015 orders of 20 May 2019 and 1 December 2021 and the Supreme Court stay reported 1 March 2022; FAO Irrigation and Drainage Paper 29 Rev. 1; WHO, Domestic Water Quantity, Service Level and Health (2003).

[AI-ASSISTANCE CREDITS LINE]

## How to run it

```sh
cd michaneer
uv sync
uv run uvicorn michaneer.app:app --port 8000
```

Open http://127.0.0.1:8000, press "Fill example readings", then "See my result". The same app is live at https://michaneer.140-245-16-129.sslip.io.

## Screenshots to upload (docs/screenshots)

1. `1-home.png`: the bucket test steps and form with example readings.
2. `2-result.png`: result with recovery, litres a year, checks and the ranked plan.
3. `3-log.png`: before and after log showing the measured change (example entries, labelled as such).
4. `4-kitchen-card.png`: the printable English and Tamil kitchen card.
5. `5-sources.png`: every threshold and where it comes from.
6. `6-result-mobile.png`: the result on a phone-width screen.

## Optional but strongest: the owner's own bucket test

If there is time before submitting, run the test on the purifier at home, save "before" in the log, and if the unit gets serviced or the reject hose goes into a bucket, save "after". Add a short section here titled "Our own purifier" with the real readings, kept separate from the evaluation figures above. Do not put any reading in the story that was not actually measured.
