"""Michaneer web app: server-rendered pages, no client framework."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import model, store
from .model import InputError, Readings
from .sources import SHORT, SOURCES, by_id

HERE = Path(__file__).resolve().parent

app = FastAPI(title="Michaneer", docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
templates = Jinja2Templates(directory=HERE / "templates")

FIELDS = (
    "reject_ml", "purified_ml", "jug_resolution_ml", "daily_purified_l", "seconds",
    "feed_tds", "product_tds", "rated_recovery_pct", "reusable_l_per_day", "water_source",
)
OPTIONAL = {"seconds", "feed_tds", "product_tds", "rated_recovery_pct", "reusable_l_per_day"}
LABELS = {
    "reject_ml": "Reject water in the bucket",
    "purified_ml": "Purified water collected",
    "jug_resolution_ml": "Jug marking interval",
    "daily_purified_l": "Purified water used a day",
    "seconds": "Seconds to fill",
    "feed_tds": "Tap water TDS",
    "product_tds": "Purified water TDS",
    "rated_recovery_pct": "Rated recovery on the label",
    "reusable_l_per_day": "Litres you can reuse a day",
}

# Clearly labelled demo input. The reject reading is the top of the official
# range (3 litres per litre, Lok Sabha answer 778 of 2020); the other values are
# illustrative, not a measurement.
EXAMPLE = {
    "reject_ml": "3000", "purified_ml": "1000", "jug_resolution_ml": "50",
    "daily_purified_l": "30", "seconds": "240", "feed_tds": "420", "product_tds": "35",
    "rated_recovery_pct": "40", "reusable_l_per_day": "60", "water_source": "metrowater",
}


def parse(data: dict[str, str]) -> Readings:
    values: dict[str, object] = {}
    for name in FIELDS:
        raw = (data.get(name) or "").strip()
        if name == "water_source":
            values[name] = raw or "mixed"
            continue
        if raw == "":
            if name in OPTIONAL:
                continue
            if name == "reject_ml":
                raise InputError("Enter how much reject water collected in the bucket.")
            continue  # use the dataclass default
        try:
            number = float(raw.replace(",", ""))
        except ValueError as exc:
            raise InputError(f"{LABELS[name]} must be a number.") from exc
        if number != number or number in (float("inf"), float("-inf")):
            raise InputError(f"{LABELS[name]} must be a number.")
        values[name] = number
    readings = Readings(**values)  # type: ignore[arg-type]
    readings.validate()
    return readings


def query_of(readings: Readings) -> str:
    pairs = {k: ("" if v is None else (f"{v:g}" if isinstance(v, float) else v)) for k, v in asdict(readings).items()}
    return urlencode({k: v for k, v in pairs.items() if v != ""})


def litres(value: float) -> str:
    if value >= 100:
        return f"{value:,.0f}"
    return f"{value:,.1f}"


templates.env.filters["litres"] = litres
templates.env.globals["source"] = by_id
templates.env.globals["short"] = SHORT


def page(request: Request, name: str, status_code: int = 200, **context) -> HTMLResponse:
    return templates.TemplateResponse(request, name, context, status_code=status_code)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, example: int = 0):
    form = EXAMPLE if example else {k: v for k, v in request.query_params.items() if k in FIELDS}
    return page(request, "home.html", form=form, sources_of_water=model.SOURCES_OF_WATER,
                who=model.WHO_DRINK_COOK_L_PER_PERSON, example=bool(example))


@app.get("/result", response_class=HTMLResponse)
def result(request: Request):
    data = dict(request.query_params)
    try:
        readings = parse(data)
        res = model.evaluate(readings)
    except InputError as err:
        return page(request, "home.html", status_code=422, form=data, error=str(err),
                    sources_of_water=model.SOURCES_OF_WATER, who=model.WHO_DRINK_COOK_L_PER_PERSON,
                    example=False)
    return page(request, "result.html", r=res, query=query_of(readings),
                example=data == {k: v for k, v in EXAMPLE.items()},
                source_name=model.SOURCES_OF_WATER[readings.water_source])


@app.get("/card", response_class=HTMLResponse)
def card(request: Request):
    try:
        readings = parse(dict(request.query_params))
    except InputError as err:
        return page(request, "message.html", status_code=422, title="Cannot make the card", text=str(err))
    return page(request, "card.html", r=model.evaluate(readings))


@app.post("/log")
async def log_add(request: Request):
    form = dict(await request.form())
    label = str(form.pop("label", ""))
    try:
        readings = parse({k: str(v) for k, v in form.items()})
    except InputError as err:
        return page(request, "message.html", status_code=422, title="Not saved", text=str(err))
    store.add(readings, label)
    return RedirectResponse("/log", status_code=303)


@app.post("/log/{entry_id}/delete")
def log_delete(entry_id: int):
    store.delete(entry_id)
    return RedirectResponse("/log", status_code=303)


@app.get("/log", response_class=HTMLResponse)
def log_view(request: Request):
    entries = store.all_entries()
    change = None
    if len(entries) >= 2:
        first, latest = entries[0], entries[-1]
        daily = latest.readings.daily_purified_l
        before = model.annual_reject_l(daily, first.recovery)
        after = model.annual_reject_l(daily, latest.recovery)
        change = {
            "first": first, "latest": latest, "daily": daily,
            "before": before, "after": after, "saved": model.compare(before, after),
        }
    rows = [(e, query_of(e.readings)) for e in entries]
    return page(request, "log.html", rows=rows, change=change)


@app.get("/how", response_class=HTMLResponse)
def how(request: Request):
    return page(request, "how.html")


@app.get("/sources", response_class=HTMLResponse)
def sources(request: Request):
    return page(request, "sources.html", sources=SOURCES)


@app.get("/healthz")
def healthz():
    return {"ok": True}
