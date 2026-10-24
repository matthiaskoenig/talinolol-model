"""Simulation experiment of the study Fan2009a."""

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

#: the activity of the intestinal P-gp after 14 days of Schisandra chinensis
#: extract (300 mg twice daily): its lignans inhibit P-gp, the inhibition in
#: vivo is not known; 0.49 was chosen to reproduce the observed ratio of the
#: AUC (1.52, 1.16-1.98, Cmax 1.51) with the start values of the model before
#: the fit; with the adopted fit oral 100 mg gives an AUC ratio of 1.33 (Cmax
#: 1.27); not fitted, the arm is validation data
F_PGP_SCHISANDRA: float = 0.49

#: the activity of the intestinal P-gp after 14 days of Ginkgo biloba extract
#: (120 mg three times daily, Fan2009a and Fan2009b, the same batch): its
#: flavonoids inhibit P-gp, the inhibition in vivo is not known; 0.72 was
#: chosen to reproduce the mean of the observed ratios of the AUC (1.25,
#: 1.10-1.42, Fan2009a; 1.22, 1.08-1.37, Fan2009b) with the start values of the
#: model before the fit; with the adopted fit oral 100 mg gives an AUC ratio of
#: 1.16; not fitted, the arms are validation data
F_PGP_GINKGO: float = 0.72


class Arm(NamedTuple):
    """An arm of the study."""

    intervention: str  # intervention of the data
    f_pgp: float  # activity of the intestinal P-gp
    coadministration: Coadministration
    name: str
    color: str


class Fan2009a(TalinololSimulationExperiment):
    """Simulation experiment of Fan2009a.

    12 healthy Chinese men (62 kg), open crossover: 100 mg talinolol (tablet)
    alone, after 14 days of Schisandra chinensis extract (SchE, 300 mg twice
    daily) and after 14 days of Ginkgo biloba extract (GBE, 120 mg three times
    daily), talinolol 1 h after the last dose of the extract. Fasting is not
    reported, meals at 5 and 10 h. The bars of Fig1 are SDs although the
    caption says SE: their size is the one of the SD from the 95% CI of Cmax of
    Tab1 (gSD 1.48, SD about 105 ng/ml at the peak, SE about 30).
    """

    arms: ClassVar[dict[str, Arm]] = {
        "po_100": Arm(
            "TAL",
            1.0,
            Coadministration.NONE,
            "control",
            "black",
        ),
        "po_100_sche": Arm(
            "TAL, SCHE",
            F_PGP_SCHISANDRA,
            Coadministration.COMEDICATION,
            "Schisandra chinensis (P-gp ↓)",
            "#e34a33",
        ),
        "po_100_gbe": Arm(
            "TAL, GBE",
            F_PGP_GINKGO,
            Coadministration.COMEDICATION,
            "Ginkgo biloba (P-gp ↓)",
            "#2ca25f",
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
                    "BW": Q(62, "kg"),
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
                    fasting=Fasting.NR,
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

        for key, arm in self.arms.items():
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
    MODEL.run_experiments(Fan2009a, output_dir=Fan2009a.__name__)
