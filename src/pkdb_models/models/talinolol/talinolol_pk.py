"""Pharmacokinetic parameters of the talinolol simulations and scans.

The pharmacokinetic parameters are the non-compartmental analysis of
`pkpdutils`, named like the variables of its `NCAResult` (e.g. `auc_last`,
`auc_inf_obs`, `cmax`, `thalf`, `lambda_z`, and `cl`, `vz` after an
intravenous or `cl_f`, `vz_f` after an oral dose), with the unit of every
parameter in `<name>_unit`, for talinolol in the venous plasma. The dose is the
oral dose `PODOSE_tal`, the intravenous bolus `IVDOSE_tal` or the intravenous
infusion `cum_dose_tal` (its duration is the time until the whole dose is
infused); a simulation without one of them (the infusions into the intestine)
has the parameters which need no dose. The concentrations below
`LLOQ_FRACTION` of the maximum are below the limit of quantification, so that
the noise of the integrator is not the terminal phase. The renal and fecal
clearances are the amounts excreted until the end of the simulation over
`auc_last`.

A single simulation has no dimension, a scan one, the scanned parameter; a run
over the draws of the fitted parameters (`run_simulation
pkdb_models.models.talinolol --uncertainty`) adds the dimension of the draws.
The parameters are calculated for every point, a row per point with its
position along the scan and the draws (the columns `point` and, with draws,
`draw`), see `summarize`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame
from pkpdsim.scan import end_values, scan_dimensions, start_values
from pkpdutils import Route, Timecourses, nca, ureg
from sbmlsim import Q
from sbmlsim.result import ScanResult

if TYPE_CHECKING:
    from pkdb_models.models.talinolol.experiments.base_experiment import (
        TalinololSimulationExperiment,
    )

#: concentration of talinolol in the venous plasma
CONCENTRATION = "[Cve_tal]"
#: the doses at the start of a simulation by route
DOSES: dict[Route, str] = {
    Route.ORAL: "PODOSE_tal",
    Route.IV_BOLUS: "IVDOSE_tal",
}
#: the cumulative dose of an intravenous infusion
INFUSION = "cum_dose_tal"
#: the clearances by route of excretion -> the cumulative amount excreted
EXCRETIONS: dict[str, str] = {
    "cl_renal": "Aurine_tal",
    "cl_fecal": "Afeces_tal",
}
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def _rows(df: pd.DataFrame, res: ScanResult, across: str | None) -> pd.DataFrame:
    """Get the rows of the analysis of a result, in the order of the points.

    A single simulation has no dimension (one point, `point` 0), a scan one
    besides the draws `across`; its position is the column `point`, the
    position of the draw the column `draw`, followed by the substance; the
    rows are ordered by the point and then the draw.

    Raises:
        ValueError: if the scan has more than one dimension besides the draws.
    """
    dims = scan_dimensions(res, across) if res.dims else []
    if len(dims) > 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    names = {
        **dict.fromkeys(dims, "point"),
        **({across: "draw"} if across is not None else {}),
    }
    df = df.rename(columns=names)
    if not dims:
        df.insert(0, "point", 0)
    positions = ["point", *(["draw"] if across is not None else [])]
    df = df.sort_values(positions, kind="stable", ignore_index=True)
    df.insert(0, "substance", "talinolol")
    return df[[*positions, *(c for c in df.columns if c not in positions)]]


def _doses(
    experiment: TalinololSimulationExperiment, res: ScanResult
) -> tuple[dict[str, np.ndarray], dict[Route | None, np.ndarray]]:
    """Get the dose of every simulation in the substance unit of the concentration.

    `cl` and `vz` require it; the dose of a simulation is the first dose of
    `DOSES` it has, else its intravenous infusion; the infusions into the
    intestine have no dose. The duration of an infusion is the time until the
    whole dose is infused [unit of time].

    Returns:
        The doses over the dimensions of the result, the `amount` [mmol] and
        the `duration` (`NaN` without), and the simulations of every route
        (`None`: without a dose).
    """
    units = res.units
    shape = tuple(res.ds.sizes[dim] for dim in res.dims)
    amounts = np.full(shape, np.nan)
    durations = np.full(shape, np.nan)
    routes: dict[Route | None, np.ndarray] = {}
    dosed = np.zeros(shape, dtype=bool)

    def amount(mass: np.ndarray, unit: str) -> np.ndarray:
        """Get the amount [mmol] of a mass of talinolol."""
        return np.asarray((Q(mass, unit) / experiment.Mr.tal).to("mmole").magnitude)

    for route, sid in DOSES.items():
        mass = start_values(res, sid).values
        selected = (mass > 0) & ~dosed
        amounts = np.where(selected, amount(mass, units[sid]), amounts)
        routes[route] = selected
        dosed |= selected

    if INFUSION in res.ds:
        ds = res.to_timecourses(INFUSION).ds
        infused = ds["value"].values
        time = np.broadcast_to(
            ds["times"].values if "times" in ds else ds["time"].values, infused.shape
        )
        # the total is the last value of a simulation, the end of the infusion
        # the first time the total is infused
        last = infused.shape[-1] - 1 - np.argmax(np.isfinite(infused)[..., ::-1], -1)
        total = np.take_along_axis(infused, last[..., None], -1)[..., 0]
        reached = np.argmax(infused >= total[..., None] * (1 - 1e-9), -1)
        end = np.take_along_axis(time, reached[..., None], -1)[..., 0]
        selected = (total > 0) & ~dosed
        amounts = np.where(selected, amount(total, units[INFUSION]), amounts)
        durations = np.where(selected, end, durations)
        routes[Route.IV_INFUSION] = selected
        dosed |= selected

    routes[None] = ~dosed
    return {"amount": amounts, "duration": durations}, routes


def calculate_talinolol_pk(
    experiment: TalinololSimulationExperiment,
    res: ScanResult,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a result.

    The non-compartmental analysis of the simulations of a route (and of those
    without a dose) at once.

    Args:
        experiment: experiment of the simulations.
        res: result of a scan or of a single simulation.
        across: the dimension of the draws of the fitted parameters, `None`
            for a result without draws.

    Returns:
        One row per simulation of the scan (and draw), in the order of the
        simulations, with its position (`point`, and `draw` with draws); one
        row for a single simulation.
    """
    units = res.units
    doses, routes = _doses(experiment, res)
    frames = []
    for route, selected in routes.items():
        if not selected.any():
            continue
        dose = {"amount": doses["amount"], "unit": "mmol"}
        if route == Route.IV_INFUSION:
            dose["duration"] = doses["duration"]
        timecourses = res.to_timecourses(
            CONCENTRATION,
            dose=None if route is None else dose,
            route=route,
            substance="talinolol",
        )
        values = timecourses.ds["value"]
        cmax = values.max(
            dim=[d for d in values.dims if d not in timecourses.sample_dims]
        )
        lloq = (LLOQ_FRACTION * cmax).where(cmax > 0)
        result = nca(Timecourses(timecourses.ds.assign(lloq=lloq)))
        df = nca_frame(result).drop(columns="nca_flags")
        position = tuple(df[dim].to_numpy() for dim in res.dims)
        auc_last = ureg.Quantity(df["auc_last"].to_numpy(), df["auc_last_unit"].iloc[0])
        for cl_key, sid in EXCRETIONS.items():
            amount = ureg.Quantity(
                end_values(res, sid).values[position], str(units[sid])
            )
            clearance = (amount / auc_last).to("ml/min")
            for key, value in {sid: amount, cl_key: clearance}.items():
                df[key] = value.magnitude
                df[f"{key}_unit"] = str(value.units)
        frames.append(_rows(df[np.reshape(selected[position], -1)], res, across))
    # the columns in the order of the first simulation which has them
    positions = [c for c in ("point", "draw") if c in frames[0].columns]
    frames.sort(key=lambda df: tuple(df[positions].iloc[0]))
    return pd.concat(frames).sort_values(positions, kind="stable", ignore_index=True)


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
