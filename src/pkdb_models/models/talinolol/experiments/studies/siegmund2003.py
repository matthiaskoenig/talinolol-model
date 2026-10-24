"""Simulation experiment of the study Siegmund2003."""

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


class Siegmund2003(TalinololSimulationExperiment):
    """Simulation experiment of Siegmund2003.

    36 healthy Caucasians (15 men), four tablets of talinolol (Cordanum) in a
    randomized changeover after an overnight fast: 100 mg film-coated (Test
    1), 200 mg film-coated (Test 2), 2 x 50 mg sugar-coated (Reference 1) and
    100 mg sugar-coated (Reference 2); serum 0-49 hr, median curves (Fig1).
    The tablets of 100 mg are bioequivalent (AUC ratios 0.96-1.06) in the
    same subjects: the film-coated tablet is the data of 100 mg, the
    sugar-coated tablets are aggregates of the same subjects. The 100 mg
    sugar-coated tablet absorbs later (0.5 hr: 14 vs 55-66 ng/ml).
    """

    #: intervention: label of the tablet
    interventions: ClassVar[dict[str, str]] = {
        "TAL_FLM_100": "100 mg film-coated",
        "TAL_FLM_200": "200 mg film-coated",
        "TAL_SUG2_100": "2 x 50 mg sugar-coated",
        "TAL_SUG1_100": "100 mg sugar-coated",
    }
    colors: ClassVar[dict[str, str]] = {
        "TAL_FLM_100": "black",
        "TAL_FLM_200": "tab:blue",
        "TAL_SUG2_100": "tab:orange",
        "TAL_SUG1_100": "tab:green",
    }
    doses: ClassVar[list[int]] = [100, 200]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("intervention"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("median", 1 / self.Mr.tal)
                dsets[f"tal_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        for dose in self.doses:
            simulations[f"tal_po_{dose}"] = Simulation(
                time_unit="min",
                end=49 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(dose, "mg"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for intervention in self.interventions:
            dose = intervention.split("_")[-1]
            mappings[f"fm_tal_po_{intervention}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"tal_{intervention}",
                    xid="time",
                    yid="median",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_tal_po_{dose}", xid="time", yid="[Cve_tal]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
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
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=f"{name}_PO_serum",
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        plots[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        for dose in self.doses:
            plots[0].add_data(
                task=f"task_tal_po_{dose}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim {dose} [mg]",
                color=self.colors[f"TAL_FLM_{dose}"],
            )

        # data
        for intervention, label in self.interventions.items():
            plots[0].add_data(
                dataset=f"tal_{intervention}",
                xid="time",
                yid="median",
                count="count",
                label=label,
                color=self.colors[intervention],
                linestyle="",
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Siegmund2003, output_dir=Siegmund2003.__name__)
