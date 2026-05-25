# Examples

Run the scripted two-client demo against a local server:

```bash
python examples/two_client_demo.py --protocol tcp
```

The TCP demo signs in Alice and Bob, sends one public message, sends one direct
message, and transfers one small file payload. UDP uses the same public/direct
message path but skips file transfer because attachments are intentionally
TCP-only.

Expected transcripts are stored in `examples/expected/` and verified by
`tests/test_examples.py` after timestamp normalization.
