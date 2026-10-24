"""Simulation experiment of the study Haustein1981."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.base_experiment import (
    TalinololSimulationExperiment,
)


class Haustein1981(TalinololSimulationExperiment):
    """Simulation experiment of Haustein1981.

    Five patients with a heart disease (ischemic heart disease, hypertension or
    mitral valve disease, `Health.HEART_DISEASE`; S1-S5 are G.S., J.E., G.V.,
    E.M. and L.B.) on a maintenance dose of 150-300 mg talinolol per day
    exchanged one dose for 100 mg 14C-talinolol (dragee, 888 kBq per 100 mg):
    plasma radioactivity 1-8 hr (Fig1, mean and SD of 5) and urine 0-72 hr
    (Tab1a, individuals and mean). The patient J.A. (S6) received 10 mg
    14C-talinolol intravenously on the 2nd day after a cholecystectomy, with the
    bile drained by a Kerr tube (`Health.CHOLECYSTECTOMY`): plasma and bile
    concentration 0-8 hr (Fig2) and bile and urine amounts 0-72 hr (Tab2a).
    Three healthy volunteers (A, B, C) took 100 mg unlabelled talinolol as a
    solution (water with 10 % ethanol and 5 % propylene glycol): urine 0-48
    hr by thin layer chromatography with a recovery of 78 % (Tab3a, not
    corrected).

    The radioactivity follows only the labelled dose, so the tracer data are
    simulated as single doses: exactly so for linear kinetics, approximately
    for the saturable intestinal P-gp of the model. The unlabelled maintenance
    doses are not simulated. The radioactivity is talinolol and its
    metabolites (m-OH-talinolol, small).

    The amounts are radioactivity converted with the specific activity of the
    paper's percentages, 888 kBq per 100 mg (oral) and per 10 mg (intravenous,
    51.19 % of the dose in the urine = 454.5 kBq); with the stated 1.06 MBq per
    10 mg the intravenous amounts and concentrations would be 0.838 times
    lower. The Kerr tube drains a part of the bile (the ratio of tube and gut
    is unknown); the bile is simulated as fully drained (`LI__f_EHC` 0), so
    the measured bile amount is a lower bound of the simulated one.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in [
            "Fig1",  # plasma concentration, mean of the patients S1-S5
            "Fig2",  # plasma and bile concentration of S6
            "Tab1a",  # cumulative amount urine, individuals S1-S5
            "Tab1a_mean",  # cumulative amount urine, mean of S1-S5
            "Tab2a",  # cumulative amount urine and bile of S6
            "Tab3a",  # cumulative amount urine, volunteers A, B, C
        ]:
            parameter = "mean" if fig_id in ["Fig1", "Tab1a_mean"] else "value"
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion(parameter, 1 / self.Mr.tal)
                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # oral: 14C-talinolol dragee of the patients, solution of the volunteers
        simulations["tal_po_100"] = Simulation(
            time_unit="min",
            end=73 * 60,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_tal": Q(100, "mg"),
            },
        )

        # intravenous: S6, the bile drained by a Kerr tube
        simulations["tal_iv_10"] = Simulation(
            time_unit="min",
            end=73 * 60,
            preinit_changes={
                **self.default_changes(),
                "IVDOSE_tal": Q(10, "mg"),
                "LI__f_EHC": Q(0, "dimensionless"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # patients S1-S5, 14C-talinolol dragee
        po_data = {
            "plasma_mean": ("[Cve_tal]", Tissue.PLASMA),
            "urine_mean": ("Aurine_tal", Tissue.URINE),
            **{f"urine_S{k}": ("Aurine_tal", Tissue.URINE) for k in range(1, 6)},
        }
        for dset, (yid, tissue) in po_data.items():
            mean = dset.endswith("_mean")
            mappings[f"fm_tal_po_100_{dset}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dset,
                    xid="time",
                    yid="mean" if mean else "value",
                    yid_sd="mean_sd" if mean else None,
                    count="count",
                ),
                observable=FitData(self, task="task_tal_po_100", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=tissue,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEART_DISEASE,
                    fasting=Fasting.NR,
                ),
            )

        # patient S6, intravenous 14C-talinolol
        iv_data = {
            "plasma_S6": ("[Cve_tal]", Tissue.PLASMA),
            "bile_S6": ("LI__Cbile_tal", Tissue.BILE),
            "urine_amount_S6": ("Aurine_tal", Tissue.URINE),
            "bile_amount_S6": ("LI__Abile_tal", Tissue.BILE),
        }
        for dset, (yid, tissue) in iv_data.items():
            mappings[f"fm_tal_iv_10_{dset}"] = FitMapping(
                self,
                reference=FitData(
                    self, dataset=dset, xid="time", yid="value", count="count"
                ),
                observable=FitData(self, task="task_tal_iv_10", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=tissue,
                    route=Route.IV,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.CHOLECYSTECTOMY,
                    fasting=Fasting.NR,
                ),
            )

        # healthy volunteers A, B, C, unlabelled talinolol solution
        for n in ["A", "B", "C"]:
            mappings[f"fm_tal_po_100_urine_{n}"] = FitMapping(
                self,
                reference=FitData(
                    self, dataset=f"urine_{n}", xid="time", yid="value", count="count"
                ),
                observable=FitData(
                    self, task="task_tal_po_100", xid="time", yid="Aurine_tal"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_po(),
            **self.figure_iv(),
            **self.figure_volunteers(),
        }

    def figure_po(self) -> dict[str, Figure]:
        """Figure of the patients S1-S5 after 100 mg oral 14C-talinolol."""
        f = Figure(
            experiment=self,
            sid="Fig1_Tab1a_PO",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (heart disease, 100 mg PO)",
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_tal_plasma, unit="µM")
        plots[1].set_yaxis(self.label_tal_urine, unit="µmole")

        for k, yid in enumerate(["[Cve_tal]", "Aurine_tal"]):
            plots[k].add_data(
                task="task_tal_po_100",
                xid="time",
                yid=yid,
                label="Sim 100 [mg] PO",
                color="black",
            )

        plots[0].add_data(
            dataset="plasma_mean",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg] PO (14C)",
            color="black",
        )
        for k in range(1, 6):
            plots[1].add_data(
                dataset=f"urine_S{k}",
                xid="time",
                yid="value",
                count="count",
                label="individuals" if k == 1 else None,
                color="darkgrey",
                linestyle="",
            )
        plots[1].add_data(
            dataset="urine_mean",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="100 [mg] PO (14C)",
            color="black",
            linestyle="",
        )

        return self.figures_by_sid(f)

    def figure_iv(self) -> dict[str, Figure]:
        """Figures of the patient S6 after 10 mg intravenous 14C-talinolol."""
        panels_by_fig = {
            # concentrations, measured up to 8 hr
            "Fig2_IV": (
                Axis(self.label_time, unit="hr", min=0, max=9),
                {
                    "plasma_S6": ("[Cve_tal]", self.label_tal_plasma, "µM"),
                    "bile_S6": ("LI__Cbile_tal", self.label_tal_bile, "µM"),
                },
            ),
            # cumulative amounts, measured up to 72 hr
            "Tab2a_IV": (
                Axis(self.label_time, unit="hr"),
                {
                    "urine_amount_S6": ("Aurine_tal", self.label_tal_urine, "µmole"),
                    "bile_amount_S6": ("LI__Abile_tal", self.label_tal_bile, "µmole"),
                },
            ),
        }
        figures = []
        for sid, (xaxis, panels) in panels_by_fig.items():
            f = Figure(
                experiment=self,
                sid=sid,
                num_rows=1,
                num_cols=2,
                name=f"{self.__class__.__name__} (Kerr tube, 10 mg IV)",
            )
            plots = f.create_plots(xaxis=xaxis, legend=True)
            for k, (dset, (yid, label, unit)) in enumerate(panels.items()):
                plots[k].set_yaxis(label, unit=unit)
                plots[k].add_data(
                    task="task_tal_iv_10",
                    xid="time",
                    yid=yid,
                    label="Sim 10 [mg] IV",
                    color="black",
                )
                plots[k].add_data(
                    dataset=dset,
                    xid="time",
                    yid="value",
                    count="count",
                    label="10 [mg] IV (14C)",
                    color="black",
                    linestyle="--" if sid == "Fig2_IV" else "",
                )
            figures.append(f)

        return self.figures_by_sid(*figures)

    def figure_volunteers(self) -> dict[str, Figure]:
        """Figure of the urine of the volunteers A, B, C after 100 mg oral."""
        f = Figure(
            experiment=self,
            sid="Tab3a_PO_urine",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (healthy, 100 mg PO)",
        )
        plots = f.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_tal_urine, unit="µmole")

        plots[0].add_data(
            task="task_tal_po_100",
            xid="time",
            yid="Aurine_tal",
            label="Sim 100 [mg] PO",
            color="black",
        )
        for n in ["A", "B", "C"]:
            plots[0].add_data(
                dataset=f"urine_{n}",
                xid="time",
                yid="value",
                count="count",
                label="100 [mg] PO (TLC)" if n == "A" else None,
                linestyle="",
                color="black",
            )

        return self.figures_by_sid(f)


if __name__ == "__main__":
    MODEL.run_experiments(Haustein1981, output_dir=Haustein1981.__name__)
