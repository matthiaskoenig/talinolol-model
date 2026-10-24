"""The simulation experiments of the talinolol model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.talinolol import MODEL
from pkdb_models.models.talinolol.experiments.misc import (
    ApplicationExperiment,
    IntestineInfusionExperiment,
)
from pkdb_models.models.talinolol.experiments.scan import (
    Gramatte1996Scan,
    Krueger2001Scan,
    OATP1B1FunctionScan,
    OATP2B1FunctionScan,
    PGFunctionScan,
    RenalFunctionScan,
    SiteDependencyScan,
)
from pkdb_models.models.talinolol.experiments.studies import (
    Bernsdorf2006,
    Bogman2005,
    DeMey1995,
    Fan2009a,
    Fan2009b,
    Giessmann2004,
    Gramatte1996,
    Han2009,
    Haustein1981,
    He2007,
    He2012,
    Juan2007,
    Krueger2001,
    Nguyen2014,
    Nguyen2015,
    Ruike2010,
    Schwarz1999,
    Schwarz2000,
    Schwarz2005,
    Schwarz2007,
    Siegmund2003,
    Terhaag1983,
    Terhaag1989,
    Trausch1995,
    Tubic2006a,
    Wang2013,
    Westphal2000a,
    Westphal2000b,
    Wetterich1996,
    Xiao2012,
    Yan2013,
    Zeng2009,
    Zhang2005,
    Zschiesche2002,
)

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    "studies": [
        Bernsdorf2006,
        Bogman2005,
        DeMey1995,
        Fan2009a,
        Fan2009b,
        Giessmann2004,
        Gramatte1996,
        Han2009,
        Haustein1981,
        He2007,
        He2012,
        Juan2007,
        Krueger2001,
        Nguyen2014,
        Nguyen2015,
        Ruike2010,
        Schwarz1999,
        Schwarz2000,
        Schwarz2005,
        Schwarz2007,
        Siegmund2003,
        Terhaag1983,
        Terhaag1989,
        Trausch1995,
        Tubic2006a,
        Wang2013,
        Westphal2000a,
        Westphal2000b,
        Wetterich1996,
        Xiao2012,
        Yan2013,
        Zeng2009,
        Zhang2005,
        Zschiesche2002,
    ],
    "misc": [
        ApplicationExperiment,
        IntestineInfusionExperiment,
    ],
    "scans": [
        Gramatte1996Scan,
        Krueger2001Scan,
        OATP1B1FunctionScan,
        OATP2B1FunctionScan,
        PGFunctionScan,
        RenalFunctionScan,
        SiteDependencyScan,
    ],
}
EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"] + EXPERIMENTS["scans"]


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")
