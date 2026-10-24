"""Simulation experiment of the study Fan2009b."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    DataType,
    Dosing,
    Fasting,
    Health,
    PKPDData,
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
from pkdb_models.models.talinolol.experiments.studies.fan2009a import F_PGP_GINKGO


class Arm(NamedTuple):
    """An arm of the study."""

    intervention: str  # intervention of the data
    f_pgp: float  # activity of the intestinal P-gp
    coadministration: Coadministration
    name: str
    color: str


class Fan2009b(TalinololSimulationExperiment):
    """Simulation experiment of Fan2009b.

    10 healthy Chinese men (48-77 kg, BMI 18-23; simulated with the middle of
    the range, 62.5 kg), sequential after a 10 h fast: 100 mg talinolol
    (tablet) alone (day 1), with a single dose of 120 mg Ginkgo biloba extract
    (GBE acute, day 8) and with the 44th dose of GBE 120 mg three times daily
    (GBE chronic, day 23). A single dose of GBE does not change the
    pharmacokinetics (AUC0-inf 2499 against 2739 ng*h/ml, Cmax ratio 0.88), the
    chronic GBE increases the AUC (1.22, 1.08-1.37) and Cmax (1.36), see
    `F_PGP_GINKGO` of Fan2009a (the same institute, assay and batch of GBE).
    The bars of Fig1 are SDs although the caption says SE (their size is the
    one of the SD from the 95% CI of Cmax of Tab1, gSD 1.56).
    """

    arms: ClassVar[dict[str, Arm]] = {
        "po_100": Arm(
            "TAL",
            1.0,
            Coadministration.NONE,
            "alone",
            "black",
        ),
        "po_100_gbe_acute": Arm(
            "GBEAC, TAL",
            1.0,
            Coadministration.COMEDICATION,
            "Ginkgo biloba acute",
            "#74c476",
        ),
        "po_100_gbe_chronic": Arm(
            "GBECR, TAL",
            F_PGP_GINKGO,
            Coadministration.COMEDICATION,
            "Ginkgo biloba chronic (P-gp ↓)",
            "#006d2c",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        keys = {arm.intervention: key for key, arm in self.arms.items()}
        dsets = {}
        df = self.load_dataframe("Fig1")
        for intervention, df_intervention in df.groupby("intervention"):
            dset = DataSet.from_df(df_intervention, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.tal)
            dsets[f"tal_{keys[str(intervention)]}_plasma"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for key, arm in self.arms.items():
            simulations[f"tal_{key}"] = Simulation(
                time_unit="min",
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(62.5, "kg"),
                    "GU__f_pgp": Q(arm.f_pgp, "dimensionless"),
                    "PODOSE_tal": Q(100, "mg"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, arm in self.arms.items():
            mappings[f"fm_tal_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"tal_{key}_plasma",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_tal_{key}", xid="time", yid="[Cve_tal]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=arm.coadministration,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # the control last: the acute arm is the same simulation
        for key, arm in reversed(self.arms.items()):
            plots[0].add_data(
                task=f"task_tal_{key}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim 100 [mg] {arm.name}",
                color=arm.color,
            )
            plots[0].add_data(
                dataset=f"tal_{key}_plasma",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"100 [mg] {arm.name}",
                color=arm.color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Fan2009b, output_dir=Fan2009b.__name__)
