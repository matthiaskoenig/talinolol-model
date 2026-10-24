# Model for talinolol elimination in the kidneys

Model `talinolol_kidney`, SBML Level 3 Version 2, read from talinolol\_kidney.xml, written by sbmlode 0.3.0.

Model for talinolol elimination in the kidneys

Model for the renal excretion of talinolol (tal) encoded in SBML format.

Talinolol is excreted unchanged in the urine by glomerular filtration and a net tubular secretion: the renal clearance (151-311 ml/min) is several times the filtration of the unbound talinolol. The renal excretion is the filtration of the unbound talinolol GFR \* fup\_tal times TALEX\_f (1 is filtration alone, above 1 a net secretion), so that it follows the renal function as the glomerular filtration rate does.

On average, about 60% of talinolol and talinolol metabolites was excreted by kidney and about 40% extrarenally. {Trausch1995}

Other metabolites then talinolol are almost not detectable in urine. I.e. sum of metabolites is 0.33% of dose vs. talinolol 52.83 % dose {Trausch1995}

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
| $\mathrm{Vki}$ | `Vki` | kidney | $1.5$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{tal}_{\mathrm{ext}}$ | `tal_ext` | talinolol (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{urine}}$ | `tal_urine` | talinolol (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $\mathrm{fup}_{\mathrm{tal}}$ | `fup_tal` | fraction unbound in plasma tal | $0.4$ | \- | ✓ |
| $\mathrm{TALEX}_{\mathrm{f}}$ | `TALEX_f` | renal clearance of unbound talinolol relative to the GFR | $7.66469242599538$ | \- | ✓ |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{tal}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{TALEX}}$ | `TALEX` | excretion talinolol | $\mathrm{tal}_{\mathrm{ext}} \longrightarrow \mathrm{tal}_{\mathrm{urine}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{TALEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{TALEX}_{\mathrm{f}} \cdot \mathrm{tal}_{\mathrm{ext}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{TALEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{TALEX}}
\end{aligned}
$$
