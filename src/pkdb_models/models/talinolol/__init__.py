"""Talinolol: PBPK model of the beta blocker talinolol, a substrate of P-glycoprotein.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.talinolol`.
"""

from pathlib import Path

from pkpdsim.model import CheckSettings, FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.talinolol.tolerances import ABSOLUTE_TOLERANCE

TALINOLOL_PATH = Path(__file__).parent

MODEL_BASE_PATH = TALINOLOL_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "talinolol_body_flat.xml"

DATA_PATH_BASE = TALINOLOL_PATH / "data"
DATA_PATH_TALINOLOL = DATA_PATH_BASE / "talinolol"
DATA_PATHS = [DATA_PATH_TALINOLOL]

MODEL = PKPDModel(
    name="talinolol",
    package=__name__,
    title="Talinolol PBPK model",
    path=TALINOLOL_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH / "talinolol_model.omex",
    factory=".models.factory:create_talinolol_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(formats=("svg",), fig_dpi=300, legend_fontsize=10),
    fits=("PK_20261020_042735__49b48",),
    fit_identifiability=True,
    checks=CheckSettings(
        one_at_a_time=(
            "slow test peaked at 5.7 GB with sbmlsim 0.9.6 (max RSS, one at a time), "
            "little headroom on a hosted runner with 7 GB"
        ),
    ),
    release=ReleaseSettings(
        title="Physiologically based pharmacokinetic (PBPK) model of talinolol",
        repository="matthiaskoenig/talinolol-model",
        doi="10.5281/zenodo.8150138",
        authors=(
            Author(
                "Stemmer Mallol, Beatrice Amelie",
                "0000-0002-0928-3401",
                "Humboldt-Universität zu Berlin, Institute for Theoretical Biology, Berlin",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "talinolol",
            "pharmacokinetics",
            "PBPK",
            "physiologically based pharmacokinetic model",
            "P-glycoprotein",
            "SBML",
        ),
        docker_image="matthiaskoenig/talinolol",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the talinolol physiologically based "
            "pharmacokinetic (PBPK) model."
        ),
        first_year=2022,
    ),
)
"""The talinolol model: its commands, see `pkpdsim.model`."""
