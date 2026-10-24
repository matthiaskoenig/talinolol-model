"""Collect the data of the talinolol studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folder of the
model, see `pkpdsim.data.collect_tsv_files`.
"""

from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.talinolol import DATA_PATH_TALINOLOL

#: copies in pkdb_data which differ from a curated file only by the case of
#: their name; they are not collected, the names would collide on a file
#: system which ignores the case (macOS, Windows)
CASE_DUPLICATES = ["Bernsdorf2006/.Bernsdorf2006_Tab1A.tsv"]


def collect_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the talinolol studies into the data folder of the model.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()
    collect_tsv_files(
        source_dir=studies_dir / "talinolol",
        target_dir=DATA_PATH_TALINOLOL,
    )
    for path in CASE_DUPLICATES:
        (DATA_PATH_TALINOLOL / path).unlink(missing_ok=True)


if __name__ == "__main__":
    collect_data()
