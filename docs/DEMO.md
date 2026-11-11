# Michaneer: 2 minute demo script

Target length 2:00. Screen recording of the app at 1280 px wide, with voice over. Captions: paste the voice-over lines as the transcript.

## Before recording

Record on the hosted demo, https://michaneer.140-245-16-129.sslip.io, in a fresh browser profile so the log starts empty. To record locally instead:

```sh
cd michaneer
uv sync
MICHANEER_DB=/tmp/michaneer-demo.db uv run uvicorn michaneer.app:app --port 8000
```

Open http://127.0.0.1:8000 in a clean browser window. The demo database starts empty.

Best version: film ten seconds of the real bucket test on the purifier at home (bottle under the tap, hose in a bucket, bucket poured into a jug) and use those readings instead of the example. If you do, say "these are our readings" and type them in. If not, use the example button and say it is an example.

## Script

| Time | On screen | Voice over |
| --- | --- | --- |
| 0:00 to 0:15 | Home page, scroll slowly over the heading and the RO drawing | "Every RO purifier in Chennai has a second hose. Officially it sends 1 to 3 litres to the drain for every litre you drink. That's a factor of three, and nobody knows where their own unit sits. Michaneer measures it." |
| 0:15 to 0:35 | Point at the four steps, then click "Fill example readings" | "The test takes ten minutes. Empty the tank, keep the tap open, catch one litre in a bottle while the reject hose fills a bucket, and measure the bucket with a kitchen jug. A TDS pen and the label's rated recovery make the advice sharper. These are example readings: 3 litres of reject per litre, the top of the official range." |
| 0:35 to 0:55 | Click "See my result". Hover the three numbers and the bar with its 20, 40 and 60 percent marks | "Recovery is 25 percent, with an error range from the jug's markings. That's 90 litres a day and almost 33,000 litres a year down the drain, the 40 percent BIS minimum for new purifiers marked on the bar." |
| 0:55 to 1:15 | Scroll the Checks column, pause on "Reject water TDS" | "The checks compare the unit with its own label and the BIS standard. And here's something most advice gets wrong: the tap water is 420, but the reject stream is about 548 milligrams per litre. By the FAO irrigation table that's not fine for every plant, so Michaneer only suggests plants when the numbers allow it." |
| 1:15 to 1:35 | Scroll the plan, pause on each step and the total | "The plan ranks what to do by litres saved. A service back to the label rating saves 16,000 litres a year. Catching the rest in a bucket for mopping and flushing, the uses CPCB's new guidelines list, saves another 16,000. Dropping RO altogether only appears when tap water is under 500, and only after a lab test. A TDS pen can't see germs or fluoride, and the app never says water is safe to drink." |
| 1:35 to 1:50 | Type "Before service" in the label box, click "Save to my log". Then go back, change reject to 1550, save as "After service". The log shows the measured change | "Save a test before the service and one after, and the log shows what you actually saved, measured on your own purifier, not estimated." |
| 1:50 to 2:00 | Open "Print kitchen card" from the result, then the Sources page for a second | "Print the card in English and Tamil for the kitchen wall. Every threshold links to its source. Michaneer: measure the water you're losing, then win it back." |

## Checks before uploading

* Saying "example readings" out loud if the example button was used.
* No browser tabs, bookmarks or notifications with personal information in frame.
* Video under 3 minutes, captions or transcript attached.
