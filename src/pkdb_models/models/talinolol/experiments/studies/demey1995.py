"""Simulation experiment of the study DeMey1995."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class DeMey1995(TalinololSimulationExperiment):
    """Simulation experiment of DeMey1995.

    12 healthy men (79 kg), 6-way crossover: talinolol 25, 50, 100 and 400 mg
    as one capsule with 100 ml water (simulated as an oral dose), fasting from
    12 h before to 7.5 h after the dose with tea and two dry biscuits 30 min
    before each ergometry. Plasma sampled at 1:00, 1:50, 3:15, 4:00, 4:50,
    7:20, 9:50 and 23:50 h; Fig4 is the median of the sum of the R- and
    S-enantiomers (no dispersion). The exposure increases more than
    proportional with the dose (Cmax/dose 1.36, 1.87, 2.17 and 2.44 ng/ml/mg),
    the only study of the dose range in the same subjects. The bicycle
    ergometry and the isoprenaline and epinephrine infusions (changes of the
    cardiac output and of the blood flows) are not modelled.
    """

    doses: ClassVar[list[int]] = [25, 50, 100, 400]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("intervention"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("median", 1 / self.Mr.tal)
                dsets[f"tal_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for dose in self.doses:
            simulations[f"tal_po_{dose}"] = Simulation(
                time_unit="min",
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(79, "kg"),
                    "PODOSE_tal": Q(dose, "mg"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dose in self.doses:
            mappings[f"fm_tal_po_{dose}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"tal_TAL_{dose}",
                    xid="time",
                    yid="median",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_tal_po_{dose}", xid="time", yid="[Cve_tal]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.CAPSULE,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    data=PKPDData.PK,
                    data_type=DataType.MEDIAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig4"
        fig = Figure(
            experiment=self,
            sid=f"{name}_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
        # data
        for k, dose in enumerate(self.doses):
            plots[0].add_data(
                dataset=f"tal_TAL_{dose}",
                xid="time",
                yid="median",
                count="count",
                label=f"{dose} [mg]",
                color=colors[k],
            )

        # simulation
        for k, dose in enumerate(self.doses):
            plots[0].add_data(
                task=f"task_tal_po_{dose}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim {dose} [mg]",
                color=colors[k],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(DeMey1995, output_dir=DeMey1995.__name__)
