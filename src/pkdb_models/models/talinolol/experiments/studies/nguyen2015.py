"""Simulation experiment of the study Nguyen2015."""

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


class Nguyen2015(TalinololSimulationExperiment):
    """Simulation experiment of Nguyen2015.

    10 healthy Caucasians (8 men), a single oral dose of 100 mg talinolol
    (film-coated tablet, Cordanum 100) after an overnight fast, plasma 0-48 hr
    and urine 0-48 hr. The subjects are ABCB1 C3435T TT (7) and CT (3), not
    selected by the genotype; the authors find no association of the genotype
    with the pharmacokinetics, so the genotype is not reported (NR) in the
    metadata, as for the other unselected populations.

    The naringin arm (350 mg t.i.d. for 6 days) is not simulated: naringin did
    not change the pharmacokinetics (geometric mean ratios 0.90-0.98, all 90 %
    CIs include 1) and there is no transporter factor of naringin to test.

    The urine is given three times for the same subjects: the mean time course
    (Fig2, fitted), the mean amount 0-48 hr (Tab1a) and the 10 individual
    amounts (Fig3c); the latter two are aggregates of the same data.
    """

    yids: ClassVar[dict[str, str]] = {
        "Tab1a": "Aurine_tal",
        "Fig1": "[Cve_tal]",
        "Fig2": "Aurine_tal",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in [
            "Tab1a",  # cumulative amount urine 48 h (mean, sd)
            "Fig1",  # concentration talinolol
            "Fig2",  # cumulative amount urine time course (mean)
            "Fig3c",  # cumulative amount urine 48 h individual
        ]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if fig_id == "Fig3c":
                    dset.unit_conversion("value", 1 / self.Mr.tal)
                else:
                    dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
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
        mappings = {}

        for fig_id, yid in self.yids.items():
            tissue = "plasma" if fig_id == "Fig1" else "urine"
            mappings[f"fm_tal_po_100_{fig_id}_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{fig_id}_TAL",
                    xid="time",
                    yid="mean",
                    # the mean time course of the urine (Fig2) has no error bars
                    yid_sd=None if fig_id == "Fig2" else "mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_tal_po_100", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA if fig_id == "Fig1" else Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,  # film-coated tablet
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        for k in range(1, 11):
            mappings[f"fm_tal_po_100_S{k}_urine"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3c_TAL_S{k}a",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_100",
                    xid="time",
                    yid="Aurine_tal",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,  # film-coated tablet
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_plasma(),
            **self.figure_urine(),
        }

    def figure_plasma(self) -> dict[str, Figure]:
        """Figure of the talinolol plasma concentration."""
        f = Figure(
            experiment=self,
            sid="Fig1_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_plasma = f.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_plasma[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots_plasma[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )
        # data
        plots_plasma[0].add_data(
            dataset="Fig1_TAL",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg]",
            color="black",
            linestyle="--",
        )
        return self.figures_by_sid(f)

    def figure_urine(self) -> dict[str, Figure]:
        """Figure of the talinolol amount in the urine."""
        f = Figure(
            experiment=self,
            sid="Fig2_PO_urine",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_urine = f.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_urine[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        # simulation
        plots_urine[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="Aurine_tal",
            label="Sim 100 [mg]",
            color="black",
        )

        # data
        for k in range(1, 11):
            plots_urine[0].add_data(
                dataset=f"Fig3c_TAL_S{k}a",
                xid="time",
                yid="value",
                count="count",
                label="100 [mg] individual" if k == 1 else None,
                color="darkgrey",
                marker="o",
                linestyle="",
            )

        for fig_id, label in [
            ("Fig2", "100 [mg] mean (Fig2)"),
            ("Tab1a", "100 [mg] Ae0-48 (Tab1)"),
        ]:
            plots_urine[0].add_data(
                dataset=f"{fig_id}_TAL",
                xid="time",
                yid="mean",
                yid_sd="mean_sd" if fig_id == "Tab1a" else None,
                count="count",
                label=label,
                color="tab:orange" if fig_id == "Tab1a" else "black",
                linestyle="--" if fig_id == "Fig2" else "",
            )

        return self.figures_by_sid(f)


if __name__ == "__main__":
    MODEL.run_experiments(Nguyen2015, output_dir=Nguyen2015.__name__)
