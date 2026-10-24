"""Simulation experiment of the study Westphal2000a."""

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


class Westphal2000a(TalinololSimulationExperiment):
    """Simulation experiment of Westphal2000a.

    Ten healthy volunteers, five period changeover after an overnight fast:
    30 mg talinolol intravenously over 2 hr, 100 mg orally (tablet), 0.5 mg
    digoxin orally, and digoxin with talinolol IV or oral. Serum (Fig 2, mean
    and SD, IV until 6 hr, oral until 12 hr) and urine over 48 hr; the urine of
    the data is the renal clearance times the AUC (Table II), the amount
    excreted in 48 hr. The non-renal clearance times the AUC is no fecal
    amount (after an oral dose it holds the unabsorbed talinolol) and is not
    used.

    Digoxin does not change the pharmacokinetics of talinolol (Table II), the
    arms with digoxin are simulated as talinolol alone and are a validation of
    this (no interaction).
    """

    yids: ClassVar[dict[str, str]] = {
        "serum": "[Cve_tal]",
        "urine": "Aurine_tal",
    }
    #: the arms: the key of the mapping and the intervention of the data
    arms: ClassVar[dict[str, str]] = {
        "": "TAL",
        "dgx_": "DGX, TAL",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig2", "Tab2a"]:
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                if fig_id == "Fig2":
                    dsets[self.to_sid(f"tal_{intervention}_serum")] = dset
                elif fig_id == "Tab2a":
                    for tissue in df_intervention.tissue.unique():
                        dset_tissue = dset[dset.tissue == tissue]
                        dsets[self.to_sid(f"tal_{intervention}_{tissue}")] = dset_tissue

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}
        # oral
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=50 * 60,  # at least 48 hours for urine
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )
        # intravenous infusion over 2 hr
        simulations["tal_iv_30"] = Simulation(
            time_unit="min",
            end=120 + 50 * 60,
            preinit_changes={
                **self.default_changes(),
                "Ri_tal": Q(30, "mg") / Q(120, "min"),
            },
            changes=[
                Change(
                    120,
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

        for arm, intervention in self.arms.items():
            coadministration = (
                Coadministration.DIGOXIN if arm else Coadministration.NONE
            )
            for tissue, yid in self.yids.items():
                for route, dose in (("po", 100), ("iv", 30)):
                    mappings[f"fm_tal_{route}_{dose}_{arm}{tissue}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=self.to_sid(
                                f"tal_{intervention}_{route.upper()}_{tissue}"
                            ),
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self, task=f"task_tal_{route}_{dose}", xid="time", yid=yid
                        ),
                        metadata=PKPDMappingMetaData(
                            tissue=Tissue(tissue),
                            route=Route.PO if route == "po" else Route.IV,
                            application_form=(
                                ApplicationForm.TABLET
                                if route == "po"
                                else ApplicationForm.SOLUTION
                            ),
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

        for route, dose in (("po", 100), ("iv", 30)):
            for tissue, yid in self.yids.items():
                if tissue == "serum":
                    ylabel = self.label_tal
                    max_value = 13 if route == "po" else 7
                else:
                    ylabel = self.label_tal_urine
                    max_value = 50

                sid = self.to_sid(f"Fig2_TAL_{route.upper()}_{tissue}")
                f = Figure(
                    experiment=self,
                    sid=sid,
                    num_rows=1,
                    num_cols=1,
                    name=self.__class__.__name__,
                )
                plots = f.create_plots(
                    xaxis=Axis(self.label_time, unit="hour", min=-0.5, max=max_value),
                    legend=True,
                )
                plots[0].set_yaxis(
                    ylabel, unit="µM" if tissue == "serum" else "µmole", scale="linear"
                )

                # simulation
                plots[0].add_data(
                    task=f"task_tal_{route}_{dose}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {route} {dose} [mg]",
                    color="black",
                )

                # data
                for arm, intervention in self.arms.items():
                    plots[0].add_data(
                        dataset=self.to_sid(
                            f"tal_{intervention}_{route.upper()}_{tissue}"
                        ),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} [mg]" + (" + digoxin" if arm else ""),
                        color="tab:orange" if arm else "black",
                        linestyle="--" if tissue == "serum" else "",
                    )

                figures[sid] = f

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Westphal2000a, output_dir=Westphal2000a.__name__)
