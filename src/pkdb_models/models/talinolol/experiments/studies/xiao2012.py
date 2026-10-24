"""Simulation experiment of the study Xiao2012."""

from typing import override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
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


class Xiao2012(TalinololSimulationExperiment):
    """Simulation experiment of Xiao2012.

    18 healthy Chinese men, 100 mg talinolol (tablet) with 7.5 mg midazolam
    after an overnight fast, after 14 days of placebo (TAL, MID) or genistein
    (TAL, MID, GST). Midazolam is a probe of CYP3A, talinolol is not
    metabolized, the placebo arm is talinolol alone in effect. The genistein
    arm (AUC -12 %) is not simulated: no documented factor of its effect on
    P-gp.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig2"]:
            df = self.load_dataframe(fig_id)
            # The error bars are labelled SD, but they are of the size of the SE:
            # Tab2 gives Cmax 326.6 +- 197.7 ng/ml (CV 60 %), the bars at the
            # peak are 10-20 ng/ml (CV 5-10 %), i.e. SD / sqrt(18).
            df["se"] = df["sd"]
            df["sd"] = float("nan")
            for intervention, df_intervention in df.groupby("intervention"):
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{str(intervention).replace(', ', '_')}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=40 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        mappings["fm_xiao2012_tal_po_100"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="tal_TAL_MID",
                xid="time",
                yid="mean",
                yid_se="mean_se",
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
                coadministration=Coadministration.MIDAZOLAM,
            ),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=f"{name}_PO_plasma",
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
            dataset="tal_TAL_MID",
            xid="time",
            yid="mean",
            yid_se="mean_se",
            count="count",
            label="100 [mg]",
            color="black",
        )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Xiao2012, output_dir=Xiao2012.__name__)
