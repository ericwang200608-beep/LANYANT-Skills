# Performance verdict report template

Copy the section that fits. Fill every field; write `not checked: <reason>` instead of leaving a field blank. Label each line measured, inferred, or unverified.

## One-off result or comparison

```
Verdict: <faster | slower | no measurable difference | inconclusive>
Claim: <the sentence you would ship, written before the run>
Primary number: <metric> <before> -> <after> <unit> (<delta, percent>)
Runs: <N per side>, alternating A/B; median <x>, range <min> to <max> (before) / <min> to <max> (after)
Limiter: <resource or code path that bounds the result, and how it was found: profile, counters>
Workload: <data size, concurrency, warm/cold state, dataset name>
Environment: <machine, cores, load average at start, build mode, flags, versions>
Tuning: <how each side was configured; "both production settings" or the gap>
Limits check: <arithmetic against bandwidth, cores, or share of runtime>
Errors: <failure count / total, output correctness check>
Work happened: <evidence the timed work ran: rows written, requests served, results used>
End-to-end share: <micro result as a share of the user-facing path, or n/a>
Regression gate: <command> -> <green | red: test>
Artifacts: <paths to baseline and post-fix traces, comparison output>
Candidate: <commit or build>
Gaps: <anything that makes this inconclusive or unverified>
```

### Worked example

```
Verdict: faster
Claim: CSV export is 20% faster at p50 on the 60k-row dataset.
Primary number: export p50 41 ms -> 33 ms (-8 ms, -19.5%)
Runs: 7 per side, alternating; median 41 ms, range 39 to 44 ms (before) / median 33 ms, range 32 to 35 ms (after)
Limiter: JSON parsing on one core (node --cpu-prof, 71% self time in parseRow) [measured]
Workload: fixtures/export-60k.json, single request, warm cache
Environment: 8-core dev machine, load average 0.4, production build, NODE_ENV=production
Tuning: both sides production build and flags; same dataset and versions
Limits check: parseRow took 29 ms of 41 ms; a 8 ms saving is inside that piece [inferred]
Errors: 0/14 runs failed; output byte-identical to baseline export
Work happened: 60,000 rows counted in each output file
End-to-end share: export is 38% of the "download report" request; request p50 108 ms -> 100 ms
Regression gate: npm test -> green
Artifacts: /tmp/perf/export-before.cpuprofile, /tmp/perf/export-after.cpuprofile, /tmp/perf/compare.txt
Candidate: 3a9f1c2
Gaps: none
```

## Hill-climb run

```
Metric and direction: <metric>, <lower | higher> is better
Stop predicate: <target> and at least <N> attempts
Predicate met: <yes | no: why stopped>
Baseline -> final: <x> -> <y> <unit> (<percent delta>)
Iterations: <total> (<kept> kept, <reverted> reverted)
Accepted fixes (in landing order):
- <commit> <one line: mechanism and delta>
Frozen harness: <command>, median of <N>, prints error count and work count
Regression gate: <command> -> <green>
Decision log: <absolute path to decision.tsv>
Next idea if pushed further: <one line>
```
