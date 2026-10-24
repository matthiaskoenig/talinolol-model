"""Simulation experiment of the study Schwarz2000."""

from typing import ClassVar, override

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


class Schwarz2000(TalinololSimulationExperiment):
    """Simulation experiment of Schwarz2000.

    8 healthy men (the subjects of Schwarz1999 without subject 4), a single
    oral dose of 50 mg talinolol (tablet, Cordanum) after an overnight fast
    with placebo or with erythromycin (2 x 1 g, 15 min before and after
    talinolol), serum 0-24 hr and urine 0-48 hr. The error bars of the serum
    (Fig1) are standard errors (CV 9-11 % at 10-12 hr against 19 % of the
    individual AUC); the copy of the data stores them as `se` and the standard
    deviation `se * sqrt(8)`.

    The placebo phase is the one of Schwarz1999 (the same subjects and
    samples, identical individual values), an aggregate of data fitted there.

    Erythromycin inhibits the intestinal P-gp, `pgp_interaction`
    ("erythromycin"): observed AUC0-24 ratio 1.52, Cmax 1.26 and urinary
    recovery 1.36 with an unchanged renal clearance (10.6 vs 10.8 l/hr); the
    factor is documented, not fitted, the arm is validation data. The earlier
    tmax with erythromycin (1.69 vs 3.15 hr) is not described by the model.
    """

    tissues: ClassVar[list[str]] = ["serum", "urine"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in [
            "Fig1",  # mean serum time course
            "Tab1a_mean",  # mean Aurine
            "Tab1a",  # individual Aurine
        ]:
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
        simulations: dict[str, Simulation] = {}
        simulations["tal_po_50"] = Simulation(
            time_unit="min",
            end=50 * 60,  # at least 48 hours for urine
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(50, "mg"),
            },
        )

        simulations["tal_po_50_inhibition"] = Simulation(
            time_unit="min",
            end=50 * 60,  # at least 48 hours for urine
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(50, "mg"),
                # inhibition of the intestinal P-gp by erythromycin 2 g
                "GU__f_pgp": Q(self.pgp_interaction["erythromycin"], "dimensionless"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        for tissue in self.tissues:
            suffix = "_mean" if tissue == "urine" else ""
            mappings[f"fm_tal_po_50_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"TAL_{tissue}{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_50",
                    xid="time",
                    yid="[Cve_tal]" if tissue == "serum" else "Aurine_tal",
                ),
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
            if k == 4:
                continue
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

        # erythromycin: the serum and the mean amount in the urine
        for tissue in self.tissues:
            suffix = "_mean" if tissue == "urine" else ""
            key = "fm_tal_po_50_inhibition"
            mappings[key if tissue == "serum" else f"{key}_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"TAL_ERY_{tissue}{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_50_inhibition",
                    xid="time",
                    yid="[Cve_tal]" if tissue == "serum" else "Aurine_tal",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue),
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.ERYTHROMYCIN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self.figure_concentration(),
            self.figure_amount(),
            self.figure_pgfunction(),
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

        plots[0].add_data(
            dataset="TAL_serum",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 [mg]",
            color="black",
        )

        return f

    def figure_amount(self) -> Figure:
        """Cumulative amount in urine with placebo and with erythromycin."""
        f = Figure(
            experiment=self,
            sid="Tab1_PO_urine",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )

        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        arms = {
            # intervention: (task, label, color)
            "TAL": (
                "task_tal_po_50",
                "50 [mg]",
                self.colors_pg_function["P-gp normal"],
            ),
            "TAL_ERY": (
                "task_tal_po_50_inhibition",
                "50 [mg] P-gp inhibition",
                self.colors_pg_function["P-gp ↓"],
            ),
        }
        for intervention, (task, label, color) in arms.items():
            # simulation
            plots[0].add_data(
                task=task,
                xid="time",
                yid="Aurine_tal",
                label=f"Sim {label}",
                color=color,
            )
            # data
            for k in range(1, 10):
                if k == 4:
                    continue
                plots[0].add_data(
                    dataset=f"{intervention}_urine_S{k}",
                    xid="time",
                    yid="value",
                    yid_sd=None,
                    count="count",
                    label=f"{label} individual" if k == 1 else None,
                    color=color,
                    marker="o",
                    linestyle="",
                    alpha=0.4,
                )
            plots[0].add_data(
                dataset=f"{intervention}_urine_mean",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=color,
                linestyle="",
            )

        return f

    def figure_pgfunction(self) -> Figure:
        """Concentration in serum with and without the P-gp inhibition."""
        f = Figure(
            experiment=self,
            sid="Fig1_PO_serum_pginhibition",
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

        plots[0].add_data(
            task="task_tal_po_50_inhibition",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 50 [mg] P-gp inhibition",
            color="#e34a33",
        )

        interventions = {
            "TAL": self.colors_pg_function["P-gp normal"],
            "TAL_ERY": self.colors_pg_function["P-gp ↓"],
        }
        for intervention, color in interventions.items():
            plots[0].add_data(
                dataset=f"{intervention}_serum",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="50 [mg]" if intervention == "TAL" else "50 [mg] P-gp inhibition",
                color=color,
            )

        return f


if __name__ == "__main__":
    MODEL.run_experiments(Schwarz2000, output_dir=Schwarz2000.__name__)
