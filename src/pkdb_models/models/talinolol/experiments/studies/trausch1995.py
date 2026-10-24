"""Simulation experiment of the study Trausch1995."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Trausch1995(TalinololSimulationExperiment):
    """Simulation experiment of Trausch1995.

    Twelve healthy volunteers received 30 mg talinolol as an intravenous
    infusion over 30 min and 50 mg orally (coated tablet) after an overnight
    fast, crossover; serum until 36 hr, urine in the intervals 0-4, 4-8, 8-12,
    12-24 and 24-36 hr. Fig 1 shows the individual serum curves (a: IV, main
    plot semilogarithmic and the 0-2 hr in an inset; b: oral), Fig 2 the
    individual cumulative urine (a: IV, b: oral). The curves of the panels are
    unmarked, the subjects of different panels are not the same.

    The intravenous 0-2 hr is taken from the inset (`S{k}a`), the main plot
    (`S{k}b`) only after 2 hr: its early points are mistimed and would count
    the 0-2 hr twice. The copy of the data drops the curves which are digitized
    twice (S5a = S4a, S5c = S1c, S11c = S3c) and keeps the urine at the ends of
    the collection intervals (the vertices of the polylines). The mean urine of
    Table 1 (n=12) is the fitted urine, the individual urine the same subjects
    again.
    """

    #: the individual curves of the panels in the copy of the data
    individuals: ClassVar[dict[str, tuple[int, ...]]] = {
        "a": (1, 2, 3, 4, 6, 7, 8, 9, 10, 11),  # iv serum 0-2 hr (inset)
        "b": tuple(range(1, 12)),  # iv serum > 2 hr
        "c": (1, 2, 3, 4, 6, 7, 8, 9, 10),  # po serum
        "d": tuple(range(1, 12)),  # iv urine
        "e": tuple(range(1, 12)),  # po urine
    }
    #: the route of the panels
    routes: ClassVar[dict[str, str]] = {
        "a": "iv",
        "b": "iv",
        "c": "po",
        "d": "iv",
        "e": "po",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in [
            "Tab1a",  # mean Aurine
            "Fig1",  # individual concentration time course
            "Fig2",  # individual Aurine time course
        ]:
            df = self.load_dataframe(fig_id)
            if fig_id == "Tab1a":
                for intervention, df_intervention in df.groupby("intervention"):
                    # amounts are in µmole, no conversion
                    dset = DataSet.from_df(df_intervention, self.ureg)
                    dsets[f"tal_{intervention}_urine"] = dset

            else:
                for individual in df.individual.unique():
                    df_subset = df.loc[df.individual == individual, :]
                    if individual.endswith("b"):
                        # the main plot after the 0-2 hr of the inset
                        df_subset = df_subset[df_subset.time > 2.0]
                    intervention = df_subset.intervention.unique()[0]
                    dset = DataSet.from_df(df_subset.copy(), self.ureg)
                    if fig_id == "Fig1":
                        dset.unit_conversion("value", 1 / self.Mr.tal)
                    # amounts of Fig2 are in µmole, no conversion
                    dsets[f"tal_{intervention}_{individual}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}

        # oral
        simulations["tal_po_50"] = Simulation(
            time_unit="min",
            end=40 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(50, "mg"),
            },
        )

        # intravenous infusion, 1 mg/min over 30 min
        simulations["tal_iv_30"] = Simulation(
            time_unit="min",
            end=30 + 49.5 * 60,
            preinit_changes={
                **self.default_changes(),
                "Ri_tal": Q(30, "mg") / Q(30, "min"),
            },
            changes=[
                Change(
                    30,
                    {
                        "Ri_tal": Q(0, "mg/min"),
                    },
                )
            ],
        )

        return simulations

    def metadata(self, route: str, tissue: Tissue) -> PKPDMappingMetaData:
        """Get the metadata of a mapping of the route and tissue."""
        return PKPDMappingMetaData(
            tissue=tissue,
            route=Route.IV if route == "iv" else Route.PO,
            application_form=(
                ApplicationForm.SOLUTION if route == "iv" else ApplicationForm.TABLET
            ),
            dosing=Dosing.SINGLE,
            health=Health.HEALTHY,
            fasting=Fasting.FASTED,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        # individual serum (a, b, c) and urine (d, e); a panel weighs as much as
        # the mean curve of another study, not as much as its subjects together
        for panel, individuals in self.individuals.items():
            route = self.routes[panel]
            dose = 30 if route == "iv" else 50
            urine = panel in ("d", "e")
            for k in individuals:
                mappings[f"fm_tal_{route}_{dose}_tal_S{k}{panel}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"tal_TAL_{route.upper()}_S{k}{panel}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_{route}_{dose}",
                        xid="time",
                        yid="Aurine_tal" if urine else "[Cve_tal]",
                    ),
                    weight=1 / len(individuals),
                    metadata=self.metadata(
                        route, Tissue.URINE if urine else Tissue.SERUM
                    ),
                )

        # mean urine (Table 1)
        for route, dose in (("po", 50), ("iv", 30)):
            mappings[f"fm_tal_{route}_{dose}_tal_urine"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"tal_TAL_{route.upper()}_urine",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_tal_{route}_{dose}", xid="time", yid="Aurine_tal"
                ),
                metadata=self.metadata(route, Tissue.URINE),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self.figure_serum_iv(),
            self.figure_serum_po(),
            self.figure_urine_iv(),
            self.figure_urine_po(),
        )

    def figure_serum_iv(self) -> Figure:
        """Concentration in serum after intravenous talinolol application."""
        f = Figure(
            experiment=self,
            sid="Fig1_IV_serum",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_iv_30",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 30 iv [mg]",
            color="black",
        )

        # data
        for panel in ["a", "b"]:
            for k in self.individuals[panel]:
                plots[0].add_data(
                    dataset=f"tal_TAL_IV_S{k}{panel}",
                    xid="time",
                    yid="value",
                    count="count",
                    label="30 iv [mg]" if (panel, k) == ("a", 1) else None,
                    color="black",
                )

        return f

    def figure_serum_po(self) -> Figure:
        """Concentration in serum after oral talinolol application."""
        f = Figure(
            experiment=self,
            sid="Fig1_PO_serum",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_po_50",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 50 po [mg]",
            color="black",
        )

        # data
        for k in self.individuals["c"]:
            plots[0].add_data(
                dataset=f"tal_TAL_PO_S{k}c",
                xid="time",
                yid="value",
                count="count",
                label="50 po [mg]" if k == 1 else None,
                color="black",
            )

        return f

    def figure_urine_iv(self) -> Figure:
        """Cumulative amount in urine after intravenous talinolol application."""
        f = Figure(
            experiment=self,
            sid="Fig2_IV_urine",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_iv_30",
            xid="time",
            yid="Aurine_tal",
            label="Sim 30 iv [mg]",
            color="black",
        )

        # data

        for k in self.individuals["d"]:
            plots[0].add_data(
                dataset=f"tal_TAL_IV_S{k}d",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label="30 iv [mg]" if k == 1 else None,
                color="black",
            )
        plots[0].add_data(
            dataset="tal_TAL_IV_urine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="30 iv mean [mg]",
            color="tab:orange",
            linestyle="",
        )

        return f

    def figure_urine_po(self) -> Figure:
        """Cumulative amount in urine after oral talinolol application."""
        f = Figure(
            experiment=self,
            sid="Fig2_PO_urine",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_po_50",
            xid="time",
            yid="Aurine_tal",
            label="Sim 50 po [mg]",
            color="black",
        )

        # data
        for k in self.individuals["e"]:
            plots[0].add_data(
                dataset=f"tal_TAL_PO_S{k}e",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label="50 po [mg]" if k == 1 else None,
                color="black",
            )

        plots[0].add_data(
            dataset="tal_TAL_PO_urine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 po mean [mg]",
            color="tab:orange",
            linestyle="",
        )

        return f


if __name__ == "__main__":
    MODEL.run_experiments(Trausch1995, output_dir=Trausch1995.__name__)
