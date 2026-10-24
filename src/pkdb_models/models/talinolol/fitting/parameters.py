"""The fit parameters of the talinolol model.

The pharmacokinetics of talinolol are fitted on the intravenous and oral data
together (subset PK): the intestinal secretion of the systemic talinolol by
P-glycoprotein couples both routes, its basolateral transport and efflux
determine the nonrenal clearance after an intravenous dose and the
bioavailability after an oral dose. The start values are chosen by hand
against the literature (IV 30 mg: CL 380 ml/min, half-life 15 hr, 46 % in the
urine; oral 100 mg: Cmax 160 ng/ml, tmax 2.7 hr, F 0.79; the AUC per mg rises
1.5 fold from 25 to 400 mg). Fixed: the fraction unbound `fup_tal` (0.4, not
identifiable, it only enters as a product with `Kp_tal`, `KI__TALEX_f` and the
transports), the biliary export `LI__TALEX_k` (no effect, the hepatic uptake
limits), the basolateral transport of the enterocytes `GU__TALEX_k` (0.35
1/min, not identifiable: its profile likelihood is flat above 0.1 1/min, the
transport is fast against the apical uptake and the efflux), the
enterohepatic circulation, the transit of the intestine and the
profiles of P-gp and OATP2B1 along it.
"""

from sbmlsim.fit import FitParameter

#: the pharmacokinetics
parameters_pk: list[FitParameter] = [
    # tissue distribution: Vss 2.4-3.3 l/kg, the distribution in the first
    # hours after an intravenous dose
    FitParameter(
        pid="Kp_tal",
        start_value=4.15,
        lower_bound=0.3,
        upper_bound=30,
        unit="dimensionless",
    ),
    FitParameter(
        pid="ftissue_tal",
        start_value=1.13,
        lower_bound=0.01,
        upper_bound=50,
        unit="l/min",
    ),
    # renal clearance relative to the filtration of the unbound talinolol:
    # 151-311 ml/min, 3.7-7.7 at fup 0.4 and GFR 101 ml/min
    FitParameter(
        pid="KI__TALEX_f",
        start_value=5.2,
        lower_bound=1,
        upper_bound=20,
        unit="dimensionless",
    ),
    # hepatic uptake, the biliary excretion: 3.7-24.7 % of an IV dose in the
    # bile of T-drain patients (Terhaag1989)
    FitParameter(
        pid="LI__TALIM_Vmax",
        start_value=0.05,
        lower_bound=1e-4,
        upper_bound=1,
        unit="mmole/min/l",
    ),
    # dissolution and gastric emptying: tmax 3-4.6 hr
    FitParameter(
        pid="Ka_dis_tal",
        start_value=0.6,
        lower_bound=0.1,
        upper_bound=10,
        unit="1/hr",
    ),
    # apical uptake into the enterocytes: the bioavailability 0.55-0.73
    FitParameter(
        pid="GU__TALABS_k",
        start_value=0.021,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    # efflux by P-glycoprotein: the bioavailability and the intestinal
    # secretion after an IV dose (nonrenal clearance 114-200 ml/min), its
    # saturation the increase of the AUC per mg with the dose (DeMey1995)
    FitParameter(
        pid="GU__TALEFL_Vmax",
        start_value=0.0026,
        lower_bound=1e-5,
        upper_bound=1,
        unit="mmole/min/l",
    ),
    FitParameter(
        pid="GU__TALEFL_Km",
        start_value=0.00095,
        lower_bound=1e-5,
        upper_bound=1,
        unit="mM",
    ),
]
