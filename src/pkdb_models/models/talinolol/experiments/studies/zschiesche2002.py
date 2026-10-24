"""Simulation experiment of the study Zschiesche2002."""

from typing import override

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Zschiesche2002(TalinololSimulationExperiment):
    """Simulation experiment of Zschiesche2002.

    The serum samples of Westphal2000b re-assayed for the enantiomers: 8 healthy
    men, 30 mg talinolol intravenously within 30 min (Fig4), then 100 mg orally
    once a day for 14 days without a dose on day 8, the profile of day 7 (Fig5);
    the racemate is the sum of R- and S-talinolol. The same samples are
    measured as total talinolol in Westphal2000b, the rifampicin arms are
    simulated there.

    Corrections of the digitized data (`data/`): Fig5, the 0.5 hr sample is
    missing, every value after 0 hr is one sample time earlier (AUC0-24 of S, R
    1260, 1341 ng*h/ml against Tab2 1256, 1332; as digitized 1502, 1603), the
    48 hr value is not digitized. Fig4, the pre-dose value is at 0 hr (was 0.33
    hr); S at 1 hr (271.6 ng/ml) is the peak of S (Cmax 269 ng/ml), not the 1 hr
    value (R 105.8 ng/ml), the 1 hr value of S and of the sum is removed. The
    samples of 0-2.5 hr cannot be separated in the raster figure.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}
        for fig_id in ["Fig4", "Fig5"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                intervention = df_label.intervention.unique()[0]
                if label.endswith(("_S", "_R")):
                    continue

                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[self.to_sid(f"tal_{intervention}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations: dict[str, Simulation] = {}

        # intravenous
        simulations["tal_iv_30"] = Simulation(
            time_unit="min",
            end=30 + 39.5 * 60,
            preinit_changes={
                **self.default_changes(),
                "Ri_tal": Q(30, "mg") / Q(30, "min"),
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

        # oral: 100 mg once a day for 14 days, no dose on day 8 (doses at the
        # days 1-7 and 9-14); the profile of Fig5 is the one of day 7
        days = [*range(1, 7), *range(8, 14)]
        simulations["tal_po_100_multi"] = Simulation(
            time_unit="min",
            end=14 * 24 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
            changes=[
                self.add_doses(
                    [day * 24 * 60 for day in days], {"PODOSE_tal": Q(100, "mg")}
                ),
            ],
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}

        mappings["fm_zschiesche2002_tal_po_100_multi"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="tal_TAL_PO",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_po_100_multi", xid="time", yid="[Cve_tal]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.SERUM,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,  # film-coated tablet
                dosing=Dosing.MULTIPLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
            ),
        )

        mappings["fm_zschiesche2002_tal_iv_30"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="tal_TAL_IV",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self, task="task_tal_iv_30", xid="time", yid="[Cve_tal]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.SERUM,
                route=Route.IV,
                application_form=ApplicationForm.SOLUTION,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
            ),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig4"
        fig4 = Figure(
            experiment=self,
            sid=self.to_sid(f"{name}_IV_serum"),
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )

        plots4 = fig4.create_plots(
            xaxis=Axis(self.label_time, unit="hour"), legend=True
        )
        plots4[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots4[0].add_data(
            task="task_tal_iv_30",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 30 [mg]",
            color="black",
        )
        # data
        plots4[0].add_data(
            dataset="tal_TAL_IV",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="30 [mg]",
            color="black",
        )

        # figure 5
        name = "Fig5"
        fig5 = Figure(
            experiment=self,
            sid=self.to_sid(f"{name}_PO_MULTI_serum"),
            num_rows=1,
            num_cols=1,
            name=self.__class__.__name__,
        )
        plots5 = fig5.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots5[0].set_yaxis(self.label_tal, unit="µM", scale="linear")

        # simulation
        plots5[0].add_data(
            task="task_tal_po_100_multi",
            xid="time",
            yid="[Cve_tal]",
            label="Sim 100 po multi [mg]",
            color="black",
        )
        # data
        plots5[0].add_data(
            dataset="tal_TAL_PO",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 po multi [mg]",
            color="black",
        )

        return self.figures_by_sid(fig4, fig5)


if __name__ == "__main__":
    MODEL.run_experiments(Zschiesche2002, output_dir=Zschiesche2002.__name__)
