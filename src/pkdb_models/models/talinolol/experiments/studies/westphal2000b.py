"""Simulation experiment of the study Westphal2000b."""

from typing import ClassVar, override

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


class Westphal2000b(TalinololSimulationExperiment):
    """Simulation experiment of Westphal2000b.

    Eight healthy men (Fig 1, the schedule): 30 mg talinolol intravenously over
    30 min (fasted 10 hr before to 5 hr after, serum until 36.5 hr, urine over 2
    days); after 8 days 100 mg talinolol orally every day for 14 days without a
    dose on day 8 (study days 8 to 21), 600 mg rifampicin every day from
    treatment day 8 for 9 days; oral profiles (serum, urine over 24 hr) on
    treatment day 7 (control) and 14 (rifampicin), a second intravenous dose
    three days after the last oral dose (rifampicin).

    The urine of the data is the renal clearance times the AUC (Table I); the
    oral AUC of Table I is normalized to the intravenous dose of 30 mg (F =
    873/1585 = 55.1 %), the urine of the oral dose uses the AUC0-24 of 100 mg
    (the copy of the data is corrected).

    Rifampicin induces the intestinal P-glycoprotein (duodenal P-gp 4.2 fold
    by Western blot, `pgp_interaction`), set from the first day of rifampicin
    on; the arms are validation data of the interaction (observed AUC ratio
    0.65 oral, 0.79 IV). The hepatic and renal P-gp are not changed (the
    renal clearance rises by 35 %, not significant).
    """

    yids: ClassVar[dict[str, str]] = {
        "serum": "[Cve_tal]",
        "urine": "Aurine_tal",
    }
    #: the arms: the key of the simulation and mapping, the activity of the
    #: intestinal P-gp
    arms: ClassVar[dict[str, float]] = {
        "": TalinololSimulationExperiment.pgp_interaction["none"],
        "rif_": TalinololSimulationExperiment.pgp_interaction["rifampicin"],
    }
    colors: ClassVar[dict[str, str]] = {
        "": "black",
        "rif_": TalinololSimulationExperiment.colors_pg_function["P-gp ↑"],
    }
    #: the oral profiles are on treatment day 7 and 14, the days after the
    #: first oral dose
    profile_day: ClassVar[dict[str, int]] = {"": 6, "rif_": 13}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig2", "Tab1a"]:
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                intervention = str(intervention).replace(" ", "")
                route = "po" if intervention.startswith("TAL_PO") else "iv"
                arm = "rif_" if "RIF" in intervention else ""
                df_intervention = df_intervention.copy()
                if fig_id == "Fig2" and route == "po" and arm:
                    # the profile of treatment day 14 in hr after its dose, the
                    # control is curated in days after the first dose
                    df_intervention["time"] = (
                        df_intervention["time"] + self.profile_day[arm] * 24
                    )
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                tissue = "serum" if fig_id == "Fig2" else "urine"
                dsets[f"tal_{route}_{arm}{tissue}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}

        for arm, f_pgp in self.arms.items():
            # oral: 100 mg every day for 14 days, no dose on day 8; the urine
            # is collected per day; rifampicin from treatment day 8 on
            days = [*range(1, 7), *range(8, 14)]
            changes = [
                self.add_doses(
                    [day * 24 * 60 for day in days], {"PODOSE_tal": Q(100, "mg")}
                ),
                Change(
                    [day * 24 * 60 for day in days],
                    {
                        # reset of the urine amount for the daily collection,
                        # the total amount of the simulation is not the
                        # cumulative one
                        "Aurine_tal": Q(0, "mmole"),
                    },
                ),
                # the daily collection of day 8 without a dose, rifampicin
                # from treatment day 8 on
                Change(
                    7 * 24 * 60,
                    {
                        "Aurine_tal": Q(0, "mmole"),
                        "GU__f_pgp": Q(f_pgp, "dimensionless"),
                    },
                ),
            ]
            simulations[f"tal_po_100_multi_{arm}".rstrip("_")] = Simulation(
                time_unit="min",
                end=14 * 24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_tal": Q(100, "mg"),
                },
                changes=changes,
            )

            # intravenous infusion over 30 min, urine over 2 days
            simulations[f"tal_iv_30_{arm}".rstrip("_")] = Simulation(
                time_unit="min",
                end=30 + 49.5 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "Ri_tal": Q(30, "mg") / Q(30, "min"),
                    "GU__f_pgp": Q(f_pgp, "dimensionless"),
                },
                changes=[
                    Change(
                        30,
                        {
                            "Ri_tal": Q(0, "mg/min"),
                        },
                    )
                ],
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        for arm in self.arms:
            coadministration = (
                Coadministration.RIFAMPICIN if arm else Coadministration.NONE
            )
            for tissue, yid in self.yids.items():
                mappings[f"fm_tal_po_100_multi_{arm}{tissue}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"tal_po_{arm}{tissue}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_po_100_multi_{arm}".rstrip("_"),
                        xid="time",
                        yid=yid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue(tissue),
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=coadministration,
                    ),
                )
                mappings[f"fm_tal_iv_30_{arm}{tissue}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"tal_iv_{arm}{tissue}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_tal_iv_30_{arm}".rstrip("_"),
                        xid="time",
                        yid=yid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue(tissue),
                        route=Route.IV,
                        application_form=ApplicationForm.SOLUTION,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=coadministration,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures: dict[str, Figure] = {}

        for route in ["po", "iv"]:
            for tissue, yid in self.yids.items():
                ylabel = self.label_tal if tissue == "serum" else self.label_tal_urine
                sid = f"Fig2_TAL_{route.upper()}_{tissue}"
                f = Figure(
                    experiment=self,
                    sid=sid,
                    num_rows=1,
                    num_cols=1,
                    name=self.__class__.__name__,
                )
                plots = f.create_plots(
                    xaxis=Axis(
                        self.label_time, unit="day" if route == "po" else "hour"
                    ),
                    legend=True,
                )
                plots[0].set_yaxis(
                    ylabel, unit="µM" if tissue == "serum" else "µmole", scale="linear"
                )

                for arm in self.arms:
                    suffix = " + rifampicin" if arm else ""
                    task = (
                        f"task_tal_po_100_multi_{arm}"
                        if route == "po"
                        else f"task_tal_iv_30_{arm}"
                    ).rstrip("_")
                    # simulation
                    plots[0].add_data(
                        task=task,
                        xid="time",
                        yid=yid,
                        label=("Sim po 100 [mg]" if route == "po" else "Sim iv 30 [mg]")
                        + suffix,
                        color=self.colors[arm],
                    )
                    # data
                    plots[0].add_data(
                        dataset=f"tal_{route}_{arm}{tissue}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=("100 [mg]" if route == "po" else "30 [mg]") + suffix,
                        color=self.colors[arm],
                        linestyle="--" if tissue == "serum" else "",
                    )

                figures[sid] = f

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Westphal2000b, output_dir=Westphal2000b.__name__)
