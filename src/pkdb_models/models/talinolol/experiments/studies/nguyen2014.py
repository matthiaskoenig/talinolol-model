"""Simulation experiment of the study Nguyen2014."""

from typing import override

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Nguyen2014(TalinololSimulationExperiment):
    """Simulation experiment of Nguyen2014.

    10 healthy volunteers (8 men, 22-57 yr, 58-93 kg), a single oral dose of
    100 mg talinolol (film-coated tablet, Cordanum) after an overnight fast of
    at least 9 hr, plasma and urine 0-48 hr, in three periods: the control with
    a dietary amount of quercetin (20 mg twice a day for 6 days before the
    dose, `Coadministration.QUERCETIN`), quercetin 1500 mg with the dose and
    quercetin 500 mg t.i.d. for 6 days and 1500 mg with the dose.

    The control is the same data as the control of Nguyen2015 (identical time
    courses, Cmax 309.7 ng/ml, AUC0-48 3186.0 ng*h/ml), a duplicate which is
    not fitted. The quercetin arms are not simulated: quercetin decreased the
    exposure (AUC0-48 ratio 0.77 with the single dose, 0.79 after one week,
    not significant), the opposite of an inhibition of the intestinal P-gp,
    and no in vivo factor of quercetin on a transporter is known.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2a"]:
            df = self.load_dataframe(fig_id)
            for intervention, df_intervention in df.groupby("intervention"):
                intervention = str(intervention)
                dset = DataSet.from_df(df_intervention, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.tal)
                dsets[f"{fig_id}_tal_{intervention.replace(', ', '_')}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=50 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for fig_id in ["Fig1", "Tab2a"]:
            tissue = "plasma" if fig_id == "Fig1" else "urine"
            mappings[f"fm_nguyen2014_tal_po_100_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{fig_id}_tal_QRC_LOW_TAL",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_tal_po_100",
                    xid="time",
                    yid="[Cve_tal]" if fig_id == "Fig1" else "Aurine_tal",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue(tissue),
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,  # film-coated tablet
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.QUERCETIN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = []

        for fig_id in ["Fig1", "Tab2a"]:
            if fig_id == "Fig1":
                ylabel = self.label_tal
                yid = "[Cve_tal]"
                tissue = "plasma"
            else:
                ylabel = self.label_tal_urine
                yid = "Aurine_tal"
                tissue = "urine"

            f = Figure(
                experiment=self,
                sid=f"{fig_id}_PO_{tissue}",
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__}",
            )
            plots = f.create_plots(
                xaxis=Axis(self.label_time, unit="hour"), legend=True
            )

            plots[0].set_yaxis(
                ylabel, unit="µM" if fig_id == "Fig1" else "µmole", scale="linear"
            )

            # simulation
            plots[0].add_data(
                task="task_tal_po_100",
                xid="time",
                yid=yid,
                label="Sim 100 [mg]",
                color="black",
            )
            # data
            plots[0].add_data(
                dataset=f"{fig_id}_tal_QRC_LOW_TAL",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="100 [mg]",
                color="black",
                linestyle="--" if fig_id == "Fig1" else "",
            )

            figures.append(f)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(Nguyen2014, output_dir=Nguyen2014.__name__)
