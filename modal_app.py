"""Optional: deploy Michaneer on Modal (https://modal.com).

The live demo does not use this file; it runs the same app in a small Docker
container on an Oracle Cloud VM (see README, "Hosted demo"). Keep this only if
you have a Modal account and want a scale-to-zero host of your own:

    pip install modal && modal deploy modal_app.py

One small container (a quarter CPU, 256 MB) that scales to zero when idle, so the
first visit after a quiet spell takes a few seconds. In hosted mode each browser's
log is kept in memory only and is lost on restart; nothing is written to disk.
"""

from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("fastapi>=0.162.0", "jinja2>=3.1.6", "python-multipart>=0.0.33")
    .env({"MICHANEER_HOSTED": "1", "MICHANEER_DB": "/tmp/unused.db"})
    .add_local_dir(str(HERE / "michaneer"), "/root/michaneer", ignore=["**/__pycache__"])
)

app = modal.App("michaneer")


@app.function(image=image, cpu=0.25, memory=256, min_containers=0, max_containers=1, scaledown_window=900)
@modal.concurrent(max_inputs=50)
@modal.asgi_app(label="michaneer")
def web():
    import sys

    sys.path.insert(0, "/root")
    from michaneer.app import app as fastapi_app

    return fastapi_app
