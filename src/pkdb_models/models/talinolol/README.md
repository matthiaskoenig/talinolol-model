# Talinolol

Physiologically based pharmacokinetic (PBPK) model of the beta blocker talinolol, a substrate of the intestinal P-glycoprotein (P-gp) which is not metabolized: its oral absorption along the six segments of the intestine (dissolution in the duodenum, apical uptake by OATP2B1, efflux by P-gp with a saturable rate, so that the bioavailability rises with the dose, and the passive basolateral transport, by which P-gp also secretes systemic talinolol into the lumen), the transit of the unabsorbed dose through the colon into the feces, its distribution into the tissues, its hepatic uptake (OATP1B1) and biliary excretion (P-gp) with the enterohepatic circulation, and its renal excretion relative to the glomerular filtration rate. The model describes the effects of the ABCB1 genotype, of renal impairment and of coadministered inhibitors and inducers of the intestinal P-gp such as erythromycin, St John's wort and rifampicin; the plasma and serum data are the venous plasma.

The published version of the model is [talinolol-model](https://github.com/matthiaskoenig/talinolol-model) ([doi:10.5281/zenodo.8150138](https://doi.org/10.5281/zenodo.8150138)).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fit, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_liver.py`, `model_kidney.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/models/`; the fitted values come from the adopted fit (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the 34 clinical studies (`studies/`), the oral, intravenous and intestinal application (`misc/`) and the scans (`scan/`): the activity of P-gp, OATP1B1 and OATP2B1 and the renal function in liver cirrhosis, the renal clearance against Krueger2001, the intestinal perfusion of Gramatte1996 and the site of an intestinal infusion. The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problem of the pharmacokinetics (`PK`), its parameters and the selection of the training, validation and outlier data (`mapping_collections.py`).
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics.
- `talinolol_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils`.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.talinolol --action factory
run_simulation pkdb_models.models.talinolol --action list_experiments
run_simulation pkdb_models.models.talinolol --action simulate --experiments all
run_simulation pkdb_models.models.talinolol --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.talinolol --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.talinolol --adopt PK_<fit id>
run_report pkdb_models.models.talinolol --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.talinolol --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.talinolol.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fit of the model
(`PK_20261020_042735__49b48`), not from numbers in the code.
`run_fit pkdb_models.models.talinolol --adopt <fit id>` copies the record of a
finished fit (its parameters, problem, profile likelihood and Fisher
information) into `models/output/fits/<fit id>/`, which is tracked; the ids of
the adopted fits are listed in `fits` of the model object (`__init__.py`). The
factory takes the fitted values and their uncertainty from the records
(`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`. A refit
is: fit, adopt, replace the id in `fits`, rebuild the model. See the
documentation of the repository on fitting (`docs/fitting.md`).
