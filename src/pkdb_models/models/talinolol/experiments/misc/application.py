"""Simulation experiment of oral and intravenous doses of talinolol."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class ApplicationExperiment(TalinololSimulationExperiment):
    """Tests oral talinolol."""

    doses: ClassVar[list[int]] = [50, 100]
    routes: ClassVar[list[str]] = ["iv", "po"]

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        tend = 24 * 60  # [min]

        for dose in self.doses:
            for route in self.routes:
                if route == "po":
                    # a dose every day for 5 days
                    simulations[f"tal_po_{dose}"] = Simulation(
                        time_unit="min",
                        end=5 * tend,
                        preinit_changes={
                            **self.default_changes(),
                            "PODOSE_tal": Q(dose, "mg"),
                        },
                        changes=[
                            self.add_doses(
                                [day * tend for day in range(1, 5)],
                                {"PODOSE_tal": Q(dose, "mg")},
                            ),
                        ],
                    )

                elif route == "iv":
                    simulations[f"tal_iv_{dose}"] = Simulation(
                        time_unit="min",
                        end=3 * 60,
                        preinit_changes={
                            **self.default_changes(),
                            "IVDOSE_tal": Q(dose, "mg"),
                        },
                    )
        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        figures = []
        for route in self.routes:
            # the oral doses have the dose which is not yet dissolved
            sids = ["[Cve_tal]", "Aurine_tal", "Afeces_tal", "LI__Abile_tal"]
            if route == "po":
                sids += ["PODOSE_tal", "[Cduodenum_tal]"]
            fig = Figure(
                experiment=self,
                sid=f"Fig_application_{route}",
                num_rows=len(sids) // 2,
                num_cols=2,
                name=f"{'Oral' if route == 'po' else 'Intravenous'} talinolol "
                "application",
            )
            # the legends inside the panels cover the doses
            fig.settings = {**fig.settings, "legend_position": "outside"}
            plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)
            for k, sid in enumerate(sids):
                self.plot_grouped_species(sid, plots[k], route=route)
            figures.append(fig)

        return self.figures_by_sid(*figures)

    def plot_grouped_species(self, sid: str, plot: Plot, route: str) -> None:
        """Plot a variable of the simulations of every dose of a route.

        Args:
            sid: id of the variable.
            plot: plot to add the curves to.
            route: route of the doses, "po" or "iv".
        """
        plot.set_yaxis(self.labels[sid], unit=self.units[sid])

        for dose in self.doses:
            plot.add_data(
                task=f"task_tal_{route}_{dose}",
                xid="time",
                yid=sid,
                label=f"TAL {dose} mg {route.upper()}",
            )


if __name__ == "__main__":
    MODEL.run_experiments(
        ApplicationExperiment, output_dir=ApplicationExperiment.__name__
    )
