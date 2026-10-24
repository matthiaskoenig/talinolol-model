"""Simulation experiment of the study Han2009."""

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


class Han2009(TalinololSimulationExperiment):
    """Simulation experiment of Han2009.

    18 healthy Chinese men (ABCB1 C3435T 6 CC, 6 CT, 6 TT, not selected for an
    effect: the genotype groups do not differ, Tab2), a single oral dose of
    100 mg talinolol (tablet) after an overnight fast and 14 days of placebo,
    plasma 0-36 hr (Fig1, mean and SD). The cohort of mixed genotypes is
    simulated with the P-gp activity of the wildtype (genotype NR).

    The silymarin arm (140 mg t.i.d. for 14 days, AUC ratio 1.30) is not
    simulated: no in vivo factor of silymarin on the intestinal P-gp is known
    and no other study has the interaction to test it with.

    The exposure of the study is the lowest of all 100 mg studies (AUC0-inf
    1490 ng*h/ml, He2012 2619, Krueger2001 3378) with a normal half-life (12.2
    hr); the reported CL/F 6.75 l/hr does not follow from the dose and the AUC
    (67.1 l/hr), a factor 10 error of the paper.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("intervention"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=37 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        mappings["fm_tal_po_100"] = FitMapping(
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
            name=f"{self.__class__.__name__}",
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

        # data
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
    MODEL.run_experiments(Han2009, output_dir=Han2009.__name__)
