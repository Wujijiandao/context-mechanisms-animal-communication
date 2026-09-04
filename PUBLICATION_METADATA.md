# GitHub + Zenodo publication metadata — public release v1.0.0

## Repository

**Owner:** `Wujijiandao`  
**Repository name:** `context-mechanisms-animal-communication`  
**Visibility:** Public  
**Default branch:** `main`

### GitHub Description

> Reproducible Python analyses and an identification framework for distinguishing where context effects enter animal-communication systems.

### GitHub Topics

`animal-communication`, `animal-behavior`, `behavioural-ecology`, `bioacoustics`, `causal-inference`, `partial-identification`, `signal-detection-theory`, `information-theory`, `receiver-psychology`, `reproducible-research`, `open-science`, `python`

## First release

**Tag:** `v1.0.0`  
**Target:** `main`  
**Release title:** `v1.0.0 — First Public Reproducibility Release`

### GitHub Release Notes

This is the first public reproducibility release of the Context Mechanisms in Animal Communication research codebase.

The release publishes the maintained Python analysis and helper-code tree together with a public smoke/regression suite and formal notes on mechanistic underidentification. The central identification logic is:

`context effect -> compatible mechanism family -> discriminating intervention`

The P/T/I/H/A labels are used as a compact bookkeeping scaffold for context effects on signal production, signal transmission/sensory access, current-context information integration, history-dependent receiver state, and response decision/action selection. They are not presented as five newly discovered biological stages.

### Included in v1.0.0

- canonical analysis scripts and `src/contextmech` helpers;
- public smoke and fixed numerical regression tests;
- the CC0/Dryad-derived titi 2013 processed extract used by the public regression target;
- data-source and redistribution notes for optional empirical analyses;
- SDT observational-equivalence and compatible-mechanism-set theory notes;
- `CITATION.cff`, `.zenodo.json`, MIT licence and provenance documentation.

### Deliberately not included

The public release does not contain the full review manuscript, journal submission package, editor correspondence, suggested reviewers, private contact metadata, internal Chinese author-reference material, original third-party scripts, PDFs, videos, or raw data archives. Processed extracts from third-party repositories are also omitted where explicit redistribution rights were not verified during the release audit.

### Validation

The public test suite reproduces the retained titi 2013 numerical target and the data-independent A2 power-planning and SDT-identifiability checks. The broader private research archive retains the full empirical regression suite.

## Zenodo

**Resource type:** Software  
**Title:** `Context Mechanisms in Animal Communication: Reproducible Analysis Code`  
**Version:** `1.0.0`  
**License:** `MIT`  
**Creator:** `Yuzhan Zhang`  
**ORCID:** `0009-0000-3121-7972`

### Zenodo Description

This software release provides reproducible Python analyses and an identification-oriented framework for studying context effects in animal communication. The central methodological problem is that a context-sensitive behavioural response does not uniquely identify the causal location at which context entered the communication system. The repository organises candidate explanations around signal production, transmission and sensory access, current-context information integration, history-dependent receiver state, and response decision/action selection, and treats partially identified compatible mechanism sets as legitimate outcomes.

Version 1.0.0 is the first public reproducibility release. It contains the maintained analysis code, helper modules, public smoke and numerical regression tests, formal notes on signal-detection observational equivalence and compatible mechanism sets, and a CC0/Dryad-derived processed extract for the titi-monkey 2013 analysis. Analysis scripts for additional empirical datasets are included, but processed extracts derived from third-party repositories are intentionally omitted where redistribution rights were not explicitly verified during the release audit. Retrieval identifiers are documented in the repository.

The associated full review manuscript, journal submission files, correspondence, reviewer suggestions and private author metadata are not included in this public software archive. Users should cite both this software release and the original datasets/papers relevant to any reused empirical analysis.

### Zenodo Keywords

- animal communication
- behavioural ecology
- mechanistic inference
- causal inference
- partial identification
- signal detection theory
- information theory
- receiver psychology
- reproducible research
- open science
- Python

### Recommended Zenodo/GitHub workflow

1. Create the public GitHub repository and push the contents of this public-repo package to `main`.
2. Connect the GitHub account to Zenodo and enable this repository **before** creating the first GitHub release.
3. Confirm that `.zenodo.json` and `CITATION.cff` are present on `main`. Because `.zenodo.json` is present, Zenodo will use it in preference to `CITATION.cff` for GitHub-release archiving.
4. Create the GitHub release from tag `v1.0.0` using the release title and notes above.
5. Zenodo should archive the release and assign the version DOI; record both the version DOI and the concept DOI back in the GitHub README after archiving.
6. When the associated paper receives a DOI, add it as a related identifier in `.zenodo.json` and update the README/citation guidance in the next software release.

**Important:** GitHub-integration DOIs cannot be pre-reserved. If a DOI must be known before the GitHub release, use a manual Zenodo deposit instead.
