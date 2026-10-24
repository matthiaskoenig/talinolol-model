"""Simulation experiment of the study Gramatte1996."""

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


class Gramatte1996(TalinololSimulationExperiment):
    """Simulation experiment of Gramatte1996.

    6 healthy men (65-90 kg), triple-lumen steady state perfusion of the small
    intestine: racemic talinolol 62.5 µg/ml in isotonic saline perfused at 10
    ml/min for 160 min (100 mg), on day 1 proximal (perfusion port 65-85 cm
    from the teeth, after an overnight fast) and on day 2 distal (135-230 cm,
    the serum corrected for the residual of day 1 by the authors). The test
    segment of 30 cm begins 15 cm below the perfusion port at the proximal
    aspiration port. Fig3 shows the serum of 4 subjects (individual data).

    The site of the perfusion is the segment of the model at the port of the
    subject (Table I; the pylorus about 55-60 cm from the teeth, the duodenum
    30 cm, jejunum_1 and jejunum_2 105 cm each): all proximal ports are in the
    duodenum, the distal ports of S1 (135 cm) and S5 (160 cm) in jejunum_1 and
    of S4 (205 cm) and S6 (230 cm) in jejunum_2.

    From 70 min, 1.5 ml/min are aspirated from the proximal port and from 85
    min from the distal port (6 x 15 min, the distal port staggered by 15 min):
    the talinolol which enters the intestine of the model is the perfusion
    minus the aspiration at the concentration of the perfusate (84.5 of 100
    mg). In S6 no fluid could be aspirated (technical difficulties), the full
    dose enters the intestine. The fluid flow of 10 ml/min, which shortens the
    residence time in the perfused segments, is not modelled.
    """

    individuals: ClassVar[list[str]] = ["S1", "S4", "S5", "S6"]
    locations: ClassVar[list[str]] = ["proximal", "distal"]
    #: the segment of the perfusion port by subject and location
    sites: ClassVar[dict[str, dict[str, str]]] = {
        "S1": {"proximal": "duodenum", "distal": "jejunum_1"},
        "S4": {"proximal": "duodenum", "distal": "jejunum_2"},
        "S5": {"proximal": "duodenum", "distal": "jejunum_1"},
        "S6": {"proximal": "duodenum", "distal": "jejunum_2"},
    }
    #: the position of the perfusion port [cm from the teeth] (Table I)
    ports: ClassVar[dict[str, dict[str, int]]] = {
        "S1": {"proximal": 70, "distal": 135},
        "S4": {"proximal": 75, "distal": 205},
        "S5": {"proximal": 85, "distal": 160},
        "S6": {"proximal": 65, "distal": 230},
    }
    #: the subjects without the aspiration of intestinal fluid
    no_aspiration: ClassVar[set[str]] = {"S6"}

    #: perfusion 62.5 µg/ml at 10 ml/min [mg/min]
    perfusion_rate: ClassVar[float] = 0.0625 * 10
    #: aspiration 1.5 ml/min at 62.5 µg/ml from one port [mg/min]
    aspiration_rate: ClassVar[float] = 0.0625 * 1.5

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig3")
        for label, df_label in df.groupby("label"):
            label = str(label)
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("value", 1 / self.Mr.tal)
            dsets[f"tal_{label.replace('Fig3_', '')}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for individual in self.individuals:
            for location in self.locations:
                ri = f"GU__Ri_tal_{self.sites[individual][location]}"
                if individual in self.no_aspiration:
                    changes = []
                else:
                    # aspiration from the proximal port (70 min) and the
                    # distal port (85 min)
                    changes = [
                        Change(
                            70,
                            {
                                ri: Q(
                                    self.perfusion_rate - self.aspiration_rate,
                                    "mg/min",
                                )
                            },
                        ),
                        Change(
                            85,
                            {
                                ri: Q(
                                    self.perfusion_rate - 2 * self.aspiration_rate,
                                    "mg/min",
                                )
                            },
                        ),
                    ]
                simulations[f"tal_perfusion_{location}_{individual}"] = Simulation(
                    time_unit="min",
                    end=160 + 9 * 60,
                    preinit_changes={
                        **self.default_changes(),
                        ri: Q(self.perfusion_rate, "mg/min"),
                    },
                    changes=[*changes, Change(160, {ri: Q(0, "mg/min")})],
                )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for individual in self.individuals:
            for location in self.locations:
                mappings[f"fm_tal_{location}_TAL_{individual}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"tal_{location}_TAL_{individual}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_perfusion_{location}_{individual}",
                        xid="time",
                        yid="[Cve_tal]",
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.SERUM,
                        route=Route.INTESTINAL,
                        application_form=ApplicationForm.SOLUTION,
                        dosing=Dosing.CONSTANT_INFUSION,
                        health=Health.HEALTHY,
                        # day 1 after an overnight fast, day 2 not reported
                        fasting=Fasting.FASTED
                        if location == "proximal"
                        else Fasting.NR,
                        data=PKPDData.PK,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig3_IVDUO_serum",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)
        for k, individual in enumerate(self.individuals):
            plots[k].set_title(individual)
            plots[k].set_yaxis(self.label_tal, unit="µM", scale="linear")
            for location in self.locations:
                site = self.sites[individual][location]
                port = self.ports[individual][location]
                color = "black" if location == "proximal" else self.sites_color[site]
                plots[k].add_data(
                    task=f"task_tal_perfusion_{location}_{individual}",
                    xid="time",
                    yid="[Cve_tal]",
                    label=f"Sim {self.sites_label[site]}",
                    color=color,
                )
                plots[k].add_data(
                    dataset=f"tal_{location}_TAL_{individual}",
                    xid="time",
                    yid="value",
                    label=f"{port} cm ({location})",
                    color=color,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Gramatte1996, output_dir=Gramatte1996.__name__)
