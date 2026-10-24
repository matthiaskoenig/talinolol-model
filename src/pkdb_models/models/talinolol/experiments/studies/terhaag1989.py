"""Simulation experiment of the study Terhaag1989."""

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


class Terhaag1989(TalinololSimulationExperiment):
    """Simulation experiment of Terhaag1989.

    Six patients 7 to 10 days after a cholecystectomy with a T-tube drain of
    the bile (`Health.CHOLECYSTECTOMY`) received 30 mg talinolol intravenously
    (patient BÜ = S2 20 mg). The bile was collected from the T-tube, so the
    drained bile does not reach the gut: the enterohepatic circulation is
    switched off (`LI__f_EHC` 0), as the amount eliminated in the bile at
    infinity of the authors (Table 1) assumes. A T-tube collects only a part of
    the bile (recovery 61-86 % in the literature), so the measured biliary
    excretion is a lower bound.

    The bile excretion rate of the data is the bile concentration times the
    bile flow of the patient (Table 1, 26 to 114 ml/hr); the model has one bile
    flow (46 ml/hr, the median), so the bile concentration is shown but not
    fitted (it repeats the rates). The amounts eliminated in the bile at
    infinity are compared at 120 hr, the end of the simulation. Patient GL
    (S1) has a flat serum curve (30-47 ng/ml over 3 hr after 30 mg IV, not
    biexponential, the only one in the paper), his mappings are outliers.
    """

    yids: ClassVar[dict[str, str]] = {
        "serum": "[Cve_tal]",
        "bile": "LI__Cbile_tal",
        "bilerate": "LI__TALEX",
    }
    doses: ClassVar[list[int]] = [30, 20]
    #: the subjects, S1 (GL) is an outlier, S2 (BÜ) received 20 mg
    subjects: ClassVar[tuple[int, ...]] = (1, 2, 3, 4, 5, 6)

    @staticmethod
    def dose(k: int) -> int:
        """Get the dose [mg] of the subject S{k}."""
        return 20 if k == 2 else 30

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1", "Tab1a", "Tab1a_mean"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if fig_id == "Tab1a_mean":
                    dset.unit_conversion("mean", 1 / self.Mr.tal)
                else:
                    dset.unit_conversion("value", 1 / self.Mr.tal)
                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        for dose in self.doses:
            simulations[f"tal_iv_{dose}"] = Simulation(
                time_unit="min",
                end=121 * 60,  # the bile amounts at infinity at 120 hr
                preinit_changes={
                    **self.default_changes(),
                    "IVDOSE_tal": Q(dose, "mg"),
                    # T-tube drainage: the drained bile does not reach the gut
                    "LI__f_EHC": Q(0, "dimensionless"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        metadata = {
            tissue: PKPDMappingMetaData(
                tissue=tissue,
                route=Route.IV,
                application_form=ApplicationForm.SOLUTION,
                dosing=Dosing.SINGLE,
                health=Health.CHOLECYSTECTOMY,
                fasting=Fasting.FASTED,
            )
            for tissue in (Tissue.SERUM, Tissue.BILE)
        }

        for k in self.subjects:
            dose = self.dose(k)
            # the bile concentration is not mapped: it is the bile rate over
            # the bile flow of the patient, the model has one bile flow
            for data in ("serum", "bilerate"):
                mappings[f"fm_tal_iv_{dose}_{data}_S{k}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig1_{data}_S{k}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_iv_{dose}",
                        xid="time",
                        yid=self.yids[data],
                    ),
                    metadata=metadata[Tissue.SERUM if data == "serum" else Tissue.BILE],
                )
            mappings[f"fm_tal_iv_{dose}_bile_amount_S{k}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab1a_bile_S{k}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_tal_iv_{dose}",
                    xid="time",
                    yid="LI__Abile_tal",
                ),
                metadata=metadata[Tissue.BILE],
            )

        # the mean of the five patients with 30 mg
        mappings["fm_tal_iv_30_bile_amount_mean"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="Tab1a_bile_mean",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_iv_30", xid="time", yid="LI__Abile_tal"
            ),
            metadata=metadata[Tissue.BILE],
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self.figure_timecourse("serum"),
            self.figure_timecourse("bile"),
            self.figure_timecourse("bilerate"),
            self.figure_amount_bile(),
        )

    @staticmethod
    def color(k: int) -> str:
        """Get the color of the subject S{k}: 20 mg, 30 mg or the outlier."""
        if k == 1:
            return "darkgrey"
        return "tab:blue" if k == 2 else "black"

    def label(self, k: int) -> str | None:
        """Get the legend label of the subject S{k}, once per group."""
        if k == 1:
            return "30 [mg] GL (outlier)"
        if k == 2:
            return "20 [mg]"
        return "30 [mg]" if k == 3 else None

    def figure_timecourse(self, data: str) -> Figure:
        """Serum concentration, bile concentration or bile excretion rate."""
        sid, ylabel, unit = {
            "serum": ("Fig1_IV_serum", self.label_tal, "µM"),
            "bile": ("Fig1_IV_bile", self.label_tal_bile, "mM"),
            "bilerate": ("Fig1_IV_bilerate", self.label_tal_bile_rate, "µmole/hr"),
        }[data]
        f = Figure(
            experiment=self,
            sid=sid,
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(
            xaxis=Axis(self.label_time, unit="hour", min=-0.5, max=7.5),
            legend=True,
        )
        plots[0].set_yaxis(ylabel, unit=unit, scale="linear")

        # simulation
        for dose in self.doses:
            plots[0].add_data(
                task=f"task_tal_iv_{dose}",
                xid="time",
                yid=self.yids[data],
                label=f"Sim {dose} [mg]",
                color="tab:blue" if dose == 20 else "black",
            )

        # data
        for k in self.subjects:
            plots[0].add_data(
                dataset=f"Fig1_{data}_S{k}",
                xid="time",
                yid="value",
                count="count",
                label=self.label(k),
                color=self.color(k),
            )

        return f

    def figure_amount_bile(self) -> Figure:
        """Amount of talinolol eliminated in the bile until infinity."""
        f = Figure(
            experiment=self,
            sid="Tab1a_IV_bile",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal_bile, unit="µmole", scale="linear")
        # simulation
        for dose in self.doses:
            plots[0].add_data(
                task=f"task_tal_iv_{dose}",
                xid="time",
                yid="LI__Abile_tal",
                label=f"Sim {dose} [mg]",
                color="tab:blue" if dose == 20 else "black",
            )

        # data
        for k in self.subjects:
            plots[0].add_data(
                dataset=f"Tab1a_bile_S{k}",
                xid="time",
                yid="value",
                count="count",
                label=self.label(k),
                color=self.color(k),
                marker="o",
                linestyle="",
            )
        plots[0].add_data(
            dataset="Tab1a_bile_mean",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="30 [mg] mean",
            color="tab:orange",
            marker="s",
            linestyle="",
        )

        return f


if __name__ == "__main__":
    MODEL.run_experiments(Terhaag1989, output_dir=Terhaag1989.__name__)
