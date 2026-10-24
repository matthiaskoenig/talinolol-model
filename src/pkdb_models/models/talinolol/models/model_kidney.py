"""Talinolol kidney model."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.talinolol.models import annotations, templates
from pkdb_models.models.talinolol.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""

    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


_m = Model(
    "talinolol_kidney",
    name="Model for talinolol elimination in the kidneys",
    notes="""
    # Model for talinolol elimination in the kidneys

    Model for the renal excretion of talinolol (tal)
    encoded in <a href="http://sbml.org">SBML</a> format.

    Talinolol is excreted unchanged in the urine by glomerular filtration and
    a net tubular secretion: the renal clearance (151-311 ml/min) is several
    times the filtration of the unbound talinolol. The renal excretion is the
    filtration of the unbound talinolol `GFR * fup_tal` times `TALEX_f` (1 is
    filtration alone, above 1 a net secretion), so that it follows the renal
    function as the glomerular filtration rate does.

    - On average, about 60% of talinolol and talinolol metabolites was excreted by kidney and about 40% extrarenally.
      {Trausch1995}
    - Other metabolites then talinolol are almost not detectable in urine. I.e. sum of metabolites is 0.33% of dose
      vs. talinolol 52.83 % dose {Trausch1995}
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        4,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vki",
        1.5,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = [
    Species(
        "tal_ext",
        initialConcentration=0.0,
        name="talinolol (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
        port=True,
    ),
    Species(
        "tal_urine",
        initialConcentration=0.0,
        name="talinolol (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
        port=True,
        notes="""
        Urinary species are in amounts.
        """,
    ),
]

_m.parameters = [
    Parameter(
        sid="f_renal_function",
        name="renal function",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        >1.0: increased kidney function
        1.0: normal kidney function (healthy control)
        <1.0: decreased kidney function

        Renal function relative to the healthy glomerular filtration rate
        GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
        clearance of X ml/min is the renal function X/101.
        """,
    ),
    Parameter(
        "GFR_base",
        101,
        U.ml_per_min,
        name="glomerular filtration rate (healthy)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "fup_tal",
        0.4,
        U.dimensionless,
        constant=True,
        name="fraction unbound in plasma tal",
        sboTerm=SBO.KINETIC_CONSTANT,
        port=True,
    ),
    Parameter(
        "TALEX_f",
        **FITS.parameter("KI__TALEX_f", unit=U.dimensionless),
        name="renal clearance of unbound talinolol relative to the GFR",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The renal clearance of talinolol is TALEX_f times the filtration of
        its unbound fraction, fup_tal * GFR: 1 is filtration alone, above 1 a
        net tubular secretion. A renal clearance of 151-311 ml/min
        (Westphal2000a/b, Trausch1995, Schwarz2007) is TALEX_f 3.7-7.7 at
        fup_tal 0.4 and GFR 101 ml/min.
        """,
    ),
]

_m.rules.extend(
    [
        AssignmentRule(
            "GFR",
            "f_renal_function * GFR_base",
            unit=U.ml_per_min,
            name="glomerular filtration rate",
        ),
    ]
)

_m.reactions = [
    Reaction(
        "TALEX",
        name="excretion talinolol",
        equation="tal_ext -> tal_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vki",
        # [ml/min] * [l/ml] * [-] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * fup_tal * TALEX_f * tal_ext",
            U.mmole_per_min,
        ),
        annotations=[(BQB.IS, "ncit/C75913")],  # renal clearance
    ),
]

model_kidney = _m


if __name__ == "__main__":
    from pkdb_models.models.talinolol import MODEL_BASE_PATH

    results = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
