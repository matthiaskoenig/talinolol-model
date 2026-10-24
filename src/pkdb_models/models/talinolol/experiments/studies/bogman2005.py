"""Simulation experiment of the study Bogman2005."""

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)

#: the activity of the intestinal P-gp with 0.04% TPGS (D-alpha-tocopheryl
#: polyethylene glycol 1000 succinate) in the perfusate: TPGS inhibits P-gp
#: (Caco-2, Bogman2005 Tab1: the basolateral to apical permeability of talinolol
#: decreases, the apical to basolateral one increases), its inhibition in vivo
#: is not known; 0.59 was chosen to reproduce the observed ratio of the AUC
#: (1.39, 1.10-1.75) with the start values of the model before the fit; with
#: the adopted fit the duodenal infusion of 50 mg gives an AUC ratio of 1.28
#: and a Cmax ratio of 1.24 (2.00 observed); not fitted, the arm is validation
#: data
F_PGP_TPGS: float = 0.59


class Arm(NamedTuple):
    """An arm of the study."""

    label: str  # label of the data
    f_pgp: float  # activity of the intestinal P-gp
    coadministration: Coadministration
    name: str
    color: str


class Bogman2005(TalinololSimulationExperiment):
    """Simulation experiment of Bogman2005.

    9 healthy men (73 kg), 3-way crossover after an overnight fast: 50 mg
    talinolol in a buffered solution (pH 6.0) perfused for 25 min at 5 ml/min
    through a tube with its tip in the duodenum (fluoroscopy), alone, with 0.04%
    TPGS or with 0.8% Poloxamer 188; liquid meal at 4 h. Fig1 is mean and SEM.

    TPGS inhibits P-gp (AUC ratio 1.39, Cmax ratio 2.00), see `F_PGP_TPGS`.
    Poloxamer 188 does not modulate P-gp (Caco-2 basolateral to apical
    permeability unchanged) and does not change the pharmacokinetics (AUC ratio
    0.91, 0.73-1.15), its arm is simulated with the factor of no effect.
    """

    arms: ClassVar[dict[str, Arm]] = {
        "ivduo_50": Arm(
            "Fig1_TAL",
            1.0,
            Coadministration.NONE,
            "talinolol",
            "black",
        ),
        "ivduo_50_tpgs": Arm(
            "Fig1_TAL_TPGS",
            F_PGP_TPGS,
            Coadministration.COMEDICATION,
            "talinolol + TPGS (P-gp ↓)",
            TalinololSimulationExperiment.colors_pg_function["P-gp ↓"],
        ),
        "ivduo_50_pol": Arm(
            "Fig1_TAL_POL",
            TalinololSimulationExperiment.pgp_interaction["poloxamer"],
            Coadministration.COMEDICATION,
            "talinolol + Poloxamer 188",
            "tab:gray",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.tal)
            dsets[self.to_sid(f"tal_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for key, arm in self.arms.items():
            simulations[f"tal_{key}"] = Simulation(
                time_unit="min",
                end=25 + 50 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(73, "kg"),
                    "GU__Ri_tal_duodenum": Q(50, "mg") / Q(25, "min"),
                    # P-gp activity of the arm
                    "GU__f_pgp": Q(arm.f_pgp, "dimensionless"),
                },
                changes=[Change(25, {"GU__Ri_tal_duodenum": Q(0, "mg/min")})],
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
                    dataset=self.to_sid(f"tal_{arm.label}"),
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
                    route=Route.INTESTINAL,
                    application_form=ApplicationForm.BUFFERED_SOLUTION,
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
        return {
            **self.figure_tal(),
            **self.figure_pgp_function(),
        }

    def figure_tal(self) -> dict[str, Figure]:
        """Figure of the talinolol plasma concentration of the control."""
        fig = Figure(
            experiment=self,
            sid="Fig1_IVDUO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")
        arm = self.arms["ivduo_50"]
        plots[0].add_data(
            task="task_tal_ivduo_50",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 50 [mg] (duodenum)",
            color=arm.color,
        )
        plots[0].add_data(
            dataset=self.to_sid(f"tal_{arm.label}"),
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 [mg] (duodenum)",
            color=arm.color,
        )

        return self.figures_by_sid(fig)

    def figure_pgp_function(self) -> dict[str, Figure]:
        """Figure of the talinolol plasma concentration of the three arms."""
        fig = Figure(
            experiment=self,
            sid="Fig1_IVDUO_plasma_pgp_function",
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
                label=f"Sim {arm.name}",
                color=arm.color,
            )
            plots[0].add_data(
                dataset=self.to_sid(f"tal_{arm.label}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=arm.name,
                color=arm.color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Bogman2005, output_dir=Bogman2005.__name__)
