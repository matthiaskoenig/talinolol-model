"""Talinolol liver model."""

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    RateRule,
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


_m = Model(
    "talinolol_liver",
    name="Model for talinolol elimination in the liver",
    notes="""
    # Model for talinolol elimination in the liver

    Model for the hepatic uptake and biliary excretion of talinolol in
    <a href="http://sbml.org">SBML</a>.
    Talinolol is not metabolized (the metabolites in the urine are 0.33 % of
    the dose, Trausch1995), it is taken up into the liver (OATP1B1, `TALIM`)
    and excreted unchanged into the bile (P-glycoprotein, `TALEX`). The bile
    reaches the duodenum (`TALEHC`, the enterohepatic circulation); the bile
    collected by a T-drain after a cholecystectomy is not (`f_EHC` 0).

    - enterohepatic circulation (see Terhaag1989); "The biliary clearance amounted to 43 ml/hr/kg (range: 13-212 ml/hr/kg)."
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
        "Vli",
        1.5,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["li"],
    ),
    Compartment(
        "Vbaso",
        np.nan,
        name="basolateral membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["basolateral"],
    ),
    Compartment(
        "Vapical",
        np.nan,
        name="apical membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["apical"],
    ),
    Compartment(
        "Vbi",
        1.0,
        name="bile",
        unit=U.liter,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["bi"],
        port=True,
    ),
    Compartment(
        "Vduodenum",
        0.1,
        name="intestinal lumen (duodenum)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
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
        "tal",
        initialConcentration=0.0,
        name="talinolol (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
    ),
    Species(
        "tal_bi",
        initialConcentration=0.0,
        name="talinolol (bile)",
        compartment="Vbi",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
        notes="""
        Bile talinolol in amount.
        """,
    ),
    Species(
        "tal_duodenum",
        initialConcentration=0.0,
        name="talinolol (duodenum)",
        compartment="Vduodenum",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
        port=True,
    ),
]

_m.parameters = [
    Parameter(
        "fup_tal",
        0.4,
        U.dimensionless,
        constant=True,
        name="fraction unbound in plasma tal",
        sboTerm=SBO.KINETIC_CONSTANT,
        port=True,
    ),
]

_m.reactions = [
    Reaction(
        "TALIM",
        name="talinolol import",
        equation="tal_ext <-> tal",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vbaso",
        pars=[
            Parameter(
                "TALIM_Vmax",
                # 9.3 % (3.7-24.7 %) of an IV dose in the bile of T-drain
                # patients (Terhaag1989)
                **FITS.parameter("LI__TALIM_Vmax", unit=U.mmole_per_min_l),
                name="Vmax for talinolol import",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "TALIM_Km_tal",
                0.301,
                unit=U.mM,
                name="Km for talinolol import",
                sboTerm=SBO.MICHAELIS_CONSTANT,
                notes="""
                Talinolol is as substrate for
                - OATP1B3 (Km = 153 ± 137 µmol/l; Vmax = 168 ± 30.3 µmol/mgxmin),
                - OATP1B1 (Km = 301 ± 133 µmol/l; Vmax = 1135 ± 348 µmol/mgxmin),
                - OATP2B1 (Km = 459 ± 260 µmol/l; Vmax = 4.32 ± 1.33 µmol/mgxmin),
                - OATP1A2 (Km = 477 ± 158 µmol/l; Vmax = 0.61 ± 0.1 µmol/mgxmin)
                - NTCP (Km = 2560 ± 781 µmol/l; Vmax = 15944 ± 3741 µmol/mgxmin)
                {Roustom2017}
                """,
            ),
            Parameter(
                "f_oatp1b1",
                1,
                unit=U.dimensionless,
                name="activity of OATP1B1",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            "f_oatp1b1 * TALIM_Vmax/TALIM_Km_tal * Vli * (fup_tal*tal_ext - tal)"
            "/(1 dimensionless + fup_tal*tal_ext/TALIM_Km_tal + tal/TALIM_Km_tal)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "TALEX",
        name="talinolol bile export",
        equation="tal -> tal_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        pars=[
            Parameter(
                "TALEX_k",
                0.15,  # no effect on the plasma and the bile (the uptake limits), not fitted
                unit=U.per_min,
                name="rate for talinolol export in bile",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
            Parameter(
                "f_pgp",
                1,
                unit=U.dimensionless,
                name="activity of P-glycoprotein (liver)",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            "f_pgp * TALEX_k * Vli * tal",
            U.mmole_per_min,
        ),
        notes="""
        This could be via MDR1 or MRP2.
        Using trick to track total amount of talinolol excreted in bile.
        """,
    ),
    Reaction(
        "TALEHC",
        name="talinolol enterohepatic circulation",
        equation="tal_bi -> tal_duodenum",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vduodenum",
        notes="""
        Transport of talinolol via bile to the intestinal lumen (duodenum). This is the
        enterohepatic circulation of talinolol.

        Irreversible transport of talinolol via Mass-Action-Kinetics.

        This is a dummy process which allows to simulate cholocystectomy.
        """,
        pars=[
            Parameter(
                "f_EHC",
                1,
                unit=U.dimensionless,
                name="factor for modifying EHC",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=("f_EHC * TALEX", U.mmole_per_min),
    ),
]

# Total cumulative amount bile
_m.parameters.append(
    Parameter(
        "Abile_tal",
        value=0.0,
        name="cumulative talinolol (bile)",
        unit=U.mmole,
        annotations=annotations.species["tal"],
        sboTerm=SBO.KINETIC_CONSTANT,
        constant=False,
        notes="""
        Total talinolol excreted in bile.
        """,
    ),
)

_m.rate_rules.append(
    # cumulative amount in bile
    RateRule(
        "Abile_tal",
        "TALEX",
        name="cumulative amount talinol bile",
        unit=U.mmole_per_min,
        sboTerm=SBO.RATE_LAW,
        notes="""
        Calculated via integration of the talinol bile excretion rate.
        """,
    ),
)

# Concentration bile
_m.parameters.extend(
    [
        Parameter(
            "bile_flow",
            value=46.0e-3 / 60,  # 46 [ml/hr] = 46/60 [ml/min]
            name="bile flow",
            unit=U.l_per_min,
            sboTerm=SBO.KINETIC_CONSTANT,
            annotations=[(BQB.HAS_PART, "ncit/C13192"), (BQB.HAS_PART, "ncit/C41141")],
            notes="""
        Concentration of talinolol in bile calculated via mean bile flow.
        Bile flow from Terhaag1989 as mean median bile flow: 46 [ml/hr].
        """,
        ),
        Parameter(
            "Cbile_tal",
            value=0.0,
            name="talinolol (bile)",
            unit=U.mM,
            annotations=annotations.species["tal"],
            constant=False,
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
        Concentration of talinolol in bile calculated via mean bile flow.
        """,
        ),
    ]
)

_m.rules.append(
    # bile concentration talinolol via bile flow: [(mmole/min)/(l/min)] = [mmole/l]
    AssignmentRule("Cbile_tal", "TALEX/bile_flow", U.mM),
)


model_liver = _m


if __name__ == "__main__":
    from pkdb_models.models.talinolol import MODEL_BASE_PATH

    result = create_model(
        model=model_liver,
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
