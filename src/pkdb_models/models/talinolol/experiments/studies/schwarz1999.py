"""Simulation experiment of the study Schwarz1999."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Schwarz1999(TalinololSimulationExperiment):
    """Simulation experiment of Schwarz1999.

    9 healthy men, a single oral dose of 50 mg talinolol (tablet, Cordanum)
    after an overnight fast, serum 0-24 hr and urine 0-48 hr. The serum time
    course (Fig1) has no error bars. The individual amounts in the urine (Tab1)
    are the subjects of the mean, an aggregate of the same data. Schwarz2000
    reports the placebo phase of 8 of these subjects again.

    The R-verapamil arm (2 x 60 mg, 15 min before and after talinolol) is not
    simulated: R-verapamil decreased the exposure (AUC0-24 ratio 0.76, urinary
    recovery 0.74) with an earlier tmax and an unchanged renal clearance, the
    opposite of an inhibition of the intestinal P-gp, and there is no
    documented factor of the process (an inhibition of the intestinal uptake
    by OATP is discussed).
    """

    tissues: ClassVar[dict[str, str]] = {
        "serum": "[Cve_tal]",
        "urine": "Aurine_tal",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1", "Tab1a_mean", "Tab1a"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if fig_id == "Tab1a":
                    dset.unit_conversion("value", 1 / self.Mr.tal)
                else:
                    dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "tal_po_50": Simulation(
                time_unit="min",
                end=50 * 60,  # at least 48 hours for urine
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(50, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        for tissue, yid in self.tissues.items():
            mappings[f"fm_tal_po_50_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"TAL_{tissue}",
                    xid="time",
                    yid="mean",
                    # the serum time course (Fig1) has no error bars
                    yid_sd=None if tissue == "serum" else "mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_tal_po_50", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue),
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        for k in range(1, 10):
            mappings[f"fm_tal_po_50_urine_S{k}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"TAL_urine_S{k}",
                    xid="time",
                    yid="value",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task="task_tal_po_50", xid="time", yid="Aurine_tal"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
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
        return self.figures_by_sid(
            self.figure_concentration(),
            self.figure_amount(),
        )

    def figure_concentration(self) -> Figure:
        """Concentration in serum."""
        f = Figure(
            experiment=self,
            sid="Fig1_PO_serum",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(
            xaxis=Axis(self.label_time, unit="hour", max=25), legend=True
        )
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
            dataset="TAL_serum",
            xid="time",
            yid="mean",
            yid_sd=None,
            count="count",
            label="50 [mg]",
            color="black",
        )
        return f

    def figure_amount(self) -> Figure:
        """Cumulative amount in urine."""
        f = Figure(
            experiment=self,
            sid="Tab1_PO_urine",
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
            label="Sim 50 [mg]",
            color="black",
        )

        # data
        for k in range(1, 10):
            plots[0].add_data(
                dataset=f"TAL_urine_S{k}",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label="50 [mg] individual" if k == 1 else None,
                color="darkgrey",
                marker="o",
                linestyle="",
            )

        plots[0].add_data(
            dataset="TAL_urine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 [mg]",
            color="black",
            linestyle="",
        )

        return f


if __name__ == "__main__":
    MODEL.run_experiments(Schwarz1999, output_dir=Schwarz1999.__name__)
