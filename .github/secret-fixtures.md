# Reviewed secret-scan fixtures

The initial source scan reported 17 generic-api-key matches in two synthetic data files. Each value was independently checked against deterministic encryption test vectors. They are a 16-byte hex pattern and its 32-byte repetition, not account credentials or service tokens.

Reviewed value SHA-256 digests:

- `9f9f5111f7b27a781f1f1ddde5ebc2dd2b796bfc7365c9c28b548e564176929f`
- `3eb1bd439947eb762998e566ccc2e099c791118b2f40579cc4f7da2b5061b7f9`

The `.gitleaksignore` file records only exact immutable commit/file/rule/line fingerprints for those reviewed findings. No directory, file type or detector rule is disabled. Any new value or location remains subject to normal scanning. The GitHub workflow scans full history with redacted output.
