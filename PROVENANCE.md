# Implementation provenance

## Scope and authorship

The code in `src/korail_api/` was written for this implementation. Its architecture separates schema-directed requests and decoding, generated value objects, session state, queue admission, HTTP transport and token serialization. `src/korail_mobile_api/` contains compatibility adapters to those engines. There is no dependency on the previous `korail-mobile-api` distribution, no runtime source import from it, and no vendored copy of its Python modules.

Public names, signatures, constructor defaults, field mappings, endpoint paths, wire ordering and synthetic input/output results were observed from the earlier implementation as compatibility facts. The earlier development checkout retained the previous runtime and observation tools as a test oracle. They remain separate and are not included in this repository. Captured synthetic decoder outcomes are retained as development-only data in `tools/validation/observations/`; they are excluded from release artifacts.

This process is **not strict clean-room development**. The same developer had access to the previous source, selected protocol arithmetic and convenience-property behavior were examined, and the original offline tests were used for compatibility verification. No assertion is made that structural changes alone remove copyright obligations. An exact-AST overlap check performed in the previous development checkout was a limited engineering check, not a legal test of independent authorship, substantial similarity or infringement.

## Sources and limits

| Material | Treatment |
| --- | --- |
| Previous public Python interface | Observed signatures, names, types and constructor behavior; new runtime implementation |
| Request and response protocol | Synthetic black-box observations and protocol facts; independent serialization/decoding engines |
| Legacy token arithmetic | Protocol arithmetic examined and reformulated; golden vectors verified |
| Diagnostic token vectors | New serializer checked against known vectors |
| Error message catalog | Extracted directly from a locally available KORAIL application resource, not copied from the previous Python catalog |
| Dependencies | Used as dependencies; their own licenses continue to apply |
| Previous fork and history | Preserved in the separate development checkout; historical license and NOTICE retained here in `licenses/` |

The vendor error catalog was imported from `assets/error_json.json` in a locally available application artifact identified as version `7.0.10`. Its resource SHA-256 is `7b7998f2582217aba20e58a722b3640a6ef3a2751d9816aaf2f78cfc97c74d00`. The importer records 12,430 codes and 19,381 translations. The version label comes from the local artifact context; the artifact's delivery origin was not independently authenticated. The APK and extracted raw vendor files are not distributed. The catalog text remains third-party material; independent extraction does not make its text maintainer-owned or supply a redistribution license.

`tools/catalog/import_messages.py` can regenerate the catalog from a separately supplied local artifact. It reads a ZIP resource and never executes application code. Secrets and application binaries are not bundled.

A subsequent performance review inspected selected search/session components of pykorail, korail2 and SRT at pinned revisions. The comparison record is in `tools/reports/related-projects.md`. No implementation from those projects was copied or added as a dependency. Referring to another repository would not by itself eliminate that repository's licensing obligations.

## Legal boundary

Apache License 2.0 section 4 imposes conditions when distributing the work or derivative works: [license text](https://www.apache.org/licenses/LICENSE-2.0). The US Copyright Office distinguishes methods, systems and ideas from their copyrightable expression: [Circular 33](https://www.copyright.gov/circs/circ33.pdf). These sources do not determine the classification of this implementation or address every applicable jurisdiction.

This package does not certify that all copyright or attribution obligations have ended. Distribution of the old fork, its source or history still requires honoring its applicable notices. The new package's vendor data and dependencies also have separate rights. A conclusive assessment of this package's status would require review of the actual code, development record and third-party materials.

## New repository boundary

The `korail-api_v2` repository begins with the current implementation in a new Git history. The earlier fork's source and Git history were not imported. Creating a new history is a packaging and maintenance decision, not evidence of a legal clean-room process. Applicable original attribution is retained in `NOTICE`, `THIRD_PARTY_NOTICES.md` and `licenses/`. The original development checkout and its notices remain separately preserved.

The historical benchmark JSON reports retain their numeric samples. Host-specific filenames were normalized to `reference-runtime/`, `current-runtime/`, `dependencies/` and `python-stdlib/` labels for publication. Normalization changes path labels, not timing results. Historical compatibility counts are explicitly distinguished from checks runnable in this repository.
