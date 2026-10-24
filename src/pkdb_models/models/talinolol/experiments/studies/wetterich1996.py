"""Simulation experiment of the study Wetterich1996."""

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Wetterich1996(TalinololSimulationExperiment):
    """Simulation experiment of Wetterich1996.

    The patients are after a cholecystectomy, the bile is collected by a T-drain
    between the days 5 and 8 after the surgery (`Health.CHOLECYSTECTOMY`); 3
    patients received 30 mg racemic talinolol intravenously as a 30 min short
    infusion, 3 patients 100 mg orally (tablet), after an overnight fast.

    The renal function of the patients is not measured (a GFR of 70-80 ml/min is
    calculated for their age, p. 517), their renal clearance (153-163 ml/min) is
    the one of the model with the healthy GFR, so `KI__f_renal_function` is not
    changed.
    """

    yids: ClassVar[dict[str, str]] = {
        "urine": "Aurine_tal",
        "bile": "LI__Abile_tal",
    }

    #: [hr] end of the simulations: the amounts of Tab1c are extrapolated to
    #: infinity, the excretion of the model is complete after 10 days
    end_hr: ClassVar[float] = 240.0

    #: [hr] the times of Fig1 are after the end of the 30 min infusion ("every
    #: 10 min in the first hour after i.v.-administration", the curve falls from
    #: the first sample on)
    infusion_hr: ClassVar[float] = 0.5

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}

        # concentration in plasma of the enantiomers, the racemate is their sum
        df = self.load_dataframe("Fig1")
        df["time"] = df["time"] + self.infusion_hr
        df_r = df[df.label == "R-talinolol"].reset_index(drop=True)
        df_s = df[df.label == "S-talinolol"].reset_index(drop=True)
        if not (df_r.time.to_numpy() == df_s.time.to_numpy()).all():
            msg = "The times of R- and S-talinolol in Fig1 differ."
            raise ValueError(msg)
        # the stored sum has the SD of a product (mean * sqrt(CV_R^2 + CV_S^2)),
        # the enantiomers are measured in the same subjects (fully correlated),
        # the SD of their sum is SD_R + SD_S
        df_sum = df_r.copy()
        df_sum["mean"] = df_r["mean"] + df_s["mean"]
        df_sum["sd"] = df_r["sd"] + df_s["sd"]
        df_sum["cv"] = df_sum["sd"] / df_sum["mean"]
        df_sum["label"] = "talinolol"
        df_sum["substance"] = "talinolol"
        for label, df_label in [
            ("R-talinolol", df_r),
            ("S-talinolol", df_s),
            ("talinolol", df_sum),
        ]:
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.tal)
            dsets[self.to_sid(f"Fig1_{label}")] = dset

        # amounts in urine and bile (Tab1c): Ae0-inf, extrapolated with the
        # terminal half-life (p. 516), not the amounts at the end of the
        # collection (72 hr urine, 24 hr bile); compared at the end of the
        # simulation
        df = self.load_dataframe("Tab1c")
        df.loc[df["time"] > 0, "time"] = self.end_hr
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.tal)
            dsets[self.to_sid(f"Tab1c_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}

        # Assumption: the T-drain collects the complete bile, nothing is
        # reabsorbed (the paper computes the biliary excretion with the full
        # bile flow of the literature); a T-drain leaves part of the bile to the
        # duodenum, the effect on the plasma and urine is small.
        no_ehc = {"LI__f_EHC": Q(0, "dimensionless")}

        # intravenous: 30 mg as a 30 min short infusion
        simulations["tal_iv_30"] = Simulation(
            time_unit="min",
            end=self.end_hr * 60,
            preinit_changes={
                **self.default_changes(),
                **no_ehc,
                "Ri_tal": Q(30, "mg") / Q(30, "min"),
            },
            changes=[Change(30, {"Ri_tal": Q(0, "mg/min")})],
        )

        # oral
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=self.end_hr * 60,
            preinit_changes={
                **self.default_changes(),
                **no_ehc,
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        mappings["fm_wetterich1996_tal_iv_30_plasma"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="Fig1_talinolol",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_iv_30", xid="time", yid="[Cve_tal]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.IV,
                application_form=ApplicationForm.SOLUTION,
                dosing=Dosing.SINGLE,
                health=Health.CHOLECYSTECTOMY,
                fasting=Fasting.FASTED,
            ),
        )

        for tissue, yid in self.yids.items():
            mappings[self.to_sid(f"fm_wetterich1996_tal_iv_30_{tissue}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1c_TAL_IV_{tissue}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_tal_iv_30", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue),
                    route=Route.IV,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.CHOLECYSTECTOMY,
                    fasting=Fasting.FASTED,
                ),
            )
            mappings[self.to_sid(f"fm_wetterich1996_tal_po_100_{tissue}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1c_TAL_PO_{tissue}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_tal_po_100", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue),
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.CHOLECYSTECTOMY,
                    fasting=Fasting.FASTED,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_plasma(),
            **self.figure_amount(),
        }

    def figure_plasma(self) -> dict[str, Figure]:
        """Concentration in plasma after the intravenous infusion (Fig1)."""
        f = Figure(
            experiment=self,
            sid="Fig1_IV_plasma",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(
            xaxis=Axis(self.label_time, unit="hour", min=-1, max=38), legend=True
        )
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_tal_iv_30",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 30 [mg]",
            color="black",
        )
        # data
        plots[0].add_data(
            dataset="Fig1_talinolol",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="30 [mg]",
            color="black",
        )

        return self.figures_by_sid(f)

    def figure_amount(self) -> dict[str, Figure]:
        """Amount in urine and bile after the oral and intravenous dose (Tab1c).

        The data are the amounts extrapolated to infinity, at the end.
        """
        figures: dict[str, Figure] = {}

        for intervention in ["TAL_PO", "TAL_IV"]:
            task_id = (
                "task_tal_po_100" if intervention == "TAL_PO" else "task_tal_iv_30"
            )

            for tissue, yid in self.yids.items():
                f = Figure(
                    experiment=self,
                    sid=self.to_sid(f"Tab1c_{intervention}_{tissue}"),
                    num_rows=1,
                    num_cols=1,
                    name=self.__class__.__name__,
                )
                plots = f.create_plots(
                    xaxis=Axis(self.label_time, unit="hour"), legend=True
                )
                plots[0].set_yaxis(
                    self.label_tal_urine if tissue == "urine" else self.label_tal_bile,
                    unit="µmole",
                    scale="linear",
                )

                # simulation
                plots[0].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid=yid,
                    label="Sim 30 [mg]" if intervention == "TAL_IV" else "Sim 100 [mg]",
                    color="black",
                )
                # data
                plots[0].add_data(
                    dataset=self.to_sid(f"Tab1c_{intervention}_{tissue}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="30 [mg]" if intervention == "TAL_IV" else "100 [mg]",
                    color="black",
                    linestyle="",
                )

                figures[self.to_sid(f"Tab1c_{intervention}_{tissue}_amount")] = f

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Wetterich1996, output_dir=Wetterich1996.__name__)
