"""Scan of the intestinal perfusion rate of talinolol, compared with Gramatte1996."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.plot.serialization_matplotlib import FigureMPL
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Gramatte1996Scan(TalinololSimulationExperiment):
    """Scan the perfusion rate of a proximal and a distal intestinal segment.

    The net uptake of talinolol in the perfused segment is compared with the
    transport rates of Gramatte1996 (Fig1).
    """

    #: color of the perfused segment
    locations: ClassVar[dict[str, str]] = {
        "proximal": "black",  # duodenum
        "distal": "#e7882b",  # jejunum1
    }

    #: perfused site of the model by location
    sites: ClassVar[list[str]] = ["duodenum", "jejunum_1"]

    infusion_rates = range(500, 751, 20)  # [µg/min]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id, study="Gramatte1996")
            for label, df_label in df.groupby("y_label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dsets[f"Gramatte1996_{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for k, location in enumerate(self.locations):
            site = self.sites[k]
            for rate in self.infusion_rates:
                # 520 µg/min -- 740 µg/min
                # 500 µg/min -- 800 µg/min  ([625 µg/min] second experiment)
                # duodenum (black), jejunum1 (orange)
                simulations[f"scan_tal_ivduo_{location}_{rate}"] = Simulation(
                    time_unit="min",
                    end=70,
                    preinit_changes={
                        **self.default_changes(),
                        f"GU__Ri_tal_{site}": Q(rate, "µg/min"),  # [625 µg/min]
                    },
                )

        return simulations

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {
            **self.figures_Gramatte1996_Fig1(),
        }

    def figures_Gramatte1996_Fig1(self) -> dict[str, FigureMPL]:
        """Transport rate depending on the perfusion rate (Gramatte1996, Fig1)."""
        f, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 6))

        # --- simulation ---
        x = Q(np.array(self.infusion_rates), "µg/min")

        # net uptake rate at the end of the perfusion [µg/min] (the median and
        # the quantiles of the draws in a run over them) per 30 cm of the
        # perfused segment: the duodenum of the model has 30 cm, its jejunum_1
        # 105 cm
        lengths = {"proximal": 1.0, "distal": 30 / 105}
        uptake: dict[str, np.ndarray] = {}
        for location, site in zip(self.locations, self.sites, strict=True):
            sid = f"GU__TALUPTAKE_{site}"
            uptake[location] = (
                lengths[location]
                * np.array(
                    [
                        self.final_value(
                            self.results[f"task_scan_tal_ivduo_{location}_{rate}"],
                            sid,
                            "µmole/min",
                        )
                        for rate in self.infusion_rates
                    ],
                    dtype=float,
                )
                * self.Mr.tal.to("µg/µmole").magnitude
            )

        ax.set_title(
            "Gramatte1996",
            fontdict={"fontsize": self.tick_font_size, "fontweight": "bold"},
        )
        ax.set_xlabel("talinolol perfusion rate [µg/min]", fontdict=self.scan_font)
        ax.set_ylabel(
            "talinolol transport rate [µg/30cm/min]",
            fontdict=self.scan_font,
        )

        # simulation
        for location, y in uptake.items():
            color = self.locations[location]
            if self.uncertainty is not None:
                ax.fill_between(
                    x.to("µg/min").magnitude,
                    y[:, 1],
                    y[:, 2],
                    color=color,
                    alpha=self.band_alpha,
                    linewidth=0,
                )
            ax.plot(
                x.to("µg/min").magnitude,
                y[:, 0],
                marker="o",
                linestyle="-",
                color=color,
                label=f"Simulation {location}",
                markersize=5,
            )

        # data
        markers = ["o", "v", "s", "^"]
        for location, color in self.locations.items():
            for k in range(4):
                dset = self._datasets[
                    f"Gramatte1996_Fig1_transport_rate_TAL_{location.upper()}_S{k + 1}"
                ]
                # the data are in `µg/(30*cm*min)`, which sbmlsim reads as a
                # rate per cm; drawn per 30 cm as the publication gives them
                y = (dset.get_quantity("y") * Q(30, "cm")).to("µg/min")
                ax.plot(
                    dset["x"],
                    y.magnitude,
                    marker=markers[k % len(markers)],
                    linestyle="",
                    color=color,
                    markerfacecolor=color,
                    markeredgecolor="black",
                    label=f"S{k + 1} {location}",
                    markersize=8,
                )

        ax.axhline(y=0, color="black", linestyle="-")
        ax.set_xlim(right=800)

        ax.legend(fontsize=self.legend_font_size - 5, loc="lower right")

        return {"fig_Gramatte1996_Fig1": f}


if __name__ == "__main__":
    MODEL.run_experiments(Gramatte1996Scan, output_dir="scan_gramatte1996")
