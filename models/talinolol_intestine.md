# Model for talinolol absorption and secretion in the intestine

Model `talinolol_intestine`, SBML Level 3 Version 2, read from talinolol\_intestine.xml, written by sbmlode 0.3.0.

Model for talinolol absorption and secretion in the intestine

The intestine is a tube of six segments (duodenum, two jejunum, two ileum segments and the colon), each a lumen with its enterocytes. The oral dose dissolves into the duodenum (dissolution\_tal), the lumen is transported from segment to segment (TALFLUX\_\*, a transit of about 4.7 hr through the small intestine and 22.5 hr through the colon) and leaves the colon into the feces (TALEXC).

Talinolol, a hydrophilic beta blocker, is taken up into the enterocytes with a first order (TALABS\_\*, passive and OATP2B1) and pumped back into the lumen by P-glycoprotein (TALEFL\_\*), whose amount increases along the small intestine (pgp\_\*). The efflux saturates (TALEFL\_Km), so that the bioavailability increases with the dose (the AUC per mg rises 1.8 fold from 25 to 400 mg, DeMey1995; Wetterich1996, Siegmund2003). The basolateral membrane is passed in both directions (TALEX\_\*): the enterocytes take up talinolol from the plasma of the gut as well, and P-glycoprotein secretes it into the lumen against the gradient, the main nonrenal elimination of talinolol after an intravenous dose (Gramatte1996, Westphal2000a/b, Bernsdorf2006: an intestinal clearance of about 74 ml/min), which an inducer (rifampicin) increases after an intravenous dose as well.

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vduodenum}$ | `Vduodenum` | small intestine duodenum D | $0.322563025707332$ | l |  |
| $\mathrm{Ventero}_{\mathrm{duodenum}}$ | `Ventero_duodenum` | enterocytes small intestine duodenum D |  | l |  |
| $\mathrm{Vjejunum}_{1}$ | `Vjejunum_1` | small intestine jejunum J1 | $0.601183024172577$ | l |  |
| $\mathrm{Ventero}_{\mathrm{jejunum\_1}}$ | `Ventero_jejunum_1` | enterocytes small intestine jejunum J1 |  | l |  |
| $\mathrm{Vjejunum}_{2}$ | `Vjejunum_2` | small intestine jejunum J2 | $0.601183024172577$ | l |  |
| $\mathrm{Ventero}_{\mathrm{jejunum\_2}}$ | `Ventero_jejunum_2` | enterocytes small intestine jejunum J2 |  | l |  |
| $\mathrm{Vileum}_{1}$ | `Vileum_1` | small intestine ileum I1 | $0.944716180842621$ | l |  |
| $\mathrm{Ventero}_{\mathrm{ileum\_1}}$ | `Ventero_ileum_1` | enterocytes small intestine ileum I1 |  | l |  |
| $\mathrm{Vileum}_{2}$ | `Vileum_2` | small intestine ileum I2 | $0.944716180842621$ | l |  |
| $\mathrm{Ventero}_{\mathrm{ileum\_2}}$ | `Ventero_ileum_2` | enterocytes small intestine ileum I2 |  | l |  |
| $\mathrm{Vcolon}$ | `Vcolon` | large intestine colon | $3.8170350741116$ | l |  |
| $\mathrm{Ventero}_{\mathrm{colon}}$ | `Ventero_colon` | enterocytes large intestine colon |  | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{tal}_{\mathrm{ext}}$ | `tal_ext` | talinolol (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{feces}}$ | `tal_feces` | talinolol (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{tal}_{\mathrm{duodenum}}$ | `tal_duodenum` | talinolol (small intestine duodenum D) | $\mathrm{Vduodenum}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_duodenum}}$ | `tal_entero_duodenum` | talinolol enterocytes (small intestine duodenum D) | $\mathrm{Ventero}_{\mathrm{duodenum}}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{jejunum\_1}}$ | `tal_jejunum_1` | talinolol (small intestine jejunum J1) | $\mathrm{Vjejunum}_{1}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_jejunum\_1}}$ | `tal_entero_jejunum_1` | talinolol enterocytes (small intestine jejunum J1) | $\mathrm{Ventero}_{\mathrm{jejunum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{jejunum\_2}}$ | `tal_jejunum_2` | talinolol (small intestine jejunum J2) | $\mathrm{Vjejunum}_{2}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_jejunum\_2}}$ | `tal_entero_jejunum_2` | talinolol enterocytes (small intestine jejunum J2) | $\mathrm{Ventero}_{\mathrm{jejunum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{ileum\_1}}$ | `tal_ileum_1` | talinolol (small intestine ileum I1) | $\mathrm{Vileum}_{1}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_ileum\_1}}$ | `tal_entero_ileum_1` | talinolol enterocytes (small intestine ileum I1) | $\mathrm{Ventero}_{\mathrm{ileum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{ileum\_2}}$ | `tal_ileum_2` | talinolol (small intestine ileum I2) | $\mathrm{Vileum}_{2}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_ileum\_2}}$ | `tal_entero_ileum_2` | talinolol enterocytes (small intestine ileum I2) | $\mathrm{Ventero}_{\mathrm{ileum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{colon}}$ | `tal_colon` | talinolol (large intestine colon) | $\mathrm{Vcolon}$ | $0$ | mmol/l | concentration |
| $\mathrm{tal}_{\mathrm{entero\_colon}}$ | `tal_entero_colon` | talinolol enterocytes (large intestine colon) | $\mathrm{Ventero}_{\mathrm{colon}}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{fup}_{\mathrm{tal}}$ | `fup_tal` | fraction unbound in plasma tal | $0.4$ | \- | ✓ |
| $\mathrm{TALABS}_{\mathrm{k}}$ | `TALABS_k` | rate of the apical uptake of talinolol | $0.00358298645106167$ | 1/min | ✓ |
| $\mathrm{TALEFL}_{\mathrm{Vmax}}$ | `TALEFL_Vmax` | Vmax of the efflux of talinolol by P-glycoprotein | $0.000103428146343818$ | mmol/min/l | ✓ |
| $\mathrm{TALEFL}_{\mathrm{Km}}$ | `TALEFL_Km` | Km of the efflux of talinolol by P-glycoprotein | $0.000240407546909154$ | mmol/l | ✓ |
| $\mathrm{TALEX}_{\mathrm{k}}$ | `TALEX_k` | rate of the basolateral transport of talinolol | $0.35$ | 1/min | ✓ |
| $f_{\mathrm{velocity}}$ | `f_velocity` | parameter for velocity intestinal transport | $1$ | \- | ✓ |
| $f_{\mathrm{oatp2b1}}$ | `f_oatp2b1` | activity of the apical uptake (OATP2B1) | $1$ | \- | ✓ |
| $f_{\mathrm{pgp}}$ | `f_pgp` | activity of P-glycoprotein (intestine) | $1$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{duodenum}}$ | `pgp_duodenum` | protein amount P-gp | $0.3$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{duodenum}}$ | `oatp2b1_duodenum` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{jejunum\_1}}$ | `pgp_jejunum_1` | protein amount P-gp | $0.4$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{jejunum\_1}}$ | `oatp2b1_jejunum_1` | protein amount OATP2B1 | $0.5$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{jejunum\_2}}$ | `pgp_jejunum_2` | protein amount P-gp | $0.5$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{jejunum\_2}}$ | `oatp2b1_jejunum_2` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{ileum\_1}}$ | `pgp_ileum_1` | protein amount P-gp | $0.7$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{ileum\_1}}$ | `oatp2b1_ileum_1` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{ileum\_2}}$ | `pgp_ileum_2` | protein amount P-gp | $1.1$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{ileum\_2}}$ | `oatp2b1_ileum_2` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{pgp}_{\mathrm{colon}}$ | `pgp_colon` | protein amount P-gp | $0.25$ | \- | ✓ |
| $\mathrm{oatp2b1}_{\mathrm{colon}}$ | `oatp2b1_colon` | protein amount OATP2B1 | $0.5$ | \- | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_duodenum}}$ | `Ri_tal_duodenum` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_jejunum\_1}}$ | `Ri_tal_jejunum_1` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_jejunum\_2}}$ | `Ri_tal_jejunum_2` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_ileum\_1}}$ | `Ri_tal_ileum_1` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_ileum\_2}}$ | `Ri_tal_ileum_2` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{Ri}_{\mathrm{tal\_colon}}$ | `Ri_tal_colon` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{PODOSE}_{\mathrm{tal}}$ | `PODOSE_tal` | oral dose tal \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_tal}}$ | `Ka_dis_tal` | Ka\_dis \[1/hr\] dissolution tal | $1.40676555809381$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{tal}}$ | `Mr_tal` | Molecular weight talinolol \[g/mole\] | $363.495$ | g/mol | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{DUODENUM\_k}}$ | `TALFLUX_DUODENUM_k` | Transport rate duodenum | $0.0666666666666667$ | 1/min | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{JEJUNUM\_1\_k}}$ | `TALFLUX_JEJUNUM_1_k` | Transport rate jejunum\_1 | $0.019047619047619$ | 1/min | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{JEJUNUM\_2\_k}}$ | `TALFLUX_JEJUNUM_2_k` | Transport rate jejunum\_2 | $0.019047619047619$ | 1/min | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{ILEUM\_1\_k}}$ | `TALFLUX_ILEUM_1_k` | Transport rate ileum\_1 | $0.0121212121212121$ | 1/min | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{ILEUM\_2\_k}}$ | `TALFLUX_ILEUM_2_k` | Transport rate ileum\_2 | $0.0121212121212121$ | 1/min | ✓ |
| $\mathrm{TALFLUX}_{\mathrm{COLON\_k}}$ | `TALFLUX_COLON_k` | Transport rate colon | $0.000740740740740741$ | 1/min | ✓ |
| $\mathrm{TALUPTAKE}_{\mathrm{duodenum}}$ | `TALUPTAKE_duodenum` | net uptake talinolol duodenum |  | mmol/min |  |
| $\mathrm{TALUPTAKE}_{\mathrm{jejunum\_1}}$ | `TALUPTAKE_jejunum_1` | net uptake talinolol jejunum\_1 |  | mmol/min |  |
| $\mathrm{TALUPTAKE}_{\mathrm{jejunum\_2}}$ | `TALUPTAKE_jejunum_2` | net uptake talinolol jejunum\_2 |  | mmol/min |  |
| $\mathrm{TALUPTAKE}_{\mathrm{ileum\_1}}$ | `TALUPTAKE_ileum_1` | net uptake talinolol ileum\_1 |  | mmol/min |  |
| $\mathrm{TALUPTAKE}_{\mathrm{ileum\_2}}$ | `TALUPTAKE_ileum_2` | net uptake talinolol ileum\_2 |  | mmol/min |  |
| $\mathrm{TALUPTAKE}_{\mathrm{colon}}$ | `TALUPTAKE_colon` | net uptake talinolol colon |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{tal}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{Ventero}_{\mathrm{duodenum}} &= 0.1 \cdot \mathrm{Vduodenum} \\[1ex]
\mathrm{Ventero}_{\mathrm{jejunum\_1}} &= 0.1 \cdot \mathrm{Vjejunum}_{1} \\[1ex]
\mathrm{Ventero}_{\mathrm{jejunum\_2}} &= 0.1 \cdot \mathrm{Vjejunum}_{2} \\[1ex]
\mathrm{Ventero}_{\mathrm{ileum\_1}} &= 0.1 \cdot \mathrm{Vileum}_{1} \\[1ex]
\mathrm{Ventero}_{\mathrm{ileum\_2}} &= 0.1 \cdot \mathrm{Vileum}_{2} \\[1ex]
\mathrm{Ventero}_{\mathrm{colon}} &= 0.1 \cdot \mathrm{Vcolon} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{duodenum}} &= v_{\mathrm{TALABS\_DUODENUM}} - v_{\mathrm{TALEFL\_DUODENUM}} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{jejunum\_1}} &= v_{\mathrm{TALABS\_JEJUNUM\_1}} - v_{\mathrm{TALEFL\_JEJUNUM\_1}} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{jejunum\_2}} &= v_{\mathrm{TALABS\_JEJUNUM\_2}} - v_{\mathrm{TALEFL\_JEJUNUM\_2}} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{ileum\_1}} &= v_{\mathrm{TALABS\_ILEUM\_1}} - v_{\mathrm{TALEFL\_ILEUM\_1}} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{ileum\_2}} &= v_{\mathrm{TALABS\_ILEUM\_2}} - v_{\mathrm{TALEFL\_ILEUM\_2}} \\[1ex]
\mathrm{TALUPTAKE}_{\mathrm{colon}} &= v_{\mathrm{TALABS\_COLON}} - v_{\mathrm{TALEFL\_COLON}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{TALABS\_DUODENUM}}$ | `TALABS_DUODENUM` | apical uptake talinolol duodenum | $\mathrm{tal}_{\mathrm{duodenum}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_duodenum}}$ |
| $v_{\mathrm{TALEFL\_DUODENUM}}$ | `TALEFL_DUODENUM` | efflux talinolol P-glycoprotein duodenum | $\mathrm{tal}_{\mathrm{entero\_duodenum}} \longrightarrow \mathrm{tal}_{\mathrm{duodenum}}$ |
| $v_{\mathrm{TALEX\_DUODENUM}}$ | `TALEX_DUODENUM` | talinolol basolateral transport duodenum | $\mathrm{tal}_{\mathrm{entero\_duodenum}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALABS\_JEJUNUM\_1}}$ | `TALABS_JEJUNUM_1` | apical uptake talinolol jejunum\_1 | $\mathrm{tal}_{\mathrm{jejunum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_jejunum\_1}}$ |
| $v_{\mathrm{TALEFL\_JEJUNUM\_1}}$ | `TALEFL_JEJUNUM_1` | efflux talinolol P-glycoprotein jejunum\_1 | $\mathrm{tal}_{\mathrm{entero\_jejunum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_1}}$ |
| $v_{\mathrm{TALEX\_JEJUNUM\_1}}$ | `TALEX_JEJUNUM_1` | talinolol basolateral transport jejunum\_1 | $\mathrm{tal}_{\mathrm{entero\_jejunum\_1}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALABS\_JEJUNUM\_2}}$ | `TALABS_JEJUNUM_2` | apical uptake talinolol jejunum\_2 | $\mathrm{tal}_{\mathrm{jejunum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_jejunum\_2}}$ |
| $v_{\mathrm{TALEFL\_JEJUNUM\_2}}$ | `TALEFL_JEJUNUM_2` | efflux talinolol P-glycoprotein jejunum\_2 | $\mathrm{tal}_{\mathrm{entero\_jejunum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_2}}$ |
| $v_{\mathrm{TALEX\_JEJUNUM\_2}}$ | `TALEX_JEJUNUM_2` | talinolol basolateral transport jejunum\_2 | $\mathrm{tal}_{\mathrm{entero\_jejunum\_2}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALABS\_ILEUM\_1}}$ | `TALABS_ILEUM_1` | apical uptake talinolol ileum\_1 | $\mathrm{tal}_{\mathrm{ileum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_ileum\_1}}$ |
| $v_{\mathrm{TALEFL\_ILEUM\_1}}$ | `TALEFL_ILEUM_1` | efflux talinolol P-glycoprotein ileum\_1 | $\mathrm{tal}_{\mathrm{entero\_ileum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{ileum\_1}}$ |
| $v_{\mathrm{TALEX\_ILEUM\_1}}$ | `TALEX_ILEUM_1` | talinolol basolateral transport ileum\_1 | $\mathrm{tal}_{\mathrm{entero\_ileum\_1}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALABS\_ILEUM\_2}}$ | `TALABS_ILEUM_2` | apical uptake talinolol ileum\_2 | $\mathrm{tal}_{\mathrm{ileum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_ileum\_2}}$ |
| $v_{\mathrm{TALEFL\_ILEUM\_2}}$ | `TALEFL_ILEUM_2` | efflux talinolol P-glycoprotein ileum\_2 | $\mathrm{tal}_{\mathrm{entero\_ileum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{ileum\_2}}$ |
| $v_{\mathrm{TALEX\_ILEUM\_2}}$ | `TALEX_ILEUM_2` | talinolol basolateral transport ileum\_2 | $\mathrm{tal}_{\mathrm{entero\_ileum\_2}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALABS\_COLON}}$ | `TALABS_COLON` | apical uptake talinolol colon | $\mathrm{tal}_{\mathrm{colon}} \longrightarrow \mathrm{tal}_{\mathrm{entero\_colon}}$ |
| $v_{\mathrm{TALEFL\_COLON}}$ | `TALEFL_COLON` | efflux talinolol P-glycoprotein colon | $\mathrm{tal}_{\mathrm{entero\_colon}} \longrightarrow \mathrm{tal}_{\mathrm{colon}}$ |
| $v_{\mathrm{TALEX\_COLON}}$ | `TALEX_COLON` | talinolol basolateral transport colon | $\mathrm{tal}_{\mathrm{entero\_colon}} \rightleftharpoons \mathrm{tal}_{\mathrm{ext}}$ |
| $v_{\mathrm{TALFLUX\_DUODENUM\_JEJUNUM\_1}}$ | `TALFLUX_DUODENUM_JEJUNUM_1` | talinolol transport duodenum to jejunum\_1 | $\mathrm{tal}_{\mathrm{duodenum}} \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_1}}$ |
| $v_{\mathrm{TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}}$ | `TALFLUX_JEJUNUM_1_JEJUNUM_2` | talinolol transport jejunum\_1 to jejunum\_2 | $\mathrm{tal}_{\mathrm{jejunum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_2}}$ |
| $v_{\mathrm{TALFLUX\_JEJUNUM\_2\_ILEUM\_1}}$ | `TALFLUX_JEJUNUM_2_ILEUM_1` | talinolol transport jejunum\_2 to ileum\_1 | $\mathrm{tal}_{\mathrm{jejunum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{ileum\_1}}$ |
| $v_{\mathrm{TALFLUX\_ILEUM\_1\_ILEUM\_2}}$ | `TALFLUX_ILEUM_1_ILEUM_2` | talinolol transport ileum\_1 to ileum\_2 | $\mathrm{tal}_{\mathrm{ileum\_1}} \longrightarrow \mathrm{tal}_{\mathrm{ileum\_2}}$ |
| $v_{\mathrm{TALFLUX\_ILEUM\_2\_COLON}}$ | `TALFLUX_ILEUM_2_COLON` | talinolol transport ileum\_2 to colon | $\mathrm{tal}_{\mathrm{ileum\_2}} \longrightarrow \mathrm{tal}_{\mathrm{colon}}$ |
| $v_{\mathrm{TALEXC}}$ | `TALEXC` | excretion talinolol (feces) | $\mathrm{tal}_{\mathrm{colon}} \longrightarrow \mathrm{tal}_{\mathrm{feces}}$ |
| $v_{\mathrm{TALINF\_duodenum}}$ | `TALINF_duodenum` | infusion talinolol (duodenum) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{duodenum}}$ |
| $v_{\mathrm{TALINF\_jejunum\_1}}$ | `TALINF_jejunum_1` | infusion talinolol (jejunum\_1) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_1}}$ |
| $v_{\mathrm{TALINF\_jejunum\_2}}$ | `TALINF_jejunum_2` | infusion talinolol (jejunum\_2) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{jejunum\_2}}$ |
| $v_{\mathrm{TALINF\_ileum\_1}}$ | `TALINF_ileum_1` | infusion talinolol (ileum\_1) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{ileum\_1}}$ |
| $v_{\mathrm{TALINF\_ileum\_2}}$ | `TALINF_ileum_2` | infusion talinolol (ileum\_2) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{ileum\_2}}$ |
| $v_{\mathrm{TALINF\_colon}}$ | `TALINF_colon` | infusion talinolol (colon) | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{colon}}$ |
| $v_{\mathrm{dissolution\_tal}}$ | `dissolution_tal` | dissolution talinolol | $\varnothing \longrightarrow \mathrm{tal}_{\mathrm{duodenum}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{TALABS\_DUODENUM}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{duodenum}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{duodenum}} \\[1ex]
v_{\mathrm{TALEFL\_DUODENUM}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{duodenum}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_duodenum}}}{\mathrm{tal}_{\mathrm{entero\_duodenum}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_DUODENUM}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_duodenum}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALABS\_JEJUNUM\_1}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{jejunum\_1}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{jejunum\_1}} \\[1ex]
v_{\mathrm{TALEFL\_JEJUNUM\_1}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{jejunum\_1}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_jejunum\_1}}}{\mathrm{tal}_{\mathrm{entero\_jejunum\_1}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_JEJUNUM\_1}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_jejunum\_1}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALABS\_JEJUNUM\_2}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{jejunum\_2}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{jejunum\_2}} \\[1ex]
v_{\mathrm{TALEFL\_JEJUNUM\_2}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{jejunum\_2}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_jejunum\_2}}}{\mathrm{tal}_{\mathrm{entero\_jejunum\_2}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_JEJUNUM\_2}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_jejunum\_2}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALABS\_ILEUM\_1}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{ileum\_1}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{ileum\_1}} \\[1ex]
v_{\mathrm{TALEFL\_ILEUM\_1}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{ileum\_1}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_ileum\_1}}}{\mathrm{tal}_{\mathrm{entero\_ileum\_1}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_ILEUM\_1}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_ileum\_1}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALABS\_ILEUM\_2}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{ileum\_2}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{ileum\_2}} \\[1ex]
v_{\mathrm{TALEFL\_ILEUM\_2}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{ileum\_2}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_ileum\_2}}}{\mathrm{tal}_{\mathrm{entero\_ileum\_2}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_ILEUM\_2}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_ileum\_2}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALABS\_COLON}} &= f_{\mathrm{oatp2b1}} \cdot \mathrm{oatp2b1}_{\mathrm{colon}} \cdot \mathrm{TALABS}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{colon}} \\[1ex]
v_{\mathrm{TALEFL\_COLON}} &= \frac{f_{\mathrm{pgp}} \cdot \mathrm{pgp}_{\mathrm{colon}} \cdot \mathrm{TALEFL}_{\mathrm{Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{tal}_{\mathrm{entero\_colon}}}{\mathrm{tal}_{\mathrm{entero\_colon}} + \mathrm{TALEFL}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{TALEX\_COLON}} &= \mathrm{TALEX}_{\mathrm{k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{tal}_{\mathrm{entero\_colon}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{tal}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{TALFLUX\_DUODENUM\_JEJUNUM\_1}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{DUODENUM\_k}} \cdot \mathrm{Vduodenum} \cdot \mathrm{tal}_{\mathrm{duodenum}} \\[1ex]
v_{\mathrm{TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{JEJUNUM\_1\_k}} \cdot \mathrm{Vjejunum}_{1} \cdot \mathrm{tal}_{\mathrm{jejunum\_1}} \\[1ex]
v_{\mathrm{TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{JEJUNUM\_2\_k}} \cdot \mathrm{Vjejunum}_{2} \cdot \mathrm{tal}_{\mathrm{jejunum\_2}} \\[1ex]
v_{\mathrm{TALFLUX\_ILEUM\_1\_ILEUM\_2}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{ILEUM\_1\_k}} \cdot \mathrm{Vileum}_{1} \cdot \mathrm{tal}_{\mathrm{ileum\_1}} \\[1ex]
v_{\mathrm{TALFLUX\_ILEUM\_2\_COLON}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{ILEUM\_2\_k}} \cdot \mathrm{Vileum}_{2} \cdot \mathrm{tal}_{\mathrm{ileum\_2}} \\[1ex]
v_{\mathrm{TALEXC}} &= f_{\mathrm{velocity}} \cdot \mathrm{TALFLUX}_{\mathrm{COLON\_k}} \cdot \mathrm{Vcolon} \cdot \mathrm{tal}_{\mathrm{colon}} \\[1ex]
v_{\mathrm{TALINF\_duodenum}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_duodenum}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{TALINF\_jejunum\_1}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_jejunum\_1}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{TALINF\_jejunum\_2}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_jejunum\_2}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{TALINF\_ileum\_1}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_ileum\_1}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{TALINF\_ileum\_2}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_ileum\_2}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{TALINF\_colon}} &= \frac{\mathrm{Ri}_{\mathrm{tal\_colon}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{dissolution\_tal}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_tal}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{tal}}}{\mathrm{Mr}_{\mathrm{tal}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vext}} \Bigl( v_{\mathrm{TALEX\_DUODENUM}} + v_{\mathrm{TALEX\_JEJUNUM\_1}} + v_{\mathrm{TALEX\_JEJUNUM\_2}} + v_{\mathrm{TALEX\_ILEUM\_1}} \\
&\quad {} + v_{\mathrm{TALEX\_ILEUM\_2}} + v_{\mathrm{TALEX\_COLON}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{TALEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{duodenum}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vduodenum}} \Bigl( -v_{\mathrm{TALABS\_DUODENUM}} + v_{\mathrm{TALEFL\_DUODENUM}} - v_{\mathrm{TALFLUX\_DUODENUM\_JEJUNUM\_1}} + v_{\mathrm{TALINF\_duodenum}} \\
&\quad {} + v_{\mathrm{dissolution\_tal}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_duodenum}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_DUODENUM}} - v_{\mathrm{TALEFL\_DUODENUM}} - v_{\mathrm{TALEX\_DUODENUM}}}{\mathrm{Ventero}_{\mathrm{duodenum}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{jejunum\_1}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vjejunum}_{1}} \Bigl( -v_{\mathrm{TALABS\_JEJUNUM\_1}} + v_{\mathrm{TALEFL\_JEJUNUM\_1}} + v_{\mathrm{TALFLUX\_DUODENUM\_JEJUNUM\_1}} - v_{\mathrm{TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} \\
&\quad {} + v_{\mathrm{TALINF\_jejunum\_1}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_jejunum\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_JEJUNUM\_1}} - v_{\mathrm{TALEFL\_JEJUNUM\_1}} - v_{\mathrm{TALEX\_JEJUNUM\_1}}}{\mathrm{Ventero}_{\mathrm{jejunum\_1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{jejunum\_2}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vjejunum}_{2}} \Bigl( -v_{\mathrm{TALABS\_JEJUNUM\_2}} + v_{\mathrm{TALEFL\_JEJUNUM\_2}} + v_{\mathrm{TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} - v_{\mathrm{TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} \\
&\quad {} + v_{\mathrm{TALINF\_jejunum\_2}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_jejunum\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_JEJUNUM\_2}} - v_{\mathrm{TALEFL\_JEJUNUM\_2}} - v_{\mathrm{TALEX\_JEJUNUM\_2}}}{\mathrm{Ventero}_{\mathrm{jejunum\_2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{ileum\_1}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vileum}_{1}} \Bigl( -v_{\mathrm{TALABS\_ILEUM\_1}} + v_{\mathrm{TALEFL\_ILEUM\_1}} + v_{\mathrm{TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} - v_{\mathrm{TALFLUX\_ILEUM\_1\_ILEUM\_2}} \\
&\quad {} + v_{\mathrm{TALINF\_ileum\_1}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_ileum\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_ILEUM\_1}} - v_{\mathrm{TALEFL\_ILEUM\_1}} - v_{\mathrm{TALEX\_ILEUM\_1}}}{\mathrm{Ventero}_{\mathrm{ileum\_1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{ileum\_2}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vileum}_{2}} \Bigl( -v_{\mathrm{TALABS\_ILEUM\_2}} + v_{\mathrm{TALEFL\_ILEUM\_2}} + v_{\mathrm{TALFLUX\_ILEUM\_1\_ILEUM\_2}} - v_{\mathrm{TALFLUX\_ILEUM\_2\_COLON}} \\
&\quad {} + v_{\mathrm{TALINF\_ileum\_2}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_ileum\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_ILEUM\_2}} - v_{\mathrm{TALEFL\_ILEUM\_2}} - v_{\mathrm{TALEX\_ILEUM\_2}}}{\mathrm{Ventero}_{\mathrm{ileum\_2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{colon}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vcolon}} \Bigl( -v_{\mathrm{TALABS\_COLON}} + v_{\mathrm{TALEFL\_COLON}} + v_{\mathrm{TALFLUX\_ILEUM\_2\_COLON}} - v_{\mathrm{TALEXC}} \\
&\quad {} + v_{\mathrm{TALINF\_colon}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{tal}_{\mathrm{entero\_colon}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TALABS\_COLON}} - v_{\mathrm{TALEFL\_COLON}} - v_{\mathrm{TALEX\_COLON}}}{\mathrm{Ventero}_{\mathrm{colon}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{tal}}}{\mathrm{d} t} &= -v_{\mathrm{dissolution\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \qquad \text{(rate rule)}
\end{aligned}
$$
