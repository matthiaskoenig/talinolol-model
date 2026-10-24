"""Base class of the talinolol simulation experiments."""

from collections.abc import Iterable, Mapping
from typing import ClassVar, NamedTuple

import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.typing import ColorType
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from pkpdsim.scan import end_values, point_band, point_timecourse, start_values
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.units import Quantity

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.talinolol_pk import (
    calculate_talinolol_pk,
    summarize,
)

#: the segments of the intestine, from the duodenum to the colon
SEGMENTS: tuple[str, ...] = (
    "duodenum",
    "jejunum_1",
    "jejunum_2",
    "ileum_1",
    "ileum_2",
    "colon",
)


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    tal: Quantity


class TalinololSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the talinolol simulation experiments.

    The plasma (and serum) concentration of talinolol is the one of the venous
    plasma `[Cve_tal]`; the excreted amounts are `Aurine_tal` (urine),
    `Afeces_tal` (feces) and `LI__Abile_tal` (bile, cumulative). An oral dose
    is `PODOSE_tal`, an intravenous bolus `IVDOSE_tal` and an intravenous
    infusion the rate `Ri_tal` [mg/min] (its cumulative dose `cum_dose_tal`),
    an infusion into a segment of the intestine `GU__Ri_tal_<segment>`
    [mg/min].
    """

    pkpd_model = MODEL
    selections = (
        "time",
        # dosing
        "IVDOSE_tal",
        "PODOSE_tal",
        "cum_dose_tal",
        # plasma
        "[Cve_tal]",
        # excretion
        "Aurine_tal",
        "Afeces_tal",
        "LI__Abile_tal",
        "LI__Cbile_tal",
        "LI__TALEX",
        "KI__TALEX",
        # liver
        "[LI__tal]",
        # intestine: the lumen and the net uptake of every segment
        "[Cduodenum_tal]",
        *(f"[GU__tal_{segment}]" for segment in SEGMENTS[1:]),
        *(f"GU__TALUPTAKE_{segment}" for segment in SEGMENTS),
        # cases
        "KI__f_renal_function",
        "GU__f_pgp",
        "LI__f_pgp",
        "GU__f_oatp2b1",
        "LI__f_oatp1b1",
        "LI__f_EHC",
        "f_cirrhosis",
    )

    font: ClassVar[dict[str, str | int]] = {"weight": "bold", "size": 22}
    scan_font: ClassVar[dict[str, str | int]] = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 13
    suptitle_font_size = 40

    # ----------- ABCB1 (MDR1) genotypes --------------
    colors_MDR1_genotype: ClassVar[dict[str, str]] = {
        "ABCB1_CC": "black",
        "ABCB1_CT": "#08519c",
        "ABCB1_TT": "#3182bd",
    }
    #: the activity of the intestinal P-glycoprotein (`GU__f_pgp`) of the ABCB1
    #: C3435T genotypes: the AUC of talinolol of TT is 0.64 times the one of
    #: CC (He2012, 100 mg oral), which the factor 1.75 of TT reproduced with
    #: the start values of the model before the fit (0.73 with the adopted
    #: fit); CT is set to the wildtype, its AUC ratio 1.17 (He2012) is not
    #: different from CC, and Zhang2005, Siegmund2003 and Nguyen2015 find no
    #: effect of the genotype at all (TODO.md)
    activity_MDR1_genotype: ClassVar[dict[str, float]] = {
        "ABCB1_CC": 1.0,
        "ABCB1_CT": 1.0,
        "ABCB1_TT": 1.75,
    }

    # ----------- P-glycoprotein interactions --------------
    colors_pg_function: ClassVar[dict[str, str]] = {
        "P-gp normal": "black",
        "P-gp ↓": "#e34a33",  # inhibition
        "P-gp ↑": "#3182bd",  # increased
    }
    #: the activity of the intestinal P-glycoprotein (`GU__f_pgp`) under a
    #: coadministration, documented factors which are not fitted (the arms are
    #: validation data), see `pgp_interaction`
    pgp_interaction: ClassVar[dict[str, float]] = {
        # no coadministration
        "none": 1.0,
        # rifampicin 600 mg/day, 9 days (Westphal2000b): duodenal P-gp protein
        # 4.2 fold (Western blot); observed AUC ratio 0.65 oral, 0.79 IV, the
        # adopted fit gives 0.38 oral (TODO.md)
        "rifampicin": 4.2,
        # St John's wort 900 mg/day, 12 days (Schwarz2007): duodenal MDR1 mRNA
        # 1.6 fold in the same subjects; oral AUC ratio about 0.75 observed,
        # 0.77 with the adopted fit
        "st_johns_wort": 1.6,
        # erythromycin 2 g (Schwarz2000): inhibition of the intestinal P-gp; no
        # in vivo inhibition fraction is known, 0.5 is of the size of the
        # observed ratios (AUC0-24 1.52, urinary recovery 1.36); the adopted
        # fit gives an oral AUC ratio of 1.33
        "erythromycin": 0.5,
        # simvastatin (Bernsdorf2006) and poloxamer 188 (Bogman2005): no effect
        # (AUC ratio 1.07 and 0.91, not significant)
        "simvastatin": 1.0,
        "poloxamer": 1.0,
    }

    # ----------- Renal function --------------
    #: the renal function `KI__f_renal_function` is the GFR relative to the
    #: healthy 101 ml/min, a measured creatinine clearance X ml/min is X/101
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    # ----------- Labels and units --------------
    label_time = "time"
    label_tal = "talinolol"
    label_tal_plasma = "talinolol plasma"
    label_tal_urine = "talinolol urine"
    label_tal_urine_rate = "talinolol excretion urine"
    label_tal_feces = "talinolol feces"
    label_tal_bile = "talinolol bile"
    label_tal_bile_rate = "talinolol excretion bile"

    units: ClassVar[Mapping[str, str]] = {
        "time": "hr",
        "IVDOSE_tal": "mg",
        "PODOSE_tal": "mg",
        "cum_dose_tal": "mg",
        "[Cve_tal]": "µM",
        "Aurine_tal": "µmole",
        "Afeces_tal": "µmole",
        "LI__Abile_tal": "µmole",
        "LI__Cbile_tal": "µM",
        "LI__TALEX": "µmole/min",
        "KI__TALEX": "µmole/min",
        "[LI__tal]": "µM",
        "[Cduodenum_tal]": "µM",
        **{f"[GU__tal_{segment}]": "µM" for segment in SEGMENTS[1:]},
        **{f"GU__TALUPTAKE_{segment}": "µmole/min" for segment in SEGMENTS},
    }
    labels: ClassVar[Mapping[str, str]] = {
        "time": "time",
        "IVDOSE_tal": "IV dose talinolol",
        "PODOSE_tal": "oral dose talinolol",
        "cum_dose_tal": "infused dose talinolol",
        "[Cve_tal]": label_tal_plasma,
        "Aurine_tal": label_tal_urine,
        "Afeces_tal": label_tal_feces,
        "LI__Abile_tal": label_tal_bile,
        "LI__Cbile_tal": label_tal_bile,
        "LI__TALEX": label_tal_bile_rate,
        "KI__TALEX": label_tal_urine_rate,
        "[LI__tal]": "talinolol liver",
        "[Cduodenum_tal]": "talinolol duodenum",
        **{
            f"[GU__tal_{segment}]": f"talinolol {segment.replace('_', '')}"
            for segment in SEGMENTS[1:]
        },
        **{
            f"GU__TALUPTAKE_{segment}": (
                f"net uptake talinolol {segment.replace('_', '')}"
            )
            for segment in SEGMENTS
        },
        "KI__f_renal_function": "renal function",
        "GU__f_pgp": "P-gp activity (intestine)",
        "LI__f_pgp": "P-gp activity (liver)",
        "GU__f_oatp2b1": "OATP2B1 activity (intestine)",
        "LI__f_oatp1b1": "OATP1B1 activity (liver)",
    }

    sites_color: ClassVar[dict[str, str]] = {
        "duodenum": "black",
        "jejunum_1": "#e7882b",
        "jejunum_2": "#c13d34",
        "ileum_1": "#c64599",
        "ileum_2": "#8059a3",
        "colon": "#2c7cc2",
    }
    #: legend names of the intestinal segments
    sites_label: ClassVar[dict[str, str]] = {
        "duodenum": "duodenum",
        "jejunum_1": "jejunum 1",
        "jejunum_2": "jejunum 2",
        "ileum_1": "ileum 1",
        "ileum_2": "ileum 2",
        "colon": "colon",
    }

    pk_labels: ClassVar[Mapping[str, str]] = {
        "auc_last": "AUCend",
        "auc_inf_obs": "AUC",
        "cl": "Total clearance",
        "cl_renal": "renal clearance",
        "cl_fecal": "fecal clearance",
        "cmax": "Cmax",
        "thalf": "Half-life",
        "lambda_z": "kel",
        "vz": "vd",
        "Aurine_tal": "Amount urine",
        "Afeces_tal": "Amount feces",
    }

    pk_units: ClassVar[Mapping[str, str]] = {
        "auc_last": "µmole/l*hr",
        "auc_inf_obs": "µmole/l*hr",
        "cl": "ml/min",
        "cl_renal": "ml/min",
        "cl_fecal": "ml/min",
        "cmax": "µmole/l",
        "thalf": "hr",
        "lambda_z": "1/hr",
        "vz": "l",
        "Aurine_tal": "µmole",
        "Afeces_tal": "µmole",
    }

    # molecular weight of talinolol
    Mr: ClassVar[MolecularWeights] = MolecularWeights(tal=Q(363.495, "g/mole"))

    #: the opacity of the bands of the draws of the fitted parameters in the
    #: figures of the scans
    band_alpha = 0.15

    @staticmethod
    def pk_id(pk_key: str, route: str) -> str:
        """Get the column of a pharmacokinetic parameter after a dose of a route.

        The clearance and the volume of distribution after an oral dose are the
        apparent ones of pkpdutils (`cl_f`, `vz_f`).

        Args:
            pk_key: the parameter, a key of `pk_labels`.
            route: the route of the dose, "po" or "iv".
        """
        if route == "po" and pk_key in ("cl", "vz"):
            return f"{pk_key}_f"
        return pk_key

    def calculate_talinolol_pk(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the simulations.

        Args:
            scans: keys of the simulations (scans), by default all simulations.

        Returns:
            The parameters by key of the simulation, one row per simulation of
            a scan and per draw of the fitted parameters in a run over them
            (`uncertainty`), see `talinolol_pk.calculate_talinolol_pk`.
        """
        keys = list(self._simulations) if scans is None else list(scans)
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_talinolol_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
        }

    # ----------- Figures over the draws of the fitted parameters --------------
    # In a run over the draws of the fitted parameters (`run_simulation
    # pkdb_models.models.talinolol --uncertainty`) every simulation of a scan
    # is simulated for every draw: the figures of the scans draw the median of
    # the draws with the band of their quantiles, without draws the simulation.

    def across(self) -> str | None:
        """Get the dimension of the draws of the fitted parameters, `None` without."""
        return None if self.uncertainty is None else self.uncertainty.id

    def scanned(self, res: ScanResult, parameter_id: str) -> Quantity:
        """Get the values of the scanned parameter at the points of a scan."""
        values = start_values(res, parameter_id)
        across = self.across()
        if across is not None:
            values = values.isel({across: 0})
        return Q(values.values, res.units[parameter_id])

    def plot_timecourse(
        self,
        ax: Axes,
        res: ScanResult,
        sid: str,
        color: ColorType,
        label: str | None = None,
        **point: int,
    ) -> tuple[Quantity, Quantity, float]:
        """Plot the timecourse of a point of a scan with the band of its draws.

        Args:
            ax: the axes.
            res: the result of the scan or of a simulation.
            sid: the variable, drawn in the units of the figures (`units`).
            color: the color of the line and of the band.
            label: the label of the line.
            **point: the position of the point along the dimensions of the
                scan, none for a simulation.

        Returns:
            The time and the values (the median of the draws in a run over
            them) and the maximum of the values or of the band in the units
            of the figure.
        """
        run = self.uncertainty
        unit = self.units[sid]
        if run is None:
            time, values = point_timecourse(res, sid, **point)
        else:
            time, lower, values, upper = point_band(
                res, sid, across=run.id, quantiles=run.quantiles, **point
            )
        t_vec = Q(time, res.units["time"]).to(self.units["time"])
        c_vec = Q(values, res.units[sid]).to(unit)
        top = float(np.nanmax(c_vec.magnitude))
        if run is not None:
            upper_vec = Q(upper, res.units[sid]).to(unit).magnitude
            ax.fill_between(
                t_vec.magnitude,
                Q(lower, res.units[sid]).to(unit).magnitude,
                upper_vec,
                color=color,
                alpha=self.band_alpha,
                linewidth=0,
            )
            top = max(top, float(np.nanmax(upper_vec)))
        ax.plot(
            t_vec.magnitude, c_vec.magnitude, color=color, linewidth=2.0, label=label
        )
        return t_vec, c_vec, top

    def pk_summary(
        self, df: pd.DataFrame, key: str, target: str
    ) -> tuple[Quantity, Quantity | None, Quantity | None]:
        """Get a pharmacokinetic parameter at the points of a scan.

        Args:
            df: the parameters of the scan, see `calculate_talinolol_pk`.
            key: the parameter (a column of `df`).
            target: the unit of the values.

        Returns:
            The values in the order of the points (the median of the draws in
            a run over them), and the lower and the upper quantile of the
            draws, `None` without draws.
        """
        unit = str(df[f"{key}_unit"].iloc[0])
        run = self.uncertainty
        if run is None:
            return Q(df[key].to_numpy(dtype=float), unit).to(target), None, None
        summary = summarize(df, key, run.quantiles)
        median, lower, upper = (
            Q(summary[column].to_numpy(), unit).to(target)
            for column in ["median", "lower", "upper"]
        )
        return median, lower, upper

    def final_value(
        self, res: ScanResult, sid: str, target: str
    ) -> tuple[float, float | None, float | None]:
        """Get the value of a variable at the end of a simulation.

        Args:
            res: the result of a simulation.
            sid: the variable.
            target: the unit of the value.

        Returns:
            The value (the median of the draws in a run over them), and the
            lower and the upper quantile of the draws, `None` without draws.
        """
        values = Q(end_values(res, sid).values, res.units[sid]).to(target).magnitude
        run = self.uncertainty
        if run is None:
            return float(values), None, None
        low, high = run.quantiles
        return (
            float(np.nanmedian(values)),
            float(np.nanquantile(values, low)),
            float(np.nanquantile(values, high)),
        )
