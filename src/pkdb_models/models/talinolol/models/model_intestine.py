"""Talinolol intestine model."""

from typing import TypedDict

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
    ValidationOptions,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.talinolol.models import annotations, templates
from pkdb_models.models.talinolol.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""

    kg = UnitDefinition("kg")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    per_hr = UnitDefinition("per_hr", "1/hr")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")


_m = Model(
    "talinolol_intestine",
    name="Model for talinolol absorption and secretion in the intestine",
    notes="""
    # Model for talinolol absorption and secretion in the intestine

    The intestine is a tube of six segments (duodenum, two jejunum, two ileum
    segments and the colon), each a lumen with its enterocytes. The oral dose
    dissolves into the duodenum (`dissolution_tal`), the lumen is transported
    from segment to segment (`TALFLUX_*`, a transit of about 4.7 hr through
    the small intestine and 22.5 hr through the colon) and leaves the colon
    into the feces (`TALEXC`).

    Talinolol, a hydrophilic beta blocker, is taken up into the enterocytes
    with a first order (`TALABS_*`, passive and OATP2B1) and pumped back into
    the lumen by P-glycoprotein (`TALEFL_*`), whose amount increases along the
    small intestine (`pgp_*`). The efflux saturates (`TALEFL_Km`), so that
    the bioavailability increases with the dose (the AUC per mg rises 1.8
    fold from 25 to 400 mg, DeMey1995; Wetterich1996, Siegmund2003). The
    basolateral membrane is passed in both directions (`TALEX_*`): the
    enterocytes take up talinolol from the plasma of the gut as well, and
    P-glycoprotein secretes it into the lumen against the gradient, the main
    nonrenal elimination of talinolol after an intravenous dose (Gramatte1996,
    Westphal2000a/b, Bernsdorf2006: an intestinal clearance of about 74
    ml/min), which an inducer (rifampicin) increases after an intravenous dose
    as well.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
]


class Segment(TypedDict):
    """Definition of a segment of the intestine."""

    sid: str
    name: str
    length: float  # [cm]
    diameter: float  # [cm]
    velocity: float  # [cm/min]
    pgp: float  # relative protein amount P-glycoprotein [-]
    oatp2b1: float  # relative protein amount OATP2B1 [-]


definitions: list[Segment] = [
    {
        # V = 0.322 [l], the duodenum of the body model has the same volume
        "sid": "duodenum",
        "name": "small intestine duodenum D",
        "length": 30,  # [cm]
        "diameter": 3.7,  # [cm] (4.7 - 2.7 cm),
        "velocity": 2,  # [cm/min] (1 - 4 cm/min),
        "pgp": 0.3,
        "oatp2b1": 0.45,
    },
    {  # V = 0.60 [l]
        "sid": "jejunum_1",
        "name": "small intestine jejunum J1",
        "length": 210 / 2.0,  # [cm]
        "diameter": 2.7,  # [cm],
        "velocity": 2,  # [cm/min] (1 - 4 cm/min),
        "pgp": 0.4,
        "oatp2b1": 0.5,
    },
    {
        # V = 0.60 [l]
        "sid": "jejunum_2",
        "name": "small intestine jejunum J2",
        "length": 210 / 2.0,  # [cm]
        "diameter": 2.7,  # [cm],
        "velocity": 2,  # [cm/min] (1 - 4 cm/min),
        "pgp": 0.5,
        "oatp2b1": 0.45,
    },
    {
        # V = 0.94 [l]
        "sid": "ileum_1",
        "name": "small intestine ileum I1",
        "length": 330 / 2.0,  # [cm]
        "diameter": 2.7,  # [cm],
        "velocity": 2,  # [cm/min] (1 - 4 cm/min),
        "pgp": 0.7,
        "oatp2b1": 0.45,
    },
    {
        # V = 0.94 [l]
        "sid": "ileum_2",
        "name": "small intestine ileum I2",
        "length": 330 / 2.0,  # [cm]
        "diameter": 2.7,  # [cm],
        "velocity": 2,  # [cm/min] (1 - 4 cm/min),
        "pgp": 1.1,
        "oatp2b1": 0.45,
    },
    {
        # V = 3.81 [l]
        "sid": "colon",
        "name": "large intestine colon",
        "length": 135,  # [cm]
        "diameter": 6,  # [cm],
        # [cm/min] a colonic transit of 22.5 hr (about 1 day)
        "velocity": 0.1,
        "pgp": 0.25,
        "oatp2b1": 0.5,
    },
]

#: the segment which the oral dose and the bile reach
DUODENUM = "duodenum"

for d in definitions:
    _m.compartments.extend(
        [
            Compartment(
                f"V{d['sid']}",
                1e-3
                * np.pi
                * np.power(d["diameter"] / 2.0, 2)
                * d["length"],  # [cm^3] -> [l]
                name=d["name"],
                sboTerm=SBO.PHYSICAL_COMPARTMENT,
                unit=U.liter,
                constant=False,
                annotations=annotations.compartments[d["sid"].split("_")[0]],
                port=(d["sid"] == DUODENUM),
                notes="""Modelled as a tube with area 2*pi*r^2 and volume area*length.""",
            ),
            Compartment(
                f"Ventero_{d['sid']}",
                f"0.1 dimensionless * V{d['sid']}",
                name=f"enterocytes {d['name']}",
                sboTerm=SBO.PHYSICAL_COMPARTMENT,
                unit=U.liter,
                constant=False,
                notes="""The volume of the enterocytes is assumed to be a tenth
                of the volume of the lumen.""",
            ),
        ]
    )

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
        "tal_feces",
        initialConcentration=0.0,
        name="talinolol (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tal"],
        port=True,
    ),
]

for d in definitions:
    _m.species.extend(
        [
            Species(
                f"tal_{d['sid']}",
                initialConcentration=0.0,
                name=f"talinolol ({d['name']})",
                compartment=f"V{d['sid']}",
                substanceUnit=U.mmole,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species["tal"],
                hasOnlySubstanceUnits=False,
                port=(d["sid"] == DUODENUM),
            ),
            Species(
                f"tal_entero_{d['sid']}",
                initialConcentration=0.0,
                name=f"talinolol enterocytes ({d['name']})",
                compartment=f"Ventero_{d['sid']}",
                substanceUnit=U.mmole,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species["tal"],
            ),
        ]
    )


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
    Parameter(
        "TALABS_k",
        **FITS.parameter("GU__TALABS_k", unit=U.per_min),
        name="rate of the apical uptake of talinolol",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The apical uptake of talinolol into the enterocytes is of first order,
        `oatp2b1_<segment> * TALABS_k * Vgu * [talinolol lumen]`: passive and
        by OATP2B1. Talinolol is a substrate of OATP2B1 (Km = 459 ± 260
        µmol/l, Roustom2017), but the uptake does not saturate in vivo, the
        bioavailability increases with the dose.
        """,
    ),
    Parameter(
        "TALEFL_Vmax",
        **FITS.parameter("GU__TALEFL_Vmax", unit=U.mmole_per_min_l),
        name="Vmax of the efflux of talinolol by P-glycoprotein",
        sboTerm=SBO.MAXIMAL_VELOCITY,
    ),
    Parameter(
        "TALEFL_Km",
        **FITS.parameter("GU__TALEFL_Km", unit=U.mM),
        name="Km of the efflux of talinolol by P-glycoprotein",
        sboTerm=SBO.MICHAELIS_CONSTANT,
        notes="""
        The efflux of talinolol by P-glycoprotein saturates at the
        concentrations in the enterocytes after the higher oral doses, so that
        the bioavailability increases with the dose (DeMey1995: the AUC per mg
        rises 1.8 fold from 25 to 400 mg; Siegmund2003: "first order nonionic
        diffusion diminished by ... saturated P-gp"). It is an apparent value
        of the concentration in the enterocytes of the model, whose volume is
        assumed (a tenth of the lumen).
        """,
    ),
    Parameter(
        "TALEX_k",
        0.35,
        unit=U.per_min,
        name="rate of the basolateral transport of talinolol",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The basolateral transport between the enterocytes and the plasma of the
        intestine is passive in both directions, driven by the unbound
        concentration in the plasma:
        `TALEX_k * Vgu * ([talinolol enterocytes] - fup_tal * [talinolol plasma])`.
        """,
    ),
    Parameter(
        sid="f_velocity",
        name="parameter for velocity intestinal transport",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        parameter controls velocity (1.0 reference velocity,
        < 1.0 reduced velocity, > 1.0 increased velocity)
        """,
    ),
    Parameter(
        sid="f_oatp2b1",
        name="activity of the apical uptake (OATP2B1)",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        parameter controls activity (1.0 reference activity,
        < 1.0 reduced activity, > 1.0 increased activity)
        """,
    ),
    Parameter(
        sid="f_pgp",
        name="activity of P-glycoprotein (intestine)",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        f_pgp = 1: normal activity;
        f_pgp < 1: reduced activity, inhibition of the efflux;
        f_pgp > 1: increased activity, induction of the efflux.
        The interactions and the ABCB1 genotypes set it, it is not fitted.
        """,
    ),
]

_m.reactions = []
for d in definitions:
    sid = d["sid"]
    _m.parameters.extend(
        [
            Parameter(
                f"pgp_{sid}",
                d["pgp"],
                unit=U.dimensionless,
                name="protein amount P-gp",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
            Parameter(
                f"oatp2b1_{sid}",
                d["oatp2b1"],
                unit=U.dimensionless,
                name="protein amount OATP2B1",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ]
    )

    _m.rules.extend(
        [
            AssignmentRule(
                f"TALUPTAKE_{sid}",
                value=f"TALABS_{sid.upper()} - TALEFL_{sid.upper()}",
                unit=U.mmole_per_min,
                name=f"net uptake talinolol {sid}",
            ),
        ]
    )

    _m.reactions.extend(
        [
            Reaction(
                f"TALABS_{sid.upper()}",
                name=f"apical uptake talinolol {sid}",
                equation=f"tal_{sid} -> tal_entero_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
                compartment=f"Ventero_{sid}",
                formula=(
                    f"f_oatp2b1 * oatp2b1_{sid} * TALABS_k * Vgu * tal_{sid}",
                    U.mmole_per_min,
                ),
            ),
            Reaction(
                sid=f"TALEFL_{sid.upper()}",
                name=f"efflux talinolol P-glycoprotein {sid}",
                compartment=f"Ventero_{sid}",
                equation=f"tal_entero_{sid} -> tal_{sid}",
                sboTerm=SBO.TRANSPORT_REACTION,
                formula=(
                    f"f_pgp * pgp_{sid} * TALEFL_Vmax * Vgu * "
                    f"tal_entero_{sid}/(tal_entero_{sid} + TALEFL_Km)",
                    U.mmole_per_min,
                ),
                notes="""
            Efflux is catalyzed by P-glycoprotein.
            """,
            ),
            Reaction(
                f"TALEX_{sid.upper()}",
                name=f"talinolol basolateral transport {sid}",
                equation=f"tal_entero_{sid} <-> tal_ext",
                sboTerm=SBO.TRANSPORT_REACTION,
                compartment=f"Ventero_{sid}",
                formula=(
                    f"TALEX_k * Vgu * (tal_entero_{sid} - fup_tal * tal_ext)",
                    U.mmole_per_min,
                ),
            ),
        ]
    )

# Transport reactions
for k, d in enumerate(definitions):
    sid = d["sid"]
    rate = Parameter(
        sid=f"TALFLUX_{sid.upper()}_k",
        name=f"Transport rate {sid}",
        value=d["velocity"] / d["length"],  # [cm/min]/[cm]
        unit=U.per_min,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    )
    formula = (
        f"f_velocity * TALFLUX_{sid.upper()}_k * V{sid} * tal_{sid}",
        U.mmole_per_min,
    )
    if sid == "colon":
        # the colon is emptied into the feces
        _m.reactions.append(
            Reaction(
                sid="TALEXC",
                name="excretion talinolol (feces)",
                compartment="Vcolon",
                equation="tal_colon -> tal_feces",
                sboTerm=SBO.TRANSPORT_REACTION,
                pars=[rate],
                formula=formula,
            ),
        )
        continue

    sid_next = definitions[k + 1]["sid"]
    _m.reactions.append(
        Reaction(
            f"TALFLUX_{sid.upper()}_{sid_next.upper()}",
            name=f"talinolol transport {sid} to {sid_next}",
            equation=f"tal_{sid} -> tal_{sid_next}",
            sboTerm=SBO.TRANSPORT_REACTION,
            compartment=f"V{sid}",
            pars=[rate],
            formula=formula,
        )
    )


for d in definitions:
    _m.parameters.extend(
        [
            Parameter(
                f"Ri_tal_{d['sid']}",
                0,
                U.mg_per_min,
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name="Ri [mg/min] rate of infusion intestine talinolol",
            ),
        ]
    )
    _m.reactions.append(
        Reaction(
            sid=f"TALINF_{d['sid']}",
            name=f"infusion talinolol ({d['sid']})",
            compartment=f"V{d['sid']}",
            equation=f"-> tal_{d['sid']}",
            sboTerm=SBO.TRANSPORT_REACTION,
            formula=(
                f"Ri_tal_{d['sid']}/Mr_tal",
                U.mmole_per_min,
            ),
        ),
    )


_m.parameters.extend(
    [
        Parameter(
            "PODOSE_tal",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose tal [mg]",
            port=True,
        ),
        Parameter(
            "Ka_dis_tal",
            **FITS.parameter("Ka_dis_tal", unit=U.per_hr),
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="Ka_dis [1/hr] dissolution tal",
            port=True,
        ),
        Parameter(
            "Mr_tal",
            363.495,
            U.g_per_mole,
            constant=True,
            name="Molecular weight talinolol [g/mole]",
            sboTerm=SBO.MOLECULAR_MASS,
            port=True,
        ),
    ]
)

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
_m.reactions.append(
    Reaction(
        sid="dissolution_tal",
        name="dissolution talinolol",
        formula=(
            "Ka_dis_tal/60 min_per_hr * PODOSE_tal/Mr_tal",
            U.mmole_per_min,
        ),
        equation=f"-> tal_{DUODENUM}",
        compartment="Vgu",
        notes="""Swallowing, dissolution of the tablet and gastric emptying
        into the duodenum.""",
    ),
)
_m.rate_rules.append(
    RateRule("PODOSE_tal", "-dissolution_tal * Mr_tal", U.mg_per_min),
)

model_intestine = _m


if __name__ == "__main__":
    from pkdb_models.models.talinolol import MODEL_BASE_PATH

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
        sbml_level=3,
        sbml_version=2,
        validation_options=ValidationOptions(units_consistency=True),
    )
