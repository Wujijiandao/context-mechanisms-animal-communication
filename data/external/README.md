# Data availability and redistribution status

This public repository intentionally distinguishes **public accessibility** from **permission to redistribute**.
The analysis scripts are all included, but third-party empirical data are bundled only when redistribution rights
were sufficiently clear at the time of the public-release audit.

## Bundled

### Titi monkeys, 2013

- Source: Cäsar et al. Dryad dataset
- DOI: `10.5061/dryad.sd1sr`
- Bundled derived extract: `data/processed_public/titi_2013_core_trials.csv`
- Licence basis: Dryad datasets are released under CC0. Scholarly citation of the original dataset/article is still expected.

## Not bundled by default

The following analyses remain in `analysis/`, but the derived local CSV extracts are intentionally omitted from the
public repository because public availability alone was not treated as sufficient evidence of redistribution rights:

- Berthet et al. 2019 titi-monkey production/playback analysis — Figshare DOI `10.6084/m9.figshare.6007316.v5`
- Vervet context experiment 2023 — OSF `kw5qg`
- Sooty mangabey one-trial learning 2022 — OSF `t93xa`
- Vervet one-trial learning 2022 — OSF `ycnhj`; supplementary collection DOI `10.6084/m9.figshare.c.6133928`

To run these optional analyses, obtain the source material from the cited repository and provide the processed input
file at the path expected by the relevant script. The private research archive retains the exact validated extracts and
fixed numerical targets, but those third-party-derived files are not part of this first public GitHub release.

This repository does not redistribute original authors' scripts, PDFs, audio/video files, or raw archives.
