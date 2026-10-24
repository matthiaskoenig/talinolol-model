"""Annotations of the talinolol models: the species and the shared compartments."""

from pkpdsim.annotations import compartments
from sbmlutils.metadata import BQB

__all__ = ["compartments", "species"]

species = {
    "tal": [
        # talinolol
        (BQB.IS, "pubchem.compound/68770"),
        (BQB.IS, "chebi/CHEBI:135533"),
    ],
    "taloh": [
        # hydroxytalinolol
    ],
}
