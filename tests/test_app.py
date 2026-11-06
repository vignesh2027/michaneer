import re

import pytest
from fastapi.testclient import TestClient

from michaneer.app import EXAMPLE, app

client = TestClient(app)


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


@pytest.mark.parametrize("path", ["/", "/?example=1", "/how", "/sources", "/log", "/healthz", "/static/style.css", "/static/logo.svg"])
def test_pages_load(path):
    assert client.get(path).status_code == 200


def test_result_page_shows_headline_and_plan():
    r = client.get("/result", params=EXAMPLE)
    assert r.status_code == 200
    body = text_of(r.text)
    assert "For every litre you drink, 3.0 litres go to the drain" in body
    assert "32,850" in body
    assert "example readings, not a measurement" in body
    assert "Get the unit serviced back to its rating" in body
    assert "Ask whether you need RO at all" in body  # 420 mg/L is within 500


def test_result_right_size_absent_for_high_tds():
    body = text_of(client.get("/result", params=dict(EXAMPLE, feed_tds="900")).text)
    assert "Ask whether you need RO at all" not in body


def test_result_right_size_marked_conditional():
    params = dict(EXAMPLE, feed_tds="300", product_tds="20")
    body = text_of(client.get("/result", params=params).text)
    assert "Ask whether you need RO at all" in body
    assert "only after a lab test" in body


def test_bad_input_returns_form_with_message():
    r = client.get("/result", params={"reject_ml": "abc"})
    assert r.status_code == 422
    assert "must be a number" in r.text
    r2 = client.get("/result", params={"purified_ml": "1000"})
    assert r2.status_code == 422
    assert "reject water" in r2.text


def test_log_round_trip_and_measured_change(temp_db):
    before = dict(EXAMPLE, label="Before service")
    after = dict(EXAMPLE, reject_ml="1500", label="After service")
    assert client.post("/log", data=before, follow_redirects=False).status_code == 303
    assert client.post("/log", data=after, follow_redirects=False).status_code == 303
    body = text_of(client.get("/log").text)
    assert "Before service" in body and "After service" in body
    # 30 L/day: 3.0 L/L before, 1.5 L/L after
    assert "16,425" in body and "Saved a year" in body
    ids = re.findall(r"/log/(\d+)/delete", client.get("/log").text)
    assert len(ids) == 2
    client.post(f"/log/{ids[0]}/delete")
    assert len(re.findall(r"/log/(\d+)/delete", client.get("/log").text)) == 1


def test_log_rejects_bad_readings():
    r = client.post("/log", data={"reject_ml": "-5", "label": "x"})
    assert r.status_code == 422


def test_card_has_tamil_and_english():
    r = client.get("/card", params=EXAMPLE)
    assert r.status_code == 200
    assert 'lang="ta"' in r.text
    assert "குடிக்கவோ சமைக்கவோ பயன்படுத்த வேண்டாம்" in r.text
    assert "Never for drinking or cooking" in r.text


def test_no_third_party_scripts_or_styles():
    for path in ["/", "/how", "/sources", "/log"]:
        html = client.get(path).text
        assert not re.search(r'<script[^>]+src=', html)
        assert not re.search(r'<link[^>]+href="https?://', html)


def test_edit_link_prefills_form():
    r = client.get("/", params={"reject_ml": "2222"})
    assert 'value="2222"' in r.text


def test_sources_page_lists_every_source():
    from michaneer.sources import SOURCES
    html = client.get("/sources").text
    for s in SOURCES:
        assert f'id="{s.id}"' in html
