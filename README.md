<p align="center">
  <img src="assets/readme-banner.svg" alt="korail-api — compatible imports, clear boundaries" width="100%">
</p>

# korail-api

> **Legal notice:** This is an unofficial client, unaffiliated with KORAIL. Apache-2.0 covers material the maintainer can license; it grants no service-access or trademark rights. This is not a certified clean-room implementation. Vendor message data has separate rights, and no independent redistribution grant has been established. Read [LEGAL.md](LEGAL.md), [NOTICE](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md) and [provenance](PROVENANCE.md) before use or redistribution.

[![CI](https://github.com/thsqaz123-dot/korail-api_v2/actions/workflows/ci.yml/badge.svg)](https://github.com/thsqaz123-dot/korail-api_v2/actions/workflows/ci.yml)
[![Security](https://github.com/thsqaz123-dot/korail-api_v2/actions/workflows/security.yml/badge.svg)](https://github.com/thsqaz123-dot/korail-api_v2/actions/workflows/security.yml)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Code license: Apache-2.0](https://img.shields.io/badge/Code_license-Apache--2.0-14b8a6)](LICENSE)
[![Status: experimental](https://img.shields.io/badge/Status-experimental-f59e0b)](VALIDATION.md)

A synchronous Python client for the KORAIL protocol, organized around separate transport, protocol, service and model layers. Existing `korail_mobile_api` imports remain compatible with the canonical `korail_api` namespace.

**[Documentation](https://thsqaz123-dot.github.io/korail-api_v2/)** · **[Architecture](ARCHITECTURE.md)** · **[Validation](VALIDATION.md)** · **[Contributing](CONTRIBUTING.md)** · **[Legal notice](LEGAL.md)**

## What it supports

| Area | Capabilities |
| --- | --- |
| Search | Direct and transfer schedules, pagination, continuation recovery, seat maps |
| Sessions | Authentication, cookies, configuration, device profiles and explicit proxies |
| Transactions | Reservations, cancellation, payment and refund operations |
| Resources | Account and ticket reads, travel products and airport limousine operations |
| Compatibility | 239 public root exports, 86 public client methods and existing model imports |

Transaction methods can affect real tickets and money. Automated validation is offline; these capabilities are not a claim of current live-service acceptance.

## Install from source

The distribution is named **`korail-api`**, version **`0.1.0.dev0`**. This development version has not been published to PyPI. The repository name `korail-api_v2` is separate from the Python distribution and import names.

```sh
git clone https://github.com/thsqaz123-dot/korail-api_v2.git
cd korail-api_v2
python -m venv .venv
.venv/bin/python -m pip install '.[socks]'
```

When migrating an existing environment, first uninstall `korail-mobile-api`. Both distributions provide the `korail_mobile_api` namespace and must not coexist in the same environment. Existing application imports can remain unchanged.

## Search example

```python
from korail_api import KorailClient, TrainSearchQuery

with KorailClient() as client:
    response = client.search_trains(TrainSearchQuery("서울", "부산", "20991230", "090000"))
    for train in response.trains:
        print(train.train_no, train.departure_time)
```

Replace the example date with a valid travel date. Executing this example sends a real schedule request; automated tests do not execute it.

Existing code can keep using:

```python
from korail_mobile_api import KorailClient, KorailConfig, TrainSearchQuery
```

## Behavior that matters

- Every search obtains a fresh response; seat availability and transaction outcomes are never cached.
- Transaction requests are never retried automatically. Check uncertain outcomes through official channels before trying again.
- Decode failures retain the whole response in `error.raw`, with nested context in `error.parser_raw` when available. Treat both as potentially sensitive.
- Pagination detects repeated pages and preserves continuation metadata.
- Business rejection, malformed responses, session expiry and protocol-access rejection remain distinct.
- HTTP cookies have one owner; curl responses are adapted without a second decompression pass. Credential and payment fields are hidden from generated model representations.

## Architecture

```text
src/
├── korail_api/
│   ├── api/             Public client and convenience resources
│   ├── services/        Authentication, search and transaction rules
│   ├── protocol/        Request compilation and response decoding
│   ├── transport/       HTTP, curl adaptation and queue admission
│   ├── models/          Value objects, exceptions and type declarations
│   ├── configuration/   Device and environment settings
│   ├── security/        Password transformation and token serialization
│   ├── messages/        Localized message lookup
│   └── resources/       Protocol contracts and vendor message data
└── korail_mobile_api/    Existing import compatibility
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for ownership boundaries and locations for behavioral changes. No previous implementation is required at runtime or during the standalone build.

## Validation and performance

The standalone suite contains **220 offline tests**. Another **1,915 captured synthetic decoder outcomes** are checked by the development validator. During development, **2,459 legacy tests and 36 subtests** passed against this implementation; 37 selected cases were excluded with replacements documented in [VALIDATION.md](VALIDATION.md). The historical test oracle is not included here, and those counts are not the size of this repository's CI suite.

A prior alternating-process benchmark used identical public search calls, mock transports and response payloads:

| Trains per response | Previous local implementation | Current implementation | Elapsed reduction |
| --- | ---: | ---: | ---: |
| 1 | 328.955 µs | 302.313 µs | 8.10% |
| 10 | 628.011 µs | 509.567 µs | 18.86% |
| 50 | 1,875.887 µs | 1,381.437 µs | 26.36% |

These are historical, warmed CPU/mock-HTTP measurements, not live network latency or a comparison of other SDKs. See [the performance investigation](tools/reports/related-projects.md) for methodology and limitations.

## Development

```sh
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
.venv/bin/python tools/validation/check_decoder_equivalence.py
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
.venv/bin/python tools/packaging/check_artifacts.py dist/*.whl --sdist dist/*.tar.gz
```

Tests block network traffic and use synthetic data. See [CONTRIBUTING.md](CONTRIBUTING.md) for documentation builds and packaging boundaries. Do not include credentials, passenger data, payment details or unredacted responses in issues.

## License and provenance

The maintainer-authored software is offered under [Apache-2.0](LICENSE), subject to the scope and notices in [LEGAL.md](LEGAL.md), [NOTICE](NOTICE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Original project attribution is retained. The previous fork and its history are maintained separately and are not included in this repository's Git history.

Source from the previous implementation was visible during development. Reimplementation, renamed files and a new repository do not establish that all copyright or attribution obligations have ended. Third-party data, dependencies, trademarks and service-access permissions remain separate matters. No live login, reservation, cancellation, payment or refund has been used to validate this development version.
