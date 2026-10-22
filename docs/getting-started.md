# Installation and usage

Use Python 3.11 or newer. From a checkout of the current source:

```sh
python -m venv .venv
.venv/bin/python -m pip install '.[socks]'
```

For an existing environment, uninstall `korail-mobile-api` before installing `korail-api`. They provide the same compatibility namespace and must not coexist. The new development version is not yet published to PyPI.

Existing imports remain supported:

```python
from korail_mobile_api import KorailClient, KorailConfig, TrainSearchQuery
```

New code can use the canonical namespace:

```python
from korail_api import KorailClient, TrainSearchQuery

with KorailClient() as client:
    response = client.search_trains(TrainSearchQuery("서울", "부산", "20991230", "090000"))
    for train in response.trains:
        print(train.train_no, train.departure_time)
```

Replace the example date with a valid travel date. Executing this example sends a real schedule request; automated tests do not execute it. Always close clients or use a context manager to release their transports.

For local development:

```sh
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
```

Tests use mock transports. A transaction response that cannot be decoded retains whole-response context in `error.raw` and nested context in `error.parser_raw` when available. Do not automatically retry a reservation or payment after an ambiguous outcome. Handle a business rejection separately from a malformed response or expired session.

The root `CONTRIBUTING.md` documents compatibility comparisons, isolated artifact checks and documentation builds. The [validation record](VALIDATION.md) lists observed results and limitations.
