"""Simulation experiment of the study Terhaag1983."""

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


class Terhaag1983(TalinololSimulationExperiment):
    """Simulation experiment of Terhaag1983.

    Three healthy men received 200 mg talinolol orally (2 coated tablets)
    after an overnight fast, plasma until 24 hr. The log axis of Fig 1 has
    misprinted nmol/l labels (1870 and 187 for 1375 and 137.5); the copy of
    the data is recalibrated against the ng/ml labels.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                # concentrations are in nmol/l, no conversion
                dsets[label] = DataSet.from_df(df_label, self.ureg)

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        simulations["tal_po_200"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(200, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        for k in range(1, 4):
            mappings[f"fm_tal_po_200_plasma_S{k}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"plasma_S{k}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_tal_po_200", xid="time", yid="[Cve_tal]"
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
        """Concentration in plasma."""
        f = Figure(
            experiment=self,
            sid="Fig1_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_po_200",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 200 [mg]",
            color="black",
        )

        # data
        for k in range(1, 4):
            plots[0].add_data(
                dataset=f"plasma_S{k}",
                xid="time",
                yid="value",
                count="count",
                label="200 [mg]" if k == 1 else None,
                color="black",
            )

        return self.figures_by_sid(f)


if __name__ == "__main__":
    MODEL.run_experiments(Terhaag1983, output_dir=Terhaag1983.__name__)
