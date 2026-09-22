# E3 Diagnostic

## Status

No valid E3 training result is available. `e3-profile-coupling/STATUS.md` records that the earlier quota-based proposal was paused because it manually selected clients by direction group. That design would not provide a clean natural arrival-process test.

## Required endpoint diagnostic

Before any multi-level scan, the correct diagnostic is a fixed-data, fixed-profile endpoint comparison at rho=0 and rho=1. Client datasets and identities must remain unchanged; only the client-to-delay/profile assignment may change. The complete causal chain must be observed in actual simulator state:

`rho -> profile assigned to client -> service duration -> finish order -> raw buffer -> valid buffer`.

Metadata-only correlation is insufficient. The diagnostic should use a rho-independent fixed reference direction grouping and record population, dispatch, raw-return, valid-buffer, and long-run arrival proportions, plus service-time and staleness summaries. A finite-population sampling null should be reported for Phi and coverage.

## Current evidence

The repository contains no completed rho=0/rho=1 endpoint output with those measurements. Therefore there is no basis for claiming that a five-level rho experiment is justified, nor for claiming monotonic performance with coupling strength.

## Decision

Keep E3 out of the completed results and final numerical claims. A future targeted diagnostic is warranted only if the reviewer requires a within-task coupling-strength answer; it should stop without a formal matrix if the endpoints do not separate in realized arrival-direction statistics.
