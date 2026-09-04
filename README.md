# Context Mechanisms in Animal Communication

Reproducible Python analyses and an identification-oriented framework for asking **where** context effects enter animal-communication systems.

The core methodological claim is simple:

> An observed behavioural context effect is not, by itself, an identified mechanism.

The repository operationalises this as:

```text
context effect -> compatible mechanism family -> discriminating intervention
```

The P/T/I/H/A labels distinguish signal production, transmission/sensory access, current-context information integration,
history-dependent receiver state, and response decision/action selection. They are an identification scaffold, not a claim of five
new biological stages.

## What is in this public release

- canonical Python analysis scripts under `analysis/`;
- maintained helper code under `src/contextmech/`;
- a public smoke/regression suite covering redistributable and synthetic components;
- the Dryad-derived titi 2013 processed extract used by the public regression target;
- data-source and redistribution notes for optional empirical analyses;
- formal notes on signal-detection observational equivalence and compatible mechanism sets.

The associated full review manuscript, journal submission files, correspondence, reviewer suggestions, private contact metadata,
and internal author-reference documents are intentionally **not** part of this public repository.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH="$PWD/src"    # Windows PowerShell: $env:PYTHONPATH="$PWD/src"
```

## Public reproducibility tests

```bash
python tests/smoke_test.py
python tests/regression_test.py
```

The first public release validates the Dryad/CC0 titi 2013 analysis and the data-independent A2 power-planning and SDT-identifiability
components. Additional scripts are provided for other public source datasets, but their processed extracts are intentionally omitted
until redistribution rights are explicit. See `data/README.md`.

## Repository provenance

The maintained scripts were consolidated from an earlier exploratory research workflow, rerun against retained data, and checked against
fixed numerical targets. They should not be represented as though every current source file existed byte-for-byte at the earliest exploratory
stage. See `PROVENANCE.md`.

## Citation

The first public reproducibility release is permanently archived on Zenodo. For exact reproducibility against `v1.0.0`, cite version DOI `10.5281/zenodo.22293278`. For the evolving software project across all releases, use concept DOI `10.5281/zenodo.22293277`. Please also cite the original datasets and associated papers for any empirical analysis reused.

## Licence

Project-authored software and documentation in this public release are MIT licensed. Third-party datasets are not relicensed by this repository;
see `THIRD_PARTY_MATERIALS.md` and `data/README.md`.
