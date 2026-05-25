# Scripted Examples

This folder contains the local two-client demo used by the root README and the
test suite.

Run the deterministic TCP path:

```bash
python examples/two_client_demo.py --protocol tcp
```

The TCP run signs in Alice and Bob, sends one public message, sends one direct
message, and transfers one small file payload.

Run the UDP path:

```bash
python examples/two_client_demo.py --protocol udp
```

UDP follows the same sign-in and messaging path but skips file transfer because
attachments are intentionally TCP-only.

Expected transcripts live in `examples/expected/` and are checked by
`tests/test_examples.py` after timestamp normalization.
