# Related SDK comparison and the small-response regression

This review inspected the synchronous search/session components listed below at fixed commits. It was an architectural comparison; these libraries were not installed, executed against railway services, vendored, or used as a dependency. No third-party implementation was transplanted. This is not a repository-wide review or a cross-library latency ranking.

| Project and revision | Reviewed components | Relevant observation |
| --- | --- | --- |
| [pykorail — 759afa802f81](https://github.com/devgyurak/pykorail/tree/759afa802f8108b4af5df6d51d18fa9c97ff0f1c) | [synchronous trains](https://github.com/devgyurak/pykorail/blob/759afa802f8108b4af5df6d51d18fa9c97ff0f1c/src/pykorail/_sync/resources/trains.py), [session](https://github.com/devgyurak/pykorail/blob/759afa802f8108b4af5df6d51d18fa9c97ff0f1c/src/pykorail/_sync/session.py), transport interface | Search/page handling leads to typed train conversion. The synchronous session forwards calls to its existing session object. |
| [korail2 — 5a6593f3093e](https://github.com/carpedm20/korail2/tree/5a6593f3093ee15564d217443bd46e40e8217c17) | [search and client](https://github.com/carpedm20/korail2/blob/5a6593f3093ee15564d217443bd46e40e8217c17/korail2/korail2.py) | Search uses a retained session, decodes JSON, checks the result, constructs train objects and filters them in a direct path. Its legacy protocol and model contract differ from this package. |
| [SRT — 3c0c29bd3b74](https://github.com/ryanking13/SRT/tree/3c0c29bd3b747db05f4a14cce77bbfb408fb4318) | [session construction and search](https://github.com/ryanking13/SRT/blob/3c0c29bd3b747db05f4a14cce77bbfb408fb4318/SRT/srt.py) | A retained requests session is used for search, followed by response and train conversion. NetFunnel and recursive search/continuation behavior are part of its separate service contract. |

The useful common design is a retained transport/session and a short search-to-model path. Session reuse was already present in our implementation; adding another session pool would not explain or fix the measured regression. Different protocol, protection, pagination and response contracts make an SDK-to-SDK network timing comparison inappropriate here.

## Measured cause in this implementation

The retained httpx client still received a relative string endpoint on every exchange. httpx therefore resolved and reconstructed the URL repeatedly. In 2,000 warmed searches, the pre-fix profile recorded **4,000 calls** to `httpx/_urlparse.py:urlparse`. The post-fix profile records **zero calls** to that function in the measured window. The standard-library URL processing used by cookie handling remains; no claim is made that all URL work disappeared.

The common response envelope also passed through the general model decoder after its type fields had already been examined by the HTTP layer. A dedicated envelope decoder now performs scalar validation/conversion and constructs the response in one place. Its raw object and failure classification are preserved.

The changes are in `src/korail_api/transport/http.py` and `src/korail_api/protocol/envelope.py`. The general decoder shares the envelope decoder for base responses. No HTTP status, session, protection, business-error or raw-context check was removed.

## Cache behavior

The endpoint cache stores resolved URL objects, not requests or responses. Its 256-entry bound prevents arbitrary route strings from accumulating indefinitely. Resolution uses httpx's public `build_request` behavior once on a cold endpoint. Headers, cookies, tokens, body fields and query arguments are still rebuilt for each exchange. If client-level query defaults are set, the optimization falls back to normal URL resolution. Changing `client.base_url` invalidates that endpoint's cached resolution.

Tests exercise relative and absolute paths, encoded query values, base prefixes and base changes, global query-default changes, successive cookies, per-request tokens and client-header updates. Transport invocation counts remain exactly one per exchange.

## Result

Three fresh processes per implementation were run in alternating order. Each process recorded five warmed timing samples at each response size. The following numbers are medians across all fifteen samples per size. The comparison uses the same public search calls, JSON payloads, httpx MockTransport and disabled queue for the previous local implementation and the new implementation.

| Returned trains | Previous local implementation | Fixed implementation | Elapsed reduction |
| --- | ---: | ---: | ---: |
| 1 | 328.955 µs | 302.313 µs | 8.10% |
| 10 | 628.011 µs | 509.567 µs | 18.86% |
| 50 | 1,875.887 µs | 1,381.437 µs | 26.36% |

The earlier independent one-row measurement was 382.979 µs. Compared with that recorded run, the current one-row median is about 21% lower. Cross-run percentages are descriptive; the alternating-process comparison above is the primary result.

These are warmed CPU/mock HTTP measurements. A cold endpoint performs its initial resolution once. This result does not establish real server latency, TLS behavior, authentication, queue admission or live reservation success.

## Evidence and reproduction

- `search-comparison.json`: all alternating-process timing samples and aggregate medians.
- `profile-before-endpoint-cache.json`: profile before this fix.
- `profile-after-endpoint-cache.json`: profile after this fix.
- `related-projects.json`: reviewed project revisions and source links.

```sh
PYTHONPATH=src .venv/bin/python tools/performance/profile_search.py
```

The prior two-runtime comparator and original runtime remain in the separate development checkout. The command above profiles only this repository's implementation. Published JSON evidence uses normalized source/dependency path labels; numeric samples are unchanged.
