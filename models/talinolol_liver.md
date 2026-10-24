# Model for talinolol elimination in the liver

Model `talinolol_liver`, SBML Level 3 Version 2, read from talinolol\_liver.xml, written by sbmlode 0.3.0.

Model for talinolol elimination in the liver

Model for the hepatic uptake and biliary excretion of talinolol in SBML. Talinolol is not metabolized (the metabolites in the urine are 0.33 % of the dose, Trausch1995), it is taken up into the liver (OATP1B1, TALIM) and excreted unchanged into the bile (P-glycoprotein, TALEX). The bile reaches the duodenum (TALEHC, the enterohepatic circulation); the bile collected by a T-drain after a cholecystectomy is not (f\_EHC 0).

enterohepatic circulation (see Terhaag1989); "The biliary clearance amounted to 43 ml/hr/kg (range: 13-212 ml/hr/kg)."

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vext}$ | `Vext` | plasma | $4$ | l | ✓ |
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |
| $\mathrm{Vbaso}$ | `Vbaso` | basolateral membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vbi}$ | `Vbi` | bile | $1$ | l | ✓ |
| $\mathrm{Vduodenum}$ | `Vduodenum` | intestinal lumen (duodenum) | $0.1$ | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{tal}_{\mathrm{ext}}$ | `tal_ext` | talinolol (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}$ | `tal` | talinolol (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{bi}}$ | `tal_bi` | talinolol (bile) | $\mathrm{Vbi}$ |  | mmol | amount |
| $\mathrm{tal}_{\mathrm{duodenum}}$ | `tal_duodenum` | talinolol (duodenum) | $\mathrm{Vduodenum}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{fup}_{\mathrm{tal}}$ | `fup_tal` | fraction unbound in plasma tal | $0.4$ | \- | ✓ |
| $\mathrm{Abile}_{\mathrm{tal}}$ | `Abile_tal` | cumulative talinolol (bile) | $0$ | mmol |  |
| $\mathrm{bile}_{\mathrm{flow}}$ | `bile_flow` | bile flow | $0.000766666666666667$ | l/min | ✓ |
| $\mathrm{Cbile}_{\mathrm{tal}}$ | `Cbile_tal` | talinolol (bile) |  | mmol/l |  |
| $\mathrm{TALIM}_{\mathrm{Vmax}}$ | `TALIM_Vmax` | Vmax for talinolol import | $0.0369201073419107$ | mmol/min/l | ✓ |
| $\mathrm{TALIM}_{\mathrm{Km\_tal}}$ | `TALIM_Km_tal` | Km for talinolol import | $0.301$ | mmol/l | ✓ |
| $f_{\mathrm{oatp1b1}}$ | `f_oatp1b1` | activity of OATP1B1 | $1$ | \- | ✓ |
| $\mathrm{TALEX}_{\mathrm{k}}$ | `TALEX_k` | rate for talinolol export in bile | $0.15$ | 1/min | ✓ |
| $f_{\mathrm{pgp}}$ | `f_pgp` | activity of P-glycoprotein (liver) | $1$ | \- | ✓ |
| $f_{\mathrm{EHC}}$ | `f_EHC` | factor for modifying EHC | $1$ | \- | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{tal}_{\mathrm{bi}} &= 0 \cdot \mathrm{Vbi}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{Cbile}_{\mathrm{tal}} &= \frac{v_{\mathrm{TALEX}}}{\mathrm{bile}_{\mathrm{flow}}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{TALIM}}$ | `TALIM` | talinolol import | $\mathrm{tal}_{\mathrm{ext}} \rightleftharpoons \mathrm{tal}$ |
| $v_{\mathrm{TALEX}}$ | `TALEX` | talinolol bile export | $\mathrm{tal} \longrightarrow \mathrm{tal}_{\mathrm{bi}}$ |
| $v_{\mathrm{TALEHC}}$ | `TALEHC` | talinolol enterohepatic circulation | $\mathrm{tal}_{\mathrm{bi}} \longrightarrow \mathrm{tal}_{\mathrm{duodenum}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{TALIM}} &= \frac{\frac{f_{\mathrm{oatp1b1}} \cdot \mathrm{TALIM}_{\mathrm{Vmax}}}{\mathrm{TALIM}_{\mathrm{Km\_tal}}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}} - \mathrm{tal}\right)}{1 + \frac{\mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}}{\mathrm{TALIM}_{\mathrm{Km\_tal}}} + \frac{\mathrm{tal}}{\mathrm{TALIM}_{\mathrm{Km\_tal}}}} \\[1ex]
v_{\mathrm{TALEX}} &= f_{\mathrm{pgp}} \cdot \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{tal} \\[1ex]
v_{\mathrm{TALEHC}} &= f_{\mathrm{EHC}} \cdot v_{\mathrm{TALEX}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{TALIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALIM}} - v_{\mathrm{TALEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{bi}}}{\mathrm{d} t} &= v_{\mathrm{TALEX}} - v_{\mathrm{TALEHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{duodenum}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALEHC}}}{\mathrm{Vduodenum}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Abile}_{\mathrm{tal}}}{\mathrm{d} t} &= v_{\mathrm{TALEX}} \qquad \text{(rate rule)}
\end{aligned}
$$
