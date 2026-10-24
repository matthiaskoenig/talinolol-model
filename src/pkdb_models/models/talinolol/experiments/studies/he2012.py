"""Simulation experiment of the study He2012."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Dosing,
    Fasting,
    Genotype,
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


class He2012(TalinololSimulationExperiment):
    """Simulation experiment of He2012.

    18 healthy Chinese men selected by the ABCB1 C3435T genotype (6 CC, 6 CT,
    6 TT), a single oral dose of 100 mg talinolol (Cordanum tablet) after an
    overnight fast (no food until 2 hr), after 14 days of placebo or of
    curcumin 1000 mg/day (crossover), plasma 0-48 hr (mean and SD).

    The placebo phase is given three times: by genotype (Fig1, fitted with the
    P-gp activity of the genotype, `activity_MDR1_genotype`), as the mean of
    all 18 subjects (Fig2, the mean of the three genotype curves, an aggregate)
    and again by genotype next to the curcumin arm (Fig3, the curves of Fig1
    digitized a second time, drawn but not mapped). The mean of the mixed
    cohort is simulated with the activity of the wildtype.

    The curcumin arm (AUC0-inf ratio 1.81, CL/F 0.74) is not simulated: no in
    vivo factor of curcumin on the intestinal P-gp is known, and curcumin
    decreased the AUC of talinolol in Juan2007 (ratio 0.67).
    """

    #: the genotype of the groups
    genotypes: ClassVar[dict[str, Genotype]] = {
        "ABCB1_CC": Genotype.ABCB1_3435CC,
        "ABCB1_CT": Genotype.ABCB1_3435CT,
        "ABCB1_TT": Genotype.ABCB1_3435TT,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Fig3"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=49 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        for genotype, activity in self.activity_MDR1_genotype.items():
            simulations[f"tal_po_100_{genotype}"] = Simulation(
                time_unit="min",
                end=49 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(100, "mg"),
                    "GU__f_pgp": Q(activity, "dimensionless"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # the placebo phase by genotype, simulated with the P-gp activity of the
        # genotype, and the mean of all subjects
        tasks = {
            **{
                f"Fig1_TAL_{group}": (f"task_tal_po_100_{group}", genotype)
                for group, genotype in self.genotypes.items()
            },
            "Fig2_TAL": ("task_tal_po_100", Genotype.NR),
        }

        for dset, (task, genotype) in tasks.items():
            mappings[f"fm_tal_po_100_{dset}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid="[Cve_tal]"),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    genotype=genotype,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_all()

    def figures_all(self) -> dict[str, Figure]:
        """Figures 1 - 3 of the study, by ABCB1 genotype and with placebo."""
        # Figure 1: Talinolol after single dose intervention in CC, CT and TT genotypes of the ABCB1 gene
        fig_1 = Figure(
            experiment=self,
            sid="Fig1_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_fig1 = fig_1.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_fig1[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        for genotype in self.activity_MDR1_genotype:
            plots_fig1[0].add_data(
                task=f"task_tal_po_100_{genotype}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim 100 [mg] {genotype.replace('_', ' ')}",
                color=self.colors_MDR1_genotype[genotype],
            )

        for group in self.genotypes:
            plots_fig1[0].add_data(
                dataset=f"Fig1_TAL_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{group.replace('_', ' ')} 100 [mg]",
                color=self.colors_MDR1_genotype[group],
            )

        # Figure 2: Talinolol after single dose intervention with placebo
        fig_2 = Figure(
            experiment=self,
            sid="Fig2_PO_plasma",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_fig2 = fig_2.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_fig2[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots_fig2[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )
        plots_fig2[0].add_data(
            dataset="Fig2_TAL",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg]",
            color="black",
            linestyle="--",
        )

        # Figure 3 Talinolol after single dose intervention with placebo in CC, CT and TT subjects
        name = "Fig3"
        fig_3 = Figure(
            experiment=self,
            sid=f"{name}_PO_plasma",
            num_rows=3,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots_fig3 = fig_3.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots_fig3[0].set_yaxis(self.label_tal, unit="µM", scale="linear")
        plots_fig3[1].set_yaxis(self.label_tal, unit="µM", scale="linear")
        plots_fig3[2].set_yaxis(self.label_tal, unit="µM", scale="linear")

        for n, group in enumerate(self.genotypes):
            # simulation
            plots_fig3[n].add_data(
                task=f"task_tal_po_100_{group}",
                xid="time",
                yid="[Cve_tal]",
                label=f"Sim 100 [mg] {group.replace('_', ' ')}",
                color=self.colors_MDR1_genotype[group],
            )
            plots_fig3[n].add_data(
                dataset=f"Fig3_TAL_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{group.replace('_', ' ')} 100 [mg]",
                color=self.colors_MDR1_genotype[group],
                linestyle="--",
            )

        return self.figures_by_sid(fig_1, fig_2, fig_3)


if __name__ == "__main__":
    MODEL.run_experiments(He2012, output_dir=He2012.__name__)
