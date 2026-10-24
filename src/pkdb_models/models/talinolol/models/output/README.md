[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8150138.svg)](https://doi.org/10.5281/zenodo.8150138)
[![GitHub Action](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/python.yml/badge.svg)](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/python.yml)
[![GitHub Action](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/docker.yml/badge.svg)](https://github.com/matthiaskoenig/talinolol-model/actions/workflows/docker.yml)

# talinolol model
This repository provides the talinolol physiologically based pharmacokinetic (PBPK) model: the absorption of talinolol along the intestine (apical uptake by OATP2B1, efflux by P-glycoprotein with a saturable rate, passive basolateral transport, by which P-glycoprotein also secretes systemic talinolol into the lumen), the transit of the unabsorbed dose into the feces, its distribution into the tissues, its hepatic uptake by OATP1B1 and biliary excretion by P-glycoprotein with the enterohepatic circulation, and its renal excretion relative to the GFR; talinolol is not metabolized. The model describes the effects of the dose, of the ABCB1 genotype, of renal impairment and of inhibitors and inducers of the intestinal P-glycoprotein (erythromycin, St John's wort, rifampicin).

The model is distributed in [SBML](http://sbml.org) format available from [`talinolol_body_flat.xml`](./models/talinolol_body_flat.xml) with 
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftalinolol-model%2Fmain%2Fmodels%2Ftalinolol_body_flat.xml) and [model equations](./models/talinolol_body_flat.md).

The COMBINE archive is available from [`talinolol_model.omex`](./talinolol_model.omex).

### Comp submodels
* **liver** submodel [`talinolol_liver.xml`](./models/talinolol_liver.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftalinolol-model%2Fmain%2Fmodels%2Ftalinolol_liver.xml) and [equations](./models/talinolol_liver.md).
* **kidney** submodel [`talinolol_kidney.xml`](./models/talinolol_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftalinolol-model%2Fmain%2Fmodels%2Ftalinolol_kidney.xml) and [equations](./models/talinolol_kidney.md).
* **intestine** submodel [`talinolol_intestine.xml`](./models/talinolol_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftalinolol-model%2Fmain%2Fmodels%2Ftalinolol_intestine.xml) and [equations](./models/talinolol_intestine.md).
* **whole-body** submodel [`talinolol_body.xml`](./models/talinolol_body.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftalinolol-model%2Fmain%2Fmodels%2Ftalinolol_body.xml) and [equations](./models/talinolol_body.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8150138.svg)](https://doi.org/10.5281/zenodo.8150138)

> Stemmer Mallol, B. A. & König, M. (2026).
> *Physiologically based pharmacokinetic (PBPK) model of talinolol.*   
> Zenodo. [https://doi.org/10.5281/zenodo.8150138](https://doi.org/10.5281/zenodo.8150138)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

## Run simulations
### python
Clone the repository 
```bash
git clone https://github.com/matthiaskoenig/talinolol-model.git
cd talinolol-model
```

#### uv
Setup environment with uv (https://docs.astral.sh/uv/getting-started/installation/)
```bash
uv sync
```
Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.talinolol -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run_simulation pkdb_models.models.talinolol -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/talinolol:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.talinolol -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Mariia Myshkina was supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within Priority Programme SPP 2311 by grant number 465194077 (Subproject SimLivA).
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2022-2026 Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)

