"""Simulation experiment of the study Schwarz2007."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
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


class Arm(NamedTuple):
    """An arm of the study: with or without St John's wort."""

    #: suffix of the interventions of the data, the simulations and mappings
    suffix: str
    coadministration: Coadministration
    #: key of `pgp_interaction`
    pgp: str
    label: str
    color: str


class Schwarz2007(TalinololSimulationExperiment):
    """Simulation experiment of Schwarz2007.

    9 healthy men (ABCB1 C3435T 2 CC, 6 CT, 1 TT), 50 mg talinolol orally
    (tablet, Cordanum) after a fast of 10 hr and 30 mg talinolol intravenously
    (infusion over 30 min, Table 1 and Methods), each before and after St
    John's wort (Jarsin 300, 300 mg t.i.d. for 12 days); serum 0-24 hr and
    urine 0-48 hr. The error bars of the oral serum are standard errors, the
    copy of the data has the standard deviation `se * sqrt(9)`; the
    intravenous serum has no error bars.

    St John's wort induces the intestinal P-gp, `pgp_interaction`
    ("st_johns_wort"), the 1.6 fold duodenal MDR1 mRNA measured in these
    subjects (not fitted): observed oral AUC0-24 ratio 0.68, Cmax 0.79 and
    urinary recovery 0.56, intravenous AUC0-inf 0.93 at an unchanged
    clearance. The arms with St John's wort are validation data.
    """

    arms: ClassVar[tuple[Arm, ...]] = (
        Arm(
            suffix="",
            coadministration=Coadministration.NONE,
            pgp="none",
            label="",
            color=TalinololSimulationExperiment.colors_pg_function["P-gp normal"],
        ),
        Arm(
            suffix="_SJW",
            coadministration=Coadministration.ST_JOHNS_WORT,
            pgp="st_johns_wort",
            label=" St John's wort",
            color=TalinololSimulationExperiment.colors_pg_function["P-gp ↑"],
        ),
    )
    #: route: (dose [mg], label)
    routes: ClassVar[dict[str, tuple[int, str]]] = {
        "PO": (50, "po"),
        "IV": (30, "iv"),
    }
    #: data: (tissue, observable)
    tissues: ClassVar[dict[str, tuple[str, str]]] = {
        "Fig1AB": ("serum", "[Cve_tal]"),
        "Tab1a": ("urine", "Aurine_tal"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in self.tissues:
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                # "TAL_PO, SJW" -> "TAL_PO_SJW"
                intervention_id = str(intervention).replace(", ", "_")
                dsets[self.to_sid(f"{fig_id}_tal_{intervention_id}")] = dset

        return dsets

    def simulation_id(self, route: str, arm: Arm) -> str:
        """Get the id of the simulation of a route and an arm.

        Args:
            route: "PO" or "IV", a key of `routes`.
            arm: the arm.
        """
        dose, label = self.routes[route]
        return f"tal_{label}_{dose}{arm.suffix.lower()}"

    @staticmethod
    def has_sd(route: str, tissue: str) -> bool:
        """Get if the data of a route and a tissue has error bars.

        Args:
            route: "PO" or "IV", a key of `routes`.
            tissue: "serum" or "urine".
        """
        return not (route == "IV" and tissue == "serum")

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        for arm in self.arms:
            changes = {
                **self.default_changes(),
                "GU__f_pgp": Q(self.pgp_interaction[arm.pgp], "dimensionless"),
            }
            # oral application
            simulations[self.simulation_id("PO", arm)] = Simulation(
                time_unit="min",
                end=50 * 60,  # at least 48 hours for urine
                preinit_changes={
                    **changes,
                    "PODOSE_tal": Q(50, "mg"),
                },
            )
            # intravenous infusion over 30 min
            simulations[self.simulation_id("IV", arm)] = Simulation(
                time_unit="min",
                end=50 * 60,  # at least 48 hours for urine
                preinit_changes={
                    **changes,
                    "Ri_tal": Q(30, "mg") / Q(30, "min"),
                },
                changes=[Change(30, {"Ri_tal": Q(0, "mg/min")})],
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        for arm in self.arms:
            for route, (dose, label) in self.routes.items():
                for fig_id, (tissue, yid) in self.tissues.items():
                    key = f"fm_tal_{label}_{dose}{arm.suffix.lower()}_{tissue}"
                    mappings[self.to_sid(key)] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=self.to_sid(
                                f"{fig_id}_tal_TAL_{route}{arm.suffix}"
                            ),
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd" if self.has_sd(route, tissue) else None,
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_{self.simulation_id(route, arm)}",
                            xid="time",
                            yid=yid,
                        ),
                        metadata=PKPDMappingMetaData(
                            tissue=Tissue(tissue),
                            route=Route.PO if route == "PO" else Route.IV,
                            application_form=(
                                ApplicationForm.TABLET
                                if route == "PO"
                                else ApplicationForm.SOLUTION
                            ),
                            dosing=Dosing.SINGLE,
                            health=Health.HEALTHY,
                            fasting=Fasting.FASTED,
                            coadministration=arm.coadministration,
                        ),
                    )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures: list[Figure] = []

        for route, (dose, label) in self.routes.items():
            for fig_id, (tissue, yid) in self.tissues.items():
                f = Figure(
                    experiment=self,
                    sid=self.to_sid(f"{fig_id}_TAL_{route}_{tissue}"),
                    num_rows=1,
                    num_cols=1,
                    name=self.__class__.__name__,
                )
                plots = f.create_plots(
                    xaxis=Axis(
                        self.label_time,
                        unit="hour",
                        max=25 if tissue == "serum" else 50,
                    ),
                    legend=True,
                )
                plots[0].set_yaxis(
                    self.label_tal if tissue == "serum" else self.label_tal_urine,
                    unit="µM" if tissue == "serum" else "µmole",
                    scale="linear",
                )

                # simulations
                for arm in self.arms:
                    plots[0].add_data(
                        task=f"task_{self.simulation_id(route, arm)}",
                        xid="time",
                        yid=yid,
                        label=f"Sim {label} {dose} [mg]{arm.label}",
                        color=arm.color,
                    )
                # data
                for arm in self.arms:
                    plots[0].add_data(
                        dataset=self.to_sid(f"{fig_id}_tal_TAL_{route}{arm.suffix}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd" if self.has_sd(route, tissue) else None,
                        count="count",
                        label=f"{label} {dose} [mg]{arm.label}",
                        color=arm.color,
                        linestyle="--" if tissue == "serum" else "",
                    )

                figures.append(f)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(Schwarz2007, output_dir=Schwarz2007.__name__)
