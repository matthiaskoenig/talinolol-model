"""Parameter fit problems for talinolol.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The training data are the single doses of talinolol alone, oral and
intravenous, in healthy subjects of the wildtype or a not reported ABCB1
genotype and in patients with a T-drain after a cholecystectomy (the only
measurements of the biliary excretion). The validation data has four parts,
each a different question: the interactions (`INTERACTION_VALIDATION`, the arms
with a coadministered drug or excipient, simulated with documented factors of
the intestinal P-glycoprotein which are not fitted), the doses
(`DOSE_VALIDATION`, the repeated doses of the studies of a steady state, which
the single doses of the training predict), the populations
(`POPULATION_VALIDATION`, the ABCB1 genotypes, renal impairment and the
patients after a cholecystectomy) and the limitations
(`LIMITATION_VALIDATION`, the application into the intestine, the controlled
release tablets and the radioactivity of patients, which the model does not
describe). The summaries of data which is fitted one by one and the data of a
study published twice are excluded (`AGGREGATE_MAPPINGS`).
"""

from pkpdsim.fit import mapping_metadata
from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    Dosing,
    Genotype,
    Health,
    Route,
)
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.talinolol import DATA_PATHS, TALINOLOL_PATH
from pkdb_models.models.talinolol.experiments.studies import (
    Bernsdorf2006,
    Bogman2005,
    DeMey1995,
    Fan2009a,
    Fan2009b,
    Giessmann2004,
    Gramatte1996,
    Han2009,
    Haustein1981,
    He2007,
    He2012,
    Juan2007,
    Krueger2001,
    Nguyen2014,
    Nguyen2015,
    Ruike2010,
    Schwarz1999,
    Schwarz2000,
    Schwarz2005,
    Schwarz2007,
    Siegmund2003,
    Terhaag1983,
    Terhaag1989,
    Trausch1995,
    Tubic2006a,
    Wang2013,
    Westphal2000a,
    Westphal2000b,
    Wetterich1996,
    Xiao2012,
    Yan2013,
    Zeng2009,
    Zhang2005,
    Zschiesche2002,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    Bernsdorf2006,
    Bogman2005,
    DeMey1995,
    Fan2009a,
    Fan2009b,
    Giessmann2004,
    Gramatte1996,
    Han2009,
    Haustein1981,
    He2007,
    He2012,
    Juan2007,
    Krueger2001,
    Nguyen2014,
    Nguyen2015,
    Ruike2010,
    Schwarz1999,
    Schwarz2000,
    Schwarz2005,
    Schwarz2007,
    Siegmund2003,
    Terhaag1983,
    Terhaag1989,
    Trausch1995,
    Tubic2006a,
    Wang2013,
    Westphal2000a,
    Westphal2000b,
    Wetterich1996,
    Xiao2012,
    Yan2013,
    Zeng2009,
    Zhang2005,
    Zschiesche2002,
]

#: genotypes of the training data, the wildtype or not reported
CONTROL_GENOTYPES: frozenset[Genotype] = frozenset(
    {Genotype.NR, Genotype.ABCB1_3435CC, Genotype.ABCB1_2677GG_3435CC}
)

#: populations of the training data: the healthy subjects and the patients with
#: a T-drain after a cholecystectomy, whose bile is the only measurement of the
#: biliary excretion of talinolol
TRAINING_HEALTH: frozenset[Health] = frozenset({Health.HEALTHY, Health.CHOLECYSTECTOMY})

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {
    # the total radioactivity (talinolol and metabolites) of patients at a
    # steady state of 150-300 mg/day, 4 times the simulation; the plasma and
    # bile of a postoperative patient with a partial drainage; the urine of the
    # volunteers by thin layer chromatography with a recovery of 78 %, half of
    # the urine of every other study
    "Haustein1981": {
        "fm_tal_po_100_plasma_mean",
        "fm_tal_iv_10_plasma_S6",
        "fm_tal_iv_10_bile_S6",
        "fm_tal_po_100_urine_A",
        "fm_tal_po_100_urine_B",
        "fm_tal_po_100_urine_C",
    },
    # the control arm of the grapefruit juice study: the exposure is far below
    # the one of the same group's other studies of 50 mg
    "Schwarz2005": {
        "fm_schwarz2005_tal_po_50_serum",
        "fm_schwarz2005_tal_po_50_urine",
    },
    # the patient GL: a flat serum curve without a decline
    "Terhaag1989": {
        "fm_tal_iv_30_serum_S1",
        "fm_tal_iv_30_bilerate_S1",
        "fm_tal_iv_30_bile_amount_S1",
    },
    # the concentrations are several times those of every other 100 mg study
    "Wang2013": {"fm_wang2013_tal_po_100"},
}

#: the validation of the interactions: the arms with a coadministered drug or
#: excipient, simulated with documented factors of the intestinal
#: P-glycoprotein (`pgp_interaction` of the base experiment and the factors of
#: the studies) which are not fitted, or without an effect
INTERACTION_VALIDATION: NamedMappings = {
    # simvastatin, no interaction (factor 1.0)
    "Bernsdorf2006": {
        "fm_tal_iv_30_sim_serum",
        "fm_tal_iv_30_sim_urine",
        "fm_tal_iv_30_sim_feces",
    },
    # the excipients TPGS (P-gp inhibition) and Poloxamer 188 (no effect)
    "Bogman2005": {"fm_tal_ivduo_50_tpgs", "fm_tal_ivduo_50_pol"},
    # Schisandra (P-gp inhibition) and Ginkgo (chronic, P-gp inhibition)
    "Fan2009a": {"fm_tal_po_100_sche", "fm_tal_po_100_gbe"},
    # Ginkgo acute (no effect) and chronic (P-gp inhibition)
    "Fan2009b": {"fm_tal_po_100_gbe_acute", "fm_tal_po_100_gbe_chronic"},
    # erythromycin, P-gp inhibition
    "Schwarz2000": {"fm_tal_po_50_inhibition", "fm_tal_po_50_inhibition_urine"},
    # St John's wort, induction of the duodenal P-gp
    "Schwarz2007": {
        "fm_tal_po_50_sjw_serum",
        "fm_tal_po_50_sjw_urine",
        "fm_tal_iv_30_sjw_serum",
        "fm_tal_iv_30_sjw_urine",
    },
    # digoxin, no interaction
    "Westphal2000a": {
        "fm_tal_po_100_dgx_serum",
        "fm_tal_iv_30_dgx_serum",
        "fm_tal_po_100_dgx_urine",
        "fm_tal_iv_30_dgx_urine",
    },
    # rifampicin, induction of the intestinal P-gp
    "Westphal2000b": {
        "fm_tal_po_100_multi_rif_serum",
        "fm_tal_po_100_multi_rif_urine",
        "fm_tal_iv_30_rif_serum",
        "fm_tal_iv_30_rif_urine",
    },
}

#: the validation of the doses: the repeated doses of the studies of a steady
#: state, which the single doses of the training predict
DOSE_VALIDATION: NamedMappings = {
    # 9 daily doses with simvastatin (no interaction), the profile of the last
    "Bernsdorf2006": {"fm_tal_po_100_multi_sim_serum"},
    "Giessmann2004": {"fm_tal_po_100_multi_serum", "fm_tal_po_100_multi_urine"},
    "Krueger2001": {
        "fm_tal_po_100_multi_plasma_control",
        "fm_tal_po_100_multi_urine_control",
    },
    "Westphal2000b": {"fm_tal_po_100_multi_serum", "fm_tal_po_100_multi_urine"},
}

#: the validation of the populations: the ABCB1 genotypes, renal impairment
#: and the patients after a cholecystectomy
POPULATION_VALIDATION: NamedMappings = {
    # ABCB1 C3435T: the factor of TT is derived from this study
    "He2012": {
        "fm_tal_po_100_Fig1_TAL_ABCB1_CT",
        "fm_tal_po_100_Fig1_TAL_ABCB1_TT",
    },
    # renal impairment (creatinine clearance 27 ml/min) and end stage renal
    # disease on dialysis
    "Krueger2001": {
        "fm_tal_po_100_plasma_increased_renal_impairment_day1",
        "fm_tal_po_100_urine_increased_renal_impairment_day1",
        "fm_tal_po_100_multi_plasma_increased_renal_impairment",
        "fm_tal_po_100_multi_urine_increased_renal_impairment",
        "fm_tal_po_100_plasma_severe_renal_impairment",
    },
    # the serum of the T-drain patients, a half-life of 4.4 hr; their bile is
    # training data
    "Terhaag1989": {
        "fm_tal_iv_20_serum_S2",
        *(f"fm_tal_iv_30_serum_S{k}" for k in range(3, 7)),
    },
    # Chinese volunteers with the midazolam of a cocktail
    "Xiao2012": {"fm_xiao2012_tal_po_100"},
    # ABCB1 haplotypes without an effect in the data, simulated as the wildtype
    "Zhang2005": {
        "fm_zhang2005_tal_po_100_TT_TT",
        "fm_zhang2005_tal_po_100_GT_CT",
        "fm_zhang2005_tal_po_100_AT_CT",
    },
}

#: the validation of the limitations of the model: valid data of an
#: application, a formulation or a population the model does not describe,
#: which would distort the fitted parameters of the processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # the duodenal solution, absorbed too fast and too much by the model
    "Bogman2005": {"fm_tal_ivduo_50"},
    # the perfusion of the jejunum, 3-10 times too high and nearly independent
    # of the site in the model
    "Gramatte1996": {
        f"fm_tal_{location}_TAL_S{k}"
        for location in ["proximal", "distal"]
        for k in [1, 4, 5, 6]
    },
    # the radioactivity in the urine of patients with heart disease and in the
    # urine and bile of a patient with a partial bile drainage
    "Haustein1981": {
        "fm_tal_po_100_urine_mean",
        "fm_tal_iv_10_urine_amount_S6",
        "fm_tal_iv_10_bile_amount_S6",
    },
    # controlled release tablets, the model has no release along the intestine
    "Tubic2006a": {
        f"fm_tal_po_TAL_CR_{dose}_{tissue}"
        for dose in [100, 200]
        for tissue in ["plasma", "urine", "urine_mean"]
    },
}

#: the summaries of data which the fits use one by one, and the data of a
#: study published twice, excluded from every fit: they would count the
#: subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the individual urine of the patients, their mean is validated
    "Haustein1981": {f"fm_tal_po_100_urine_S{k}" for k in range(1, 6)},
    # the mean of the three genotype curves
    "He2012": {"fm_tal_po_100_Fig2_TAL"},
    # the data of He2007
    "Juan2007": {"fm_tal_po_50"},
    # the control of Nguyen2015
    "Nguyen2014": {
        "fm_nguyen2014_tal_po_100_plasma",
        "fm_nguyen2014_tal_po_100_urine",
    },
    # the urine of Table 1 and of the subjects, the mean of Fig 2 is fitted
    "Nguyen2015": {
        "fm_tal_po_100_Tab1a_urine",
        *(f"fm_tal_po_100_S{k}_urine" for k in range(1, 11)),
    },
    # the urine of the subjects, the mean is fitted
    "Schwarz1999": {f"fm_tal_po_50_urine_S{k}" for k in range(1, 10)},
    # the placebo phase of Schwarz1999 again
    "Schwarz2000": {
        "fm_tal_po_50_serum",
        "fm_tal_po_50_urine",
        *(f"fm_tal_po_50_urine_S{k}" for k in [1, 2, 3, 5, 6, 7, 8, 9]),
    },
    # the genotype groups of the subjects of the 100 mg arm
    "Siegmund2003": {"fm_tal_po_TAL_SUG1_100", "fm_tal_po_TAL_SUG2_100"},
    # the bile amounts, the extrapolated integral of the bile rates
    "Terhaag1989": {
        "fm_tal_iv_20_bile_amount_S2",
        *(f"fm_tal_iv_30_bile_amount_S{k}" for k in range(3, 7)),
        "fm_tal_iv_30_bile_amount_mean",
    },
    # the urine of the subjects, the means are fitted
    "Trausch1995": {
        *(f"fm_tal_iv_30_tal_S{k}d" for k in range(1, 12)),
        *(f"fm_tal_po_50_tal_S{k}e" for k in range(1, 12)),
    },
    # one volunteer of the subjects of Table 1
    "Tubic2006a": {"fm_tal_po_TAL_IR_100_urine"},
    # the serum samples of Westphal2000b assayed again
    "Zschiesche2002": {
        "fm_zschiesche2002_tal_iv_30",
        "fm_zschiesche2002_tal_po_100_multi",
    },
}

#: the validation data
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for mappings in VALIDATION_QUESTIONS.values()
    for study in mappings
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_training(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Single oral and intravenous doses of talinolol alone, besides the named data.

    The training data are the single doses without a coadministered drug of the
    control genotypes (`CONTROL_GENOTYPES`) and populations (`TRAINING_HEALTH`),
    without the controlled release tablets. The validation data and the outliers
    are named and pass, every other mapping is excluded.
    """
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping) or named(
        OUTLIER_MAPPINGS, fit_mapping_key, fit_mapping
    ):
        return True
    metadata = mapping_metadata(fit_mapping)
    return (
        metadata.route in {Route.PO, Route.IV}
        and metadata.dosing == Dosing.SINGLE
        and metadata.coadministration == Coadministration.NONE
        and metadata.genotype in CONTROL_GENOTYPES
        and metadata.health in TRAINING_HEALTH
        and metadata.application_form != ApplicationForm.CONTROLLED_RELEASE
    )


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`) and every mapping which is neither training data
    nor named (`filter_training`). The outliers are `OUTLIER_MAPPINGS`, the
    validation data is `VALIDATION_MAPPINGS`. Neither kind enters the cost;
    both are simulated and evaluated with the training data, so a report says
    how the fitted parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=TALINOLOL_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
            filter_training,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data of talinolol."""
    return mapping_collections([])


if __name__ == "__main__":
    console.rule(title=f_collections_pk.__name__, align="left", style="white")
    f_collections_pk()
