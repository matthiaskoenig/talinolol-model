"""Simulation experiment of infusions of talinolol into the intestine."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class IntestineInfusionExperiment(TalinololSimulationExperiment):
    """Tests talinolol infusion.

    GU__Ri_tal_duodenum [mg/min]
    GU__Ri_tal_jejunum_1 [mg/min]
    GU__Ri_tal_jejunum_2 [mg/min]
    GU__Ri_tal_ileum_1 [mg/min]
    GU__Ri_tal_ileum_2 [mg/min]
    GU__Ri_tal_colon [mg/min]
    """

    sites: ClassVar[list[str]] = [
        "duodenum",
        "jejunum_1",
        "jejunum_2",
        "ileum_1",
        "ileum_2",
        "colon",
    ]

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for site in self.sites:
            simulations[f"tal_iv_{site}"] = Simulation(
                time_unit="min",
                end=30 + 30 + 20 * 60,
                preinit_changes={
                    **self.default_changes(),
                    f"GU__Ri_tal_{site}": Q(1, "mg/min"),
                },
                changes=[
                    Change(
                        30,
                        {
                            **self.default_changes(),
                            f"GU__Ri_tal_{site}": Q(0, "mg/min"),
                        },
                    )
                ],
            )
        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_application",
            num_rows=2,
            num_cols=2,
            name="Intestine iv talinolol application",
        )
        plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)

        sids = [
            "[Cve_tal]",
            "[LI__tal]",
            "Aurine_tal",
            "Afeces_tal",
        ]

        for k, sid in enumerate(sids):
            self.plot_grouped_species(sid, plots[k])

        return self.figures_by_sid(fig)

    def plot_grouped_species(self, sid: str, plot: Plot) -> None:
        """Plot a variable of the infusions into every site.

        Args:
            sid: id of the variable.
            plot: plot to add the curves to.
        """
        plot.set_yaxis(self.labels[sid], unit=self.units[sid])

        for site in self.sites:
            plot.add_data(
                task=f"task_tal_iv_{site}",
                xid="time",
                yid=sid,
                label=f"TAL {self.sites_label[site]}",
            )


if __name__ == "__main__":
    MODEL.run_experiments(IntestineInfusionExperiment, output_dir="test")
