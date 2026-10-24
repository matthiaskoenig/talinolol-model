"""Simulation experiment of the study Zhang2005."""

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


class Zhang2005(TalinololSimulationExperiment):
    """Simulation experiment of Zhang2005.

    27 healthy Chinese men, 100 mg talinolol (tablet) after an overnight fast,
    in four groups of the ABCB1 haplotype G2677T/A and C3435T. The study finds
    no effect of the genotype on the pharmacokinetics (P > 0.05), so every
    group is compared with the simulation of the wildtype (P-gp activity of the
    model). The simulations with the P-gp activity of the genotypes of the
    model (`activity_MDR1_genotype`, from He2012) are drawn for comparison
    only.
    """

    #: genotype of the groups, the C3435T allele of a group is the genotype of
    #: `activity_MDR1_genotype`
    genotypes: ClassVar[dict[str, Genotype]] = {
        "GG_CC": Genotype.ABCB1_2677GG_3435CC,
        "TT_TT": Genotype.ABCB1_2677TT_3435TT,
        "GT_CT": Genotype.ABCB1_2677GT_3435CT,
        "AT_CT": Genotype.ABCB1_2677AT_3435CT,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for group, df_group in df.groupby("group"):
                dset = DataSet.from_df(df_group, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{group}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=61 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        for genotype, activity in self.activity_MDR1_genotype.items():
            simulations[self.to_sid(f"tal_po_100_{genotype}")] = Simulation(
                time_unit="min",
                end=61 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(100, "mg"),
                    "GU__f_pgp": Q(activity, "dimensionless"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for group, genotype in self.genotypes.items():
            # no error bars: the default CV of sbmlsim (Cmax CV 43-53 %)
            mappings[self.to_sid(f"fm_zhang2005_tal_po_100_{group}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"tal_{group}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_tal_po_100", xid="time", yid="[Cve_tal]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
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
        return {
            **self.figure_wildtype(),
            **self.figure_pg_activity(),
            **self.figure_all(),
        }

    def figure_wildtype(self) -> dict[str, Figure]:
        """Concentration in serum of the wildtype (ABCB1 2677GG/3435CC)."""
        name = "Fig1_wildtype"
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
        plots[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )

        plots[0].add_data(
            dataset=self.to_sid("tal_GG_CC"),
            xid="time",
            yid="mean",
            count="count",
            label="GG/CC 100 [mg]",
            color="black",
        )
        return self.figures_by_sid(fig)

    def figure_pg_activity(self) -> dict[str, Figure]:
        """Concentration in serum with the P-gp activity of the genotypes.

        The P-gp activity of the genotypes of the model, the data show no effect
        of the genotype.
        """
        name = "Fig1_pgactivity"
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
        for genotype in self.activity_MDR1_genotype:
            if genotype != "ABCB1_CT":
                plots[0].add_data(
                    task=self.to_sid(f"task_tal_po_100_{genotype}"),
                    xid="time",
                    yid="[Cve_tal]",
                    label=f"Sim 100 [mg] {genotype.replace('_', ' ')}",
                    color=self.colors_MDR1_genotype[genotype],
                )

        # data
        for group, genotype in [("GG_CC", "ABCB1_CC"), ("TT_TT", "ABCB1_TT")]:
            plots[0].add_data(
                dataset=self.to_sid(f"tal_{group}"),
                xid="time",
                yid="mean",
                count="count",
                label=f"{group.replace('_', '/')} 100 [mg]",
                color=self.colors_MDR1_genotype[genotype],
            )

        return self.figures_by_sid(fig)

    def figure_all(self) -> dict[str, Figure]:
        """Concentration in serum of all genotypes."""
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
        plots[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 [mg]",
            color="black",
        )

        for group in self.genotypes:
            plots[0].add_data(
                dataset=self.to_sid(f"tal_{group}"),
                xid="time",
                yid="mean",
                count="count",
                label=f"{group.replace('_', '/')} 100 [mg]",
            )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Zhang2005, output_dir=Zhang2005.__name__)
