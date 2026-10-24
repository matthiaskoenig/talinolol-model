"""Simulation experiment of the study Tubic2006a."""

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


class Tubic2006a(TalinololSimulationExperiment):
    """Simulation experiment of Tubic2006a.

    Seven healthy volunteers received talinolol orally after an overnight fast
    (standard meal 4 hr after the dose), crossover: one immediate release
    tablet of 100 mg (IR), one controlled release matrix tablet of 100 mg and
    two of them (200 mg, CR). Plasma until 48 hr (Fig 3, mean and SEM), the
    cumulative urine of one representative volunteer (Fig 4) and the urine
    until infinity (Table 1, Ae_inf: Ae0-48 and an extrapolation), compared at
    120 hr, the end of the simulations.

    The controlled release tablet is simulated with the first order release of
    its dissolution in vitro (Fig 2, pH 4.5 and 6.8: 60-73 % in 4 hr, 80-89 %
    in 6 hr, `Ka_dis_tal` 0.3 1/hr) into the duodenum. The model has no release
    along the gut, where the tablet passes the absorption window of talinolol,
    so it overpredicts the exposure of CR (relative F 54 % and 38 %): the CR
    arms are a limitation of the model, not fitted.
    """

    #: the first order release of the controlled release tablet (Fig 2)
    ka_release_cr: ClassVar[float] = 0.3

    doses: ClassVar[dict[int, str]] = {
        100: "#756bb1",
        200: "#bcbddc",
    }
    yid_observable: ClassVar[dict[str, str]] = {
        "Fig3": "[Cve_tal]",
        "Fig4": "Aurine_tal",
        "Tab1a": "Aurine_tal",
    }
    yid_data: ClassVar[dict[str, str]] = {
        "Fig3": "mean",
        "Fig4": "value",
        "Tab1a": "mean",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig3", "Fig4", "Tab1a"]:
            parameter = "value" if fig_id == "Fig4" else "mean"
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion(parameter, 1 / self.Mr.tal)
                dsets[f"{fig_id}_tal_{intervention}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        for dose in self.doses:
            simulations[f"tal_po_CR_{dose}"] = Simulation(
                time_unit="min",
                end=121 * 60,  # Ae_inf at 120 hr
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(dose, "mg"),
                    "Ka_dis_tal": Q(self.ka_release_cr, "1/hr"),
                },
            )
        simulations["tal_po_IR_100"] = Simulation(
            time_unit="min",
            end=121 * 60,  # Ae_inf at 120 hr
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        for fig_id in ["Fig3", "Fig4", "Tab1a"]:
            if fig_id == "Fig3":
                tissue = "plasma"
            elif fig_id == "Tab1a":
                tissue = "urine_mean"
            else:
                tissue = "urine"

            mappings[f"fm_tal_po_TAL_IR_100_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{fig_id}_tal_TAL_IR_100",
                    xid="time",
                    yid=self.yid_data[fig_id],
                    yid_sd=None if fig_id == "Fig4" else "mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_IR_100",
                    xid="time",
                    yid=self.yid_observable[fig_id],
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue.removesuffix("_mean")),
                    route=Route.PO,
                    application_form=ApplicationForm.IMMEDIATE_RELEASE,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

            for dose in self.doses:
                mappings[f"fm_tal_po_TAL_CR_{dose}_{tissue}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{fig_id}_tal_TAL_CR_{dose}",
                        xid="time",
                        yid=self.yid_data[fig_id],
                        yid_sd=None if fig_id == "Fig4" else "mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_po_CR_{dose}",
                        xid="time",
                        yid=self.yid_observable[fig_id],
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue(tissue.removesuffix("_mean")),
                        route=Route.PO,
                        application_form=ApplicationForm.CONTROLLED_RELEASE,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_IR(),
            **self.figures_all(),
        }

    def figure_IR(self) -> dict[str, Figure]:
        """Concentration in plasma and amount in urine after the IR tablet."""
        f_plasma = Figure(
            experiment=self,
            sid="Fig3_PO_plasma_IR",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots_plasma = f_plasma.create_plots(
            xaxis=Axis(self.label_time, unit="hour", min=-1, max=50), legend=True
        )
        plots_plasma[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        plots_plasma[0].add_data(
            dataset="Fig3_tal_TAL_IR_100",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 IR [mg]",
            color="black",
        )

        # plot sim
        plots_plasma[0].add_data(
            task="task_tal_po_IR_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 IR [mg]",
            color="black",
        )

        f_urine = Figure(
            experiment=self,
            sid="Fig4_PO_urine_IR",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots_urine = f_urine.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_urine[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        plots_urine[0].add_data(
            task="task_tal_po_IR_100",
            xid="time",
            yid="Aurine_tal",
            label="Sim 100 IR [mg]",
            color="black",
        )

        plots_urine[0].add_data(
            dataset="Fig4_tal_TAL_IR_100",
            xid="time",
            yid="value",
            yid_sd=None,
            count="count",
            label="100 IR [mg] one subject",
            color="black",
        )
        plots_urine[0].add_data(
            dataset="Tab1a_tal_TAL_IR_100",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 IR [mg] total amount",
            color="black",
            linestyle="",
        )

        return self.figures_by_sid(f_plasma, f_urine)

    def figures_all(self) -> dict[str, Figure]:
        """Concentration in plasma and amount in urine after all tablets."""
        fig_plasma = Figure(
            experiment=self,
            sid="Fig3_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots_plasma = fig_plasma.create_plots(
            xaxis=Axis(self.label_time, unit="hour", min=-1, max=50), legend=True
        )
        plots_plasma[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # plot sim
        for dose, color in self.doses.items():
            plots_plasma[0].add_data(
                task=f"task_tal_po_CR_{dose}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim {dose} CR [mg]",
                color=color,
            )

        plots_plasma[0].add_data(
            task="task_tal_po_IR_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 IR [mg]",
            color="black",
        )

        # plot data
        plots_plasma[0].add_data(
            dataset="Fig3_tal_TAL_IR_100",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 IR [mg]",
            color="black",
        )
        for dose, color in self.doses.items():
            plots_plasma[0].add_data(
                dataset=f"Fig3_tal_TAL_CR_{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} CR [mg]",
                color=color,
            )

        fig_urine = Figure(
            experiment=self,
            sid="Fig4_PO_urine",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots_urine = fig_urine.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_urine[0].set_yaxis(self.label_tal_urine, unit="µmole", scale="linear")

        # plot sim
        for dose, color in self.doses.items():
            plots_urine[0].add_data(
                task=f"task_tal_po_CR_{dose}",
                xid="time",
                yid="Aurine_tal",
                label=f"Sim {dose} CR [mg]",
                color=color,
            )
        plots_urine[0].add_data(
            task="task_tal_po_IR_100",
            xid="time",
            yid="Aurine_tal",
            label="Sim 100 IR [mg]",
            color="black",
        )

        # plot data
        plots_urine[0].add_data(
            dataset="Fig4_tal_TAL_IR_100",
            xid="time",
            yid="value",
            yid_sd=None,
            count="count",
            label="100 IR [mg] one subject",
            color="black",
        )
        plots_urine[0].add_data(
            dataset="Tab1a_tal_TAL_IR_100",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 IR [mg] total amount",
            linestyle="",
            color="black",
        )
        for dose, color in self.doses.items():
            plots_urine[0].add_data(
                dataset=f"Fig4_tal_TAL_CR_{dose}",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label=f"{dose} CR [mg] one subject",
                color=color,
            )
            plots_urine[0].add_data(
                dataset=f"Tab1a_tal_TAL_CR_{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} CR [mg] total amount",
                linestyle="",
                color=color,
            )

        return self.figures_by_sid(fig_plasma, fig_urine)


if __name__ == "__main__":
    MODEL.run_experiments(Tubic2006a, output_dir=Tubic2006a.__name__)
