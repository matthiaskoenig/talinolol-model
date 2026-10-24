"""Simulation experiment of the study He2007."""

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


class He2007(TalinololSimulationExperiment):
    """Simulation experiment of He2007.

    12 healthy Chinese men (68.6 kg, 175.1 cm), a single oral dose of 50 mg
    talinolol (Cordanum tablet) after an overnight fast, plasma 0-60 hr (Fig2,
    mean and SD). Juan2007 reports the same subjects and data as the control
    arm of its curcumin study (identical curves and PK, Cmax 147.8 ng/ml,
    AUC0-inf 1860.0 ng*h/ml); He2007 is the one fitted, Juan2007 the duplicate.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("intervention"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        simulations["tal_po_50"] = Simulation(
            time_unit="min",
            end=61 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(50, "mg"),
                "BW": Q(68.6, "kg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        mappings["fm_tal_po_50"] = FitMapping(
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
                self, task="task_tal_po_50", xid="time", yid="[Cve_tal]"
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
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(f"{name}_PO_plasma"),
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_po_50",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 50 [mg]",
            color="black",
        )
        # data
        plots[0].add_data(
            dataset="tal_TAL",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 [mg]",
            color="black",
        )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(He2007, output_dir=He2007.__name__)
