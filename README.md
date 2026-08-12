# Mutation testing

Org hub for [quality-gates](https://github.com/quality-gates) mutation tools.

Mutation testing changes production source in small ways and re-runs the suite.
If tests fail, the mutant is **killed**. If tests still pass, the mutant
**escaped**. An escape is a gap: that shape of bug would ship.

You need mutation testing to avoid **AI test slop**. Models write passing tests
that look complete under coverage and review. Mutation testing asks the harder
question: if the code were wrong, would the tests fail?

## Why you need it

You need mutation testing to avoid AI test slop. Line coverage only proves
code ran. It does not prove the assertions would catch a fault.

AI-assisted suites write passing tests that still miss faults. They often:

- assert existence instead of values
- pin happy paths and skip boundaries
- mock so heavily that production behaviour cannot fail the test
- pass on every run because they cannot fail

Mutation testing exposes those gaps with brutal efficiency. A high kill rate
is a regression guard. A pile of escapes is a map of tests that do not pull
their weight — including tests an agent just added.

Prefer **covered-MSI** (score on lines the suite actually executes) when the
tool supports it. Raw MSI drops when you add untested code; covered-MSI stays
flat until existing tests get weaker.

## Pain points it hits

| Pain | What mutation testing does |
| :--- | :--- |
| AI writes green tests that never fail | Escapes show assertions that do not constrain behaviour |
| 100% coverage, weak confidence | Coverage counts execution; mutants count detection |
| Review cannot read every test | Scores and escape diffs scale past human attention |
| CI only runs unit tests | Score floors (`--min-msi`, `--min-covered-msi`) fail the job |
| Legacy suite full of known holes | Baseline / accepted survivors: fail only on **new** escapes |
| PR noise and long runtimes | Diff-aware mutation limits work to changed lines |
| Polyglot or infra outside one language tool | Manual mutation still applies (see below) |

## Language map

Quality-gates ships language-native CLIs. Start with the row for your stack.

| Language | Tool | Role | Repo |
| :--- | :--- | :--- | :--- |
| Go | **mutago** | Full CLI: coverage-aware MSI, git-diff filter, baseline, CI loggers, Go-idiom mutators | [quality-gates/mutago](https://github.com/quality-gates/mutago) |
| Rust | **mutarust** | Cargo-native mutation runner with score gates, coverage mode, baselines, CI loggers | [quality-gates/mutarust](https://github.com/quality-gates/mutarust) |
| Haskell | **mutaskell** | GHC-parser mutator with covered-MSI, project mode, and CI setups | [quality-gates/mutaskell](https://github.com/quality-gates/mutaskell) |

Site docs where published:

- mutago — https://quality-gates.github.io/mutago/
- mutaskell — https://quality-gates.github.io/mutaskell

Other languages are not first-party here yet. Use a mature tool in that
ecosystem, or run [manual mutation](#manual-mutation) until a quality-gates
port exists.

## Start here

**Go**

```console
go install github.com/quality-gates/mutago/v2/cmd/mutago@latest
mutago --coverage --min-msi 75 --min-covered-msi 80 ./...
```

**Rust**

```console
cargo install mutarust
mutarust --coverage --min-msi 75 --min-covered-msi 80 .
```

**Haskell**

```console
cabal build --write-ghc-environment-files=always all
cabal run mutaskell -- --min-covered-msi 70 src/YourModule.hs
```

Raise floors only when the suite can hold them. On a brownfield tree, record a
baseline of current escapes first, then fail only on new ones (see each tool’s
README for `--baseline` / config equivalents).

## Manual mutation

Automation needs a parser and a fast suite. You still need the *idea* when:

- the change lives outside app source (Dockerfile, Terraform, CI YAML, SQL)
- the repo mixes languages one tool does not own
- the valuable check is an end-to-end or container smoke path

Minimum loop:

1. Name one behaviour users would notice if it broke.
2. Change one line that should break that behaviour.
3. Run the automated checks that should catch it.
4. Record kill or escape. Restore the line.
5. Keep a short, repeatable list so successive runs stay comparable.

Agents can propose mutants; humans still own the list, the oracle, and the
pass/fail record. Manual mutation does not replace a language CLI in CI. It
extends the same pressure to layers tools do not reach.

## Related quality gates

Mutation testing asks whether tests detect faults. The **mess\*** family asks
whether the source stays maintainable before faults hide in mess:

| Language | Mess detector |
| :--- | :--- |
| Python | [messpy](https://github.com/quality-gates/messpy) |
| Rust | [messrust](https://github.com/quality-gates/messrust) |
| Go | [messgo](https://github.com/quality-gates/messgo) |
| JavaScript / TypeScript | [messcript](https://github.com/quality-gates/messcript) |
| C# | [messharp](https://github.com/quality-gates/messharp) |
| F# | [messfsharp](https://github.com/quality-gates/messfsharp) |

Use both: mess detectors on every change; mutation scores on a cadence or on
touched packages when runtime allows.

## Maintainers

This repository is documentation only: the org map and pitch for mutation
testing. Product code and releases live in the language tool repos above.

Hub contract tests:

```console
python3 tests/hub_contract_test.py
```
