"""The tolerances of the integrator for the talinolol model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, species: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the talinolol model.

    The species of talinolol are small: the plasma concentrations are about
    1e-5 to 1e-3 mM, the amounts about 1e-6 to 1e-1 mmole. The amount of
    talinolol in the bile `LI__Abile_tal` [mmole] is the target of a rate rule
    and has the tolerance of the species; the other targets of rate rules are
    the doses in mg.

    Args:
        value: tolerance of the doses [mg].
        species: tolerance of the species, of their concentrations [mM] and
            amounts [mmole].

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(
        amount=species,
        concentration=species,
        other=value,
        ids={"LI__Abile_tal": species},
    )


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, species=1e-14)
