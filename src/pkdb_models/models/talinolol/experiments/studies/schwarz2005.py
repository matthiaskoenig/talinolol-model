"""Simulation experiment of the study Schwarz2005."""

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


class Schwarz2005(TalinololSimulationExperiment):
    """Simulation experiment of Schwarz2005.

    24 healthy men (ABCB1 C3435T 5 CC, 13 CT, 6 TT, no association with the
    pharmacokinetics), a single oral dose of 50 mg talinolol (tablet,
    Cordanum 50) after a fast of 10 hr with water, serum 0-24 hr and urine
    0-48 hr. The exposure with water is about a third of the one of the other
    studies of the group with the same tablet (AUC0-24 329 vs 834-955 ng*hr/ml,
    urinary recovery 4.5 vs 12.9-17.7 mg) at a comparable renal clearance,
    unexplained in the paper: the mappings are outliers.

    The grapefruit juice arms (acute and chronic, AUC ratios 0.56 and 0.64,
    urinary recovery 0.56 and 0.44, inhibition of the intestinal uptake by
    OATP) are not simulated: there is no literature factor of the OATP2B1
    activity under grapefruit juice, and the ratios cannot be validated
    against the absolute values of an outlying control arm.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1", "Tab1a"]:
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"{fig_id}_tal_{intervention}")] = dset

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

        for fig_id in ["Fig1", "Tab1a"]:
            tissue = "serum" if fig_id == "Fig1" else "urine"

            mappings[self.to_sid(f"fm_schwarz2005_tal_po_50_{tissue}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{fig_id}_tal_TAL"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_50",
                    xid="time",
                    yid="[Cve_tal]" if fig_id == "Fig1" else "Aurine_tal",
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
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures: list[Figure] = []

        for fig_id in ["Fig1", "Tab1a"]:
            if fig_id == "Fig1":
                ylabel = self.label_tal
                max_value = 25
                yid = "[Cve_tal]"
                tissue = "serum"
            else:
                ylabel = self.label_tal_urine
                max_value = 50
                yid = "Aurine_tal"
                tissue = "urine"

            f = Figure(
                experiment=self,
                sid=self.to_sid(f"{fig_id}_PO_{tissue}"),
                num_rows=1,
                num_cols=1,
                name=self.__class__.__name__,
            )
            plots = f.create_plots(
                xaxis=Axis(self.label_time, unit="hour", max=max_value), legend=True
            )

            plots[0].set_yaxis(
                ylabel, unit="µM" if fig_id == "Fig1" else "µmole", scale="linear"
            )

            # simulation
            plots[0].add_data(
                task="task_tal_po_50",
                xid="time",
                yid=yid,
                label="Sim 50 [mg]",
                color="black",
            )

            plots[0].add_data(
                dataset=self.to_sid(f"{fig_id}_tal_TAL"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="50 [mg]",
                color="black",
                linestyle="--" if fig_id == "Fig1" else "",
            )

            figures.append(f)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(Schwarz2005, output_dir=Schwarz2005.__name__)
