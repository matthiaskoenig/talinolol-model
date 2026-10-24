"""Simulation experiment of the study Zeng2009."""

from typing import override

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Zeng2009(TalinololSimulationExperiment):
    """Simulation experiment of Zeng2009.

    16 healthy Chinese men, 100 mg talinolol with 200 ml water after an
    overnight fast, after 14 days of placebo (TAL) or bifendate (BIF, TAL). The
    bifendate arm (AUC -11 %, proposed induction of P-gp by PXR) is not
    simulated: no documented factor.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            # The error bars of Fig1 are labelled SE, but they are the SD of
            # Tab1 (3 hr 22.0 vs Cmax 209.4 +- 21.1 ng/ml, CV 10 %; the
            # individual AUC of Fig2 have the SD of Tab1); as SE they would be
            # an SD of 88 ng/ml at the peak (CV 42 %).
            df["sd"] = df["se"]
            df["se"] = float("nan")
            for label, df_label in df.groupby("intervention"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        mappings["fm_zeng2009_tal_po_100"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="tal_TAL",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_po_100", xid="time", yid="[Cve_tal]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
            ),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(f"{name}_PO_plasma"),
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )

        plots[0].add_data(
            dataset="tal_TAL",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg]",
            color="black",
        )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Zeng2009, output_dir=Zeng2009.__name__)
