"""Simulation experiment of the study Giessmann2004."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
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


class Giessmann2004(TalinololSimulationExperiment):
    """Simulation experiment of Giessmann2004.

    8 healthy volunteers (64-93 kg, 7 evaluated, creatinine clearance 94.7
    ml/min): 30 mg talinolol infused over 30 min (serum to 144 h and urine for 3
    days, not in the figures), then 100 mg talinolol tablets daily after an
    overnight fast from study day 11 for 19 days, the steady state profile on
    day 15 and no dose on day 16 (for the half-life). Simulated day 0 is study
    day 11: the troughs of Fig2 on days 1 to 4 are study days 12 to 15, the
    profile is on day 4. The urine is reset at every dose, the amount of the
    dosing interval of day 15 (Tab3a, CLR*AUC0-24, computed from Tab3) is
    compared with the urine of day 4 to 5. The amount after the infusion is
    CLR*AUC0-inf (Tab3), compared at 3 days (Ae(0-72 h) is about 94% of it with
    the half-life of 17.8 h). The arms with carbamazepine (induction of P-gp
    and of the renal excretion, CLR +53%) are not simulated.
    """

    #: the days of the oral doses after the first one: daily to study day 15
    #: (simulated day 4), no dose on study day 16 (simulated day 5)
    dose_days: ClassVar[list[int]] = [1, 2, 3, 4]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Tab3a"]:
            df = self.load_dataframe(fig_id)
            # the urine of the dosing interval of study day 15 (simulated day 4)
            is_po_urine = df["label"] == "Tab3a_TAL_PO_urine"
            df.loc[is_po_urine, "time"] += 4
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # infusion of 30 mg over 30 min
        simulations["tal_iv_30"] = Simulation(
            time_unit="min",
            end=30 + 24 * 60 * 3,  # at least 3 days for urine
            preinit_changes={
                **self.default_changes(),
                "Ri_tal": Q(30, "mg") / Q(30, "min"),
            },
            changes=[Change(30, {"Ri_tal": Q(0, "mg/min")})],
        )

        # multiple dosing: 100 mg daily, no dose on day 5 (study day 16); the
        # urine is the amount of the dosing interval (reset at every dose)
        simulations["tal_po_100_multi"] = Simulation(
            time_unit="min",
            end=6 * 24 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
            changes=[
                self.add_doses(
                    [day * 24 * 60 for day in self.dose_days],
                    {"PODOSE_tal": Q(100, "mg")},
                ),
                Change(
                    [day * 24 * 60 for day in self.dose_days],
                    {"Aurine_tal": Q(0, "mmole")},
                ),
            ],
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dset_id in ["Fig2_TAL_PO", "Tab3a_TAL_PO_urine"]:
            tissue = "serum" if dset_id == "Fig2_TAL_PO" else "urine"
            mappings[self.to_sid(f"fm_tal_po_100_multi_{tissue}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"tal_{dset_id}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_100_multi",
                    xid="time",
                    yid="[Cve_tal]" if dset_id == "Fig2_TAL_PO" else "Aurine_tal",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM if dset_id == "Fig2_TAL_PO" else Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )

        mappings["fm_tal_iv_30_urine"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="tal_Tab3a_TAL_IV_urine",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_iv_30", xid="time", yid="Aurine_tal"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.URINE,
                route=Route.IV,
                application_form=ApplicationForm.SOLUTION,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.NR,
                data=PKPDData.PK,
                data_type=DataType.MEAN,
            ),
        )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        f_multi = Figure(
            experiment=self,
            sid="Fig2_multi",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_multi = f_multi.create_plots(
            xaxis=Axis(self.label_time, unit="day"), legend=True
        )
        plots_multi[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots_multi[0].add_data(
            task="task_tal_po_100_multi",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )

        plots_multi[0].add_data(
            dataset="tal_Fig2_TAL_PO",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg]",
            color="black",
        )

        f_urinepo = Figure(
            experiment=self,
            sid="Tab3a_TAL_PO_urine",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_urinepo = f_urinepo.create_plots(
            xaxis=Axis(self.label_time, unit="day"), legend=True
        )
        plots_urinepo[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        plots_urinepo[0].add_data(
            task="task_tal_po_100_multi",
            xid="time",
            yid="Aurine_tal",
            label="Sim 100 po multi [mg]",
            color="black",
        )
        plots_urinepo[0].add_data(
            dataset="tal_Tab3a_TAL_PO_urine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 po multi [mg]",
            color="black",
            linestyle="",
        )
        f_urineiv = Figure(
            experiment=self,
            sid="Tab3a_TAL_IV_urine",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_urineiv = f_urineiv.create_plots(
            xaxis=Axis(self.label_time, unit="day"), legend=True
        )
        plots_urineiv[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        plots_urineiv[0].add_data(
            task="task_tal_iv_30",
            xid="time",
            yid="Aurine_tal",
            label="Sim 30 iv [mg]",
            color="black",
        )
        plots_urineiv[0].add_data(
            dataset="tal_Tab3a_TAL_IV_urine",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="30 iv [mg]",
            color="black",
            linestyle="",
        )

        return {
            "Fig2_PO_MULTI_serum": f_multi,
            "Tab3a_PO_urine": f_urinepo,
            "Tab3a_IV_urine": f_urineiv,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Giessmann2004, output_dir=Giessmann2004.__name__)
