"""Sensitivity analysis of the talinolol model.

The outputs are the pharmacokinetic parameters of talinolol in plasma after a
single oral dose (the non-compartmental analysis of `pkpdutils`) and the
fractions of the dose excreted in the urine and the feces. The parameters are
the parameters of the model with bounds of +-15 % around their value. The
analyses are run as a script, the local analysis by default:

    python -m pkdb_models.models.talinolol.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.talinolol.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the groups of renal
impairment, leaves out `KI__f_renal_function`. The environment variable
`PKPDSIM_SENSITIVITY_N` replaces the numbers of samples of the global analyses
for a quick run, see `pkpdsim.sensitivity.sample_size`.

The model without talinolol is stationary, so the simulation of a group starts
with the dose. The dose is followed for `END_HR` hours, long enough for the
terminal phase of talinolol (a half-life of about 14 hr) and for the transit
of the unabsorbed dose through the colon into the feces.
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Custom, Formula, Simulation

from pkdb_models.models.talinolol import MODEL, MODEL_PATH
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)
from pkdb_models.models.talinolol.fitting.parameters import (
    parameters_pk as fit_parameters,
)

#: oral dose of talinolol of the analysis [mg], the dose of most studies
DOSE_TAL = 100
#: the dose [mmole]
DOSE_TAL_MMOLE = float(
    (Q(DOSE_TAL, "mg") / TalinololSimulationExperiment.Mr.tal).to("mmole").magnitude
)
#: the hours after the dose
END_HR = 120
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal concentration after 100 mg (5e-4 mM), so that the noise
#: of the integrator is not the terminal phase
LLOQ = 5e-8
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of talinolol -> unit of the output
PK_OUTPUTS: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_tal` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})


def fraction_of_dose(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the amount at the end of a timecourse [mmole] as a fraction of the dose."""
    del time
    (x,) = values.values()
    return float(x[-1]) / DOSE_TAL_MMOLE


#: the excreted fractions of the dose: id -> selection
EXCRETIONS: dict[str, str] = {
    "fe_urine": "Aurine_tal",
    "fe_feces": "Afeces_tal",
}

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("tal_auc_inf_obs", "talinolol AUC∞"),
    SensitivityOutput("tal_cmax", "talinolol Cmax"),
    SensitivityOutput("tal_tmax", "talinolol tmax"),
    SensitivityOutput("tal_thalf", "talinolol Half-life"),
    SensitivityOutput("tal_vz_f", "talinolol Vz/F"),
    SensitivityOutput("tal_cl_f", "talinolol CL/F"),
    SensitivityOutput("fe_urine", "talinolol fraction urine"),
    SensitivityOutput("fe_feces", "talinolol fraction feces"),
]

#: the observables of a simulation, the outputs with their units; the id of
#: the analysis (`pk_tal`) is no species of the model
OBSERVABLES = [
    PK(
        "pk_tal",
        "[Cve_tal]",
        dose="PODOSE_tal",
        route="oral",
        options=NCAOptions(lloq=LLOQ),
        parameters=list(PK_OUTPUTS),
    ),
    *(
        Formula(
            f"tal_{key}",
            f"pk_tal.{key} / at(Mr_tal, 0)"
            if key in PK_PER_DOSE_MASS
            else f"pk_tal.{key}",
            unit=unit,
        )
        for key, unit in PK_OUTPUTS.items()
    ),
    *(
        Custom(key, fraction_of_dose, "dimensionless", symbols=[selection])
        for key, selection in EXCRETIONS.items()
    ),
]

#: the output times [hr]: every 0.02 hr in the first day after the dose
#: (absorption and maximum), every 0.5 hr after it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 24, 1201),
                np.linspace(24, END_HR, 2 * (END_HR - 24) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of talinolol at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes, "PODOSE_tal": Q(DOSE_TAL, "mg")},
    )


#: the groups the analyses are run for: the control and the classes of renal
#: impairment of the simulation experiments (the kidneys excrete about 60 % of
#: an intravenous dose)
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"KI__f_renal_function": TalinololSimulationExperiment.renal_map[name]}
            ),
            TalinololSimulationExperiment.renal_colors[name],
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("modRI", "Moderate renal impairment"),
            ("sevRI", "Severe renal impairment"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # molecular weight
            "Mr_tal",
            # reference values
            "BW_ref",
            "KI__GFR_base",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters
            "PODOSE_tal",
            "IVDOSE_tal",
            "ti_tal",
            # unused volumes
            "Vurine",
            "Vfeces",
            # the switch of the enterohepatic circulation (0 with a T-drain)
            "LI__f_EHC",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions and of the transporters
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in [
                "KI__f_renal_function",
                "GU__f_pgp",
                "LI__f_pgp",
                "GU__f_oatp2b1",
                "LI__f_oatp1b1",
            ]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
        "KI__f_renal_function": r"\cite{Stevens2024}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
