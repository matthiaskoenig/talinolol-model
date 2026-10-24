"""Simulation experiment of the study Wang2013."""

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


class Wang2013(TalinololSimulationExperiment):
    """Simulation experiment of Wang2013.

    18 healthy Chinese men (6 each of ABCB1 3435 CC, CT and TT) received 100 mg
    talinolol orally on day 14 of 500 mg quercetin or placebo daily. The
    placebo arm is an outlier: Cmax 543 ng/ml and AUCinf 10478 ng*h/ml are 2-3
    times those of the other studies of 100 mg (Tubic2006a, Westphal2000a),
    which the body weight of 55.7 kg does not explain, the quercetin arm has
    106 ng/ml before the dose, and the samples are reported until 48 hr while
    the methods sample until 24 hr. The quercetin arm is not simulated (no
    documented factor of the induction of P-gp).
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig2"]:
            df = self.load_dataframe(fig_id)
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
            end=50 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        mappings["fm_wang2013_tal_po_100"] = FitMapping(
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
        name = "Fig2"
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
    MODEL.run_experiments(Wang2013, output_dir=Wang2013.__name__)
