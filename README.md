[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8150138.svg)](https://doi.org/10.5281/zenodo.8150138)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/talinolol-model)](https://github.com/matthiaskoenig/talinolol-model/releases)
[![Documentation](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/talinolol-model/)
[![CI](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/talinolol?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/talinolol)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic (PBPK) model of talinolol

This repository provides the talinolol physiologically based pharmacokinetic (PBPK) model.

Documentation: <https://matthiaskoenig.github.io/talinolol-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/talinolol-model.git && cd talinolol-model
uv sync
uv run run_simulation pkdb_models.models.talinolol --action all -r results
```

## How to cite

> Stemmer Mallol, B. & König, M. (2026). *Physiologically based pharmacokinetic (PBPK) model of talinolol*. Zenodo. https://doi.org/10.5281/zenodo.8150138

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2022-2026 Beatrice Amelie Stemmer Mallol and Matthias König
