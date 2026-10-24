"""Scan of the renal function, compared with Krueger2001."""

from typing import ClassVar, TypedDict, override

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.plot.serialization_matplotlib import FigureMPL
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class ScanSpec(TypedDict):
    """Definition of a single parameter scan."""

    parameter: str
    range: np.ndarray
    units: str
    label: str


class Krueger2001Scan(TalinololSimulationExperiment):
    """Scan the effect of renal function on talinolol pharmacokinetics."""

    #: pharmacokinetic parameters of the scans by simulation key, set by
    #: `figures_mpl`
    pk_dfs: dict[str, pd.DataFrame]

    #: the renal function from 0.1 to 1.9 of the normal GFR of 101 ml/min, the
    #: creatinine clearances of the study (about 10 to 150 ml/min)
    scan_map: ClassVar[dict[str, ScanSpec]] = {
        "renal": {
            "parameter": "KI__f_renal_function",
            "range": np.linspace(0.1, 1.9, num=19),
            "units": "dimensionless",
            "label": "Renal function [-]",
        },
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df = self.load_dataframe(fig_id, study="Krueger2001")
            for label, df_label in df.groupby("y_label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dsets[f"Krueger2001_{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Scan]:
        scans = {}

        # renal scans (Krueger2001)
        scan_data = self.scan_map["renal"]
        scans["scan_tal_100_renal"] = Scan(
            simulation=Simulation(
                # the renal clearance is the amount in the urine over the AUC
                # until the end, five half-lives after the dose
                time_unit="hr",
                end=72,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(100, "mg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_scan",
                    values={
                        scan_data["parameter"]: Q(
                            scan_data["range"], scan_data["units"]
                        )
                    },
                ),
            ],
        )
        return scans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        # calculate the pharmacokinetic parameters
        self.pk_dfs = self.calculate_talinolol_pk()

        return {
            **self.figures_Krueger2001_Fig3(),
        }

    def figures_Krueger2001_Fig3(self) -> dict[str, FigureMPL]:
        """Dependency renal clearance on renal function."""
        scan_data = self.scan_map["renal"]

        f, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 6), layout="constrained")

        # --- simulation ---
        sim_key = "scan_tal_100_renal"
        res = self.results[f"task_{sim_key}"]
        df = self.pk_dfs[sim_key]

        # the scanned renal function and the renal clearance [l/min]
        x = self.scanned(res, scan_data["parameter"])
        y, y_lower, y_upper = self.pk_summary(df, "cl_renal", "l/min")

        # the limits of the creatinine clearance, the autoscaling of the x-axis
        # is off from here on
        ax.set_xlim(left=0.0, right=150)

        # --- data ---
        ax.axvspan(
            90,
            150,
            # white with a grey edge, visible in the legend
            facecolor="white",
            edgecolor="lightgrey",
            lw=1,
            label="Normal renal function",
        )
        ax.axvspan(
            50,
            90,
            color=self.renal_colors["Mild renal impairment"],
            lw=0,
            label="Mild renal impairment",
        )
        ax.axvspan(
            30,
            50,
            color=self.renal_colors["Moderate renal impairment"],
            lw=0,
            label="Moderate renal impairment",
        )
        ax.axvspan(
            0,
            30,
            color=self.renal_colors["Severe renal impairment"],
            lw=0,
            label="Severe renal impairment",
        )

        dset_control = self._datasets["Krueger2001_Fig3_clearance_renal_control"]
        dset_increased_renal_impairment = self._datasets[
            "Krueger2001_Fig3_clearance_renal_increased_renal_impairment"
        ]

        ax.set_title(
            "Krueger2001",
            fontdict={"fontsize": self.tick_font_size, "fontweight": "bold"},
        )
        ax.set_xlabel("creatinine clearance [ml/min]", fontdict=self.font)
        ax.set_ylabel("renal clearance [l/min]", fontdict=self.font)

        # simulation, the renal function scaled to the creatinine clearance
        if y_lower is not None and y_upper is not None:
            ax.fill_between(
                x.magnitude * 101,
                y_lower.magnitude,
                y_upper.magnitude,
                color="black",
                alpha=self.band_alpha,
                linewidth=0,
            )
        ax.plot(
            x.magnitude * 101,
            y.magnitude,
            marker="o",
            linestyle="-",
            color="black",
            label="Simulation",
            markersize=5,
        )

        # data
        ax.plot(
            dset_control["x"],
            dset_control["y"] / 1000,  # [ml/min] -> [l/min]
            marker="o",
            linestyle="",
            color="black",
            markerfacecolor="black",
            label="Krueger2001 control",
            markersize=10,
        )

        ax.errorbar(
            x=[114.44],
            xerr=[14.37],
            # the mean and SD of the renal clearance [ml/min] -> [l/min]
            y=[146.54 / 1000],
            yerr=[53.38 / 1000],
            marker="s",
            linestyle="",
            color="black",
            label="Krueger2001 control mean±SD (n=12)",
            markersize=8,
        )

        ax.plot(
            dset_increased_renal_impairment["x"],
            dset_increased_renal_impairment["y"] / 1000,  # [ml/min] -> [l/min]
            marker="o",
            linestyle="",
            color="black",
            markerfacecolor="darkgrey",
            label="Krueger2001 renal impairment",
            markersize=10,
        )

        ax.errorbar(
            x=[27.00],
            xerr=[13.59],
            y=[32.92 / 1000],
            yerr=[34.30 / 1000],
            marker="s",
            linestyle="",
            color="black",
            markerfacecolor="darkgrey",
            label="Krueger2001 renal impairment mean±SD (n=12)",
            markersize=8,
        )

        # the legend right of the axes, the data fill the axes
        ax.legend(
            fontsize=self.legend_font_size - 3,
            loc="upper left",
            bbox_to_anchor=(1.02, 1.0),
        )

        return {"fig_Krueger2001_Fig3": f}


if __name__ == "__main__":
    MODEL.run_experiments(Krueger2001Scan, output_dir="scan_krueger2001")
