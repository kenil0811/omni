# Reference implementations — oracle self-test only

These are hand-written Apps that satisfy the fixture briefs. They exist for one
reason: to prove the oracles and the SDK harness are correct before the
experiment runs. An oracle that has never passed anything is not evidence.

They are **never** shown to the Builder, never copied into
`templates/python-app/`, and never counted as an EXP-BUILDER result. The runner
does not read this directory.

Validate the oracles with:

```bash
just check-oracles
```

If a brief changes, update the reference and re-run, so a broken oracle is
caught here instead of being blamed on the Builder.
