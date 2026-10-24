# Talinolol (TAL) body model

Model `talinolol_body`, SBML Level 3 Version 2, read from talinolol\_body\_flat.xml, written by sbmlode 0.3.0.

Talinolol (TAL) body model

Whole-body model of talinolol: the venous blood reaches the lung and the arterial blood, which perfuses the kidney, the gut, the liver and the rest of the body. Talinolol distributes into the tissues of the lung and of the rest of the body (ftissue\_tal, Kp\_tal), is excreted unchanged into the urine (kidney), the bile (liver) and the intestinal lumen (intestine, P-glycoprotein) and is not metabolized. The plasma concentration of talinolol is the one of the venous blood \[Cve\_tal\]; the blood volumes and flows carry the plasma concentration (blood to plasma ratio 1).

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
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{Vduodenum}$ | `Vduodenum` | small intestine duodenum D | $0.322563025707332$ | l |  |
| $\mathrm{LI}_{\mathrm{\_Vbaso}}$ | `LI__Vbaso` | basolateral membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vapical}}$ | `LI__Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vbi}}$ | `LI__Vbi` | bile | $1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ventero\_duodenum}}$ | `GU__Ventero_duodenum` | enterocytes small intestine duodenum D |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vjejunum\_1}}$ | `GU__Vjejunum_1` | small intestine jejunum J1 | $0.601183024172577$ | l |  |
| $\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_1}}$ | `GU__Ventero_jejunum_1` | enterocytes small intestine jejunum J1 |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vjejunum\_2}}$ | `GU__Vjejunum_2` | small intestine jejunum J2 | $0.601183024172577$ | l |  |
| $\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_2}}$ | `GU__Ventero_jejunum_2` | enterocytes small intestine jejunum J2 |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vileum\_1}}$ | `GU__Vileum_1` | small intestine ileum I1 | $0.944716180842621$ | l |  |
| $\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_1}}$ | `GU__Ventero_ileum_1` | enterocytes small intestine ileum I1 |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vileum\_2}}$ | `GU__Vileum_2` | small intestine ileum I2 | $0.944716180842621$ | l |  |
| $\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_2}}$ | `GU__Ventero_ileum_2` | enterocytes small intestine ileum I2 |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vcolon}}$ | `GU__Vcolon` | large intestine colon | $3.8170350741116$ | l |  |
| $\mathrm{GU}_{\mathrm{\_Ventero\_colon}}$ | `GU__Ventero_colon` | enterocytes large intestine colon |  | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cki}_{\mathrm{plasma\_tal}}$ | `Cki_plasma_tal` | talinolol (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_tal}}$ | `Cli_plasma_tal` | talinolol (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_tal}}$ | `Clu_plasma_tal` | talinolol (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_tal}}$ | `Cgu_plasma_tal` | talinolol (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_tal}}$ | `Cre_plasma_tal` | talinolol (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{tal}}$ | `Car_tal` | talinolol (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{tal}}$ | `Cve_tal` | talinolol (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{tal}}$ | `Cpo_tal` | talinolol (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{tal}}$ | `Chv_tal` | talinolol (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{tal}}$ | `Clu_tal` | talinolol (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{tal}}$ | `Cre_tal` | talinolol (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{tal}}$ | `Aurine_tal` | talinolol (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{tal}}$ | `Afeces_tal` | talinolol (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cduodenum}_{\mathrm{tal}}$ | `Cduodenum_tal` | talinolol (duodenum) | $\mathrm{Vduodenum}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_tal}}$ | `LI__tal` | talinolol (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_tal\_bi}}$ | `LI__tal_bi` | talinolol (bile) | $\mathrm{LI}_{\mathrm{\_Vbi}}$ |  | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}}$ | `GU__tal_entero_duodenum` | talinolol enterocytes (small intestine duodenum D) | $\mathrm{GU}_{\mathrm{\_Ventero\_duodenum}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}}$ | `GU__tal_jejunum_1` | talinolol (small intestine jejunum J1) | $\mathrm{GU}_{\mathrm{\_Vjejunum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}}$ | `GU__tal_entero_jejunum_1` | talinolol enterocytes (small intestine jejunum J1) | $\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}}$ | `GU__tal_jejunum_2` | talinolol (small intestine jejunum J2) | $\mathrm{GU}_{\mathrm{\_Vjejunum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}}$ | `GU__tal_entero_jejunum_2` | talinolol enterocytes (small intestine jejunum J2) | $\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_ileum\_1}}$ | `GU__tal_ileum_1` | talinolol (small intestine ileum I1) | $\mathrm{GU}_{\mathrm{\_Vileum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}}$ | `GU__tal_entero_ileum_1` | talinolol enterocytes (small intestine ileum I1) | $\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_ileum\_2}}$ | `GU__tal_ileum_2` | talinolol (small intestine ileum I2) | $\mathrm{GU}_{\mathrm{\_Vileum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}}$ | `GU__tal_entero_ileum_2` | talinolol enterocytes (small intestine ileum I2) | $\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_colon}}$ | `GU__tal_colon` | talinolol (large intestine colon) | $\mathrm{GU}_{\mathrm{\_Vcolon}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}}$ | `GU__tal_entero_colon` | talinolol enterocytes (large intestine colon) | $\mathrm{GU}_{\mathrm{\_Ventero\_colon}}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.548$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[l/min\] |  | l/min |  |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- |  |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $\mathrm{PODOSE}_{\mathrm{tal}}$ | `PODOSE_tal` | oral dose tal \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_tal}}$ | `Ka_dis_tal` | Ka\_dis \[1/hr\] dissolution tal | $1.40676555809381$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{tal}}$ | `Mr_tal` | Molecular weight tal \[g/mole\] | $363.495$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{tal}}$ | `fup_tal` | fraction unbound in plasma tal | $0.4$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{tal}}$ | `ftissue_tal` | tissue distribution tal | $2.75911585140351$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{tal}}$ | `Kp_tal` | tissue/plasma partition coefficient tal | $3.91659764067487$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{tal}}$ | `IVDOSE_tal` | IV bolus dose tal \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{tal}}$ | `ti_tal` | injection time tal \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{tal}}$ | `Ki_tal` | Ki \[1/min\] injection tal |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{tal}}$ | `Ri_tal` | Ri \[mg/min\] rate of infusion tal | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_tal}}$ | `cum_dose_tal` | Cumulative dose due to infusion tal | $0$ | mg |  |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{Aki}_{\mathrm{plasma\_tal}}$ | `Aki_plasma_tal` | talinolol amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_tal}}$ | `Xki_plasma_tal` | talinolol amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_tal}}$ | `Mki_plasma_tal` | talinolol concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_tal}}$ | `Ali_plasma_tal` | talinolol amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_tal}}$ | `Xli_plasma_tal` | talinolol amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_tal}}$ | `Mli_plasma_tal` | talinolol concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_tal}}$ | `Alu_plasma_tal` | talinolol amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_tal}}$ | `Xlu_plasma_tal` | talinolol amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_tal}}$ | `Mlu_plasma_tal` | talinolol concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_tal}}$ | `Agu_plasma_tal` | talinolol amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_tal}}$ | `Xgu_plasma_tal` | talinolol amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_tal}}$ | `Mgu_plasma_tal` | talinolol concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_tal}}$ | `Are_plasma_tal` | talinolol amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_tal}}$ | `Xre_plasma_tal` | talinolol amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_tal}}$ | `Mre_plasma_tal` | talinolol concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{tal}}$ | `Aar_tal` | talinolol amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{tal}}$ | `Xar_tal` | talinolol amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{tal}}$ | `Mar_tal` | talinolol concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{tal}}$ | `Ave_tal` | talinolol amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{tal}}$ | `Xve_tal` | talinolol amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{tal}}$ | `Mve_tal` | talinolol concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{tal}}$ | `Apo_tal` | talinolol amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{tal}}$ | `Xpo_tal` | talinolol amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{tal}}$ | `Mpo_tal` | talinolol concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{tal}}$ | `Ahv_tal` | talinolol amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{tal}}$ | `Xhv_tal` | talinolol amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{tal}}$ | `Mhv_tal` | talinolol concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{tal}}$ | `Xurine_tal` | talinolol amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Xfeces}_{\mathrm{tal}}$ | `Xfeces_tal` | talinolol amount (feces) |  | mg |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR\_base}}$ | `KI__GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_TALEX\_f}}$ | `KI__TALEX_f` | renal clearance of unbound talinolol relative to the GFR | $7.66469242599538$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{LI}_{\mathrm{\_Abile\_tal}}$ | `LI__Abile_tal` | cumulative talinolol (bile) | $0$ | mmol |  |
| $\mathrm{LI}_{\mathrm{\_bile\_flow}}$ | `LI__bile_flow` | bile flow | $0.000766666666666667$ | l/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_Cbile\_tal}}$ | `LI__Cbile_tal` | talinolol (bile) |  | mmol/l |  |
| $\mathrm{LI}_{\mathrm{\_TALIM\_Vmax}}$ | `LI__TALIM_Vmax` | Vmax for talinolol import | $0.0369201073419107$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_TALIM\_Km\_tal}}$ | `LI__TALIM_Km_tal` | Km for talinolol import | $0.301$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_oatp1b1}}$ | `LI__f_oatp1b1` | activity of OATP1B1 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_TALEX\_k}}$ | `LI__TALEX_k` | rate for talinolol export in bile | $0.15$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_pgp}}$ | `LI__f_pgp` | activity of P-glycoprotein (liver) | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_EHC}}$ | `LI__f_EHC` | factor for modifying EHC | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALABS\_k}}$ | `GU__TALABS_k` | rate of the apical uptake of talinolol | $0.00358298645106167$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}}$ | `GU__TALEFL_Vmax` | Vmax of the efflux of talinolol by P-glycoprotein | $0.000103428146343818$ | mmol/min/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALEFL\_Km}}$ | `GU__TALEFL_Km` | Km of the efflux of talinolol by P-glycoprotein | $0.000240407546909154$ | mmol/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALEX\_k}}$ | `GU__TALEX_k` | rate of the basolateral transport of talinolol | $0.35$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_velocity}}$ | `GU__f_velocity` | parameter for velocity intestinal transport | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_oatp2b1}}$ | `GU__f_oatp2b1` | activity of the apical uptake (OATP2B1) | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_pgp}}$ | `GU__f_pgp` | activity of P-glycoprotein (intestine) | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_duodenum}}$ | `GU__pgp_duodenum` | protein amount P-gp | $0.3$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_duodenum}}$ | `GU__oatp2b1_duodenum` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_jejunum\_1}}$ | `GU__pgp_jejunum_1` | protein amount P-gp | $0.4$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_jejunum\_1}}$ | `GU__oatp2b1_jejunum_1` | protein amount OATP2B1 | $0.5$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_jejunum\_2}}$ | `GU__pgp_jejunum_2` | protein amount P-gp | $0.5$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_jejunum\_2}}$ | `GU__oatp2b1_jejunum_2` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_ileum\_1}}$ | `GU__pgp_ileum_1` | protein amount P-gp | $0.7$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_ileum\_1}}$ | `GU__oatp2b1_ileum_1` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_ileum\_2}}$ | `GU__pgp_ileum_2` | protein amount P-gp | $1.1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_ileum\_2}}$ | `GU__oatp2b1_ileum_2` | protein amount OATP2B1 | $0.45$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_pgp\_colon}}$ | `GU__pgp_colon` | protein amount P-gp | $0.25$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_oatp2b1\_colon}}$ | `GU__oatp2b1_colon` | protein amount OATP2B1 | $0.5$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_duodenum}}$ | `GU__Ri_tal_duodenum` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_jejunum\_1}}$ | `GU__Ri_tal_jejunum_1` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_jejunum\_2}}$ | `GU__Ri_tal_jejunum_2` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_ileum\_1}}$ | `GU__Ri_tal_ileum_1` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_ileum\_2}}$ | `GU__Ri_tal_ileum_2` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ri\_tal\_colon}}$ | `GU__Ri_tal_colon` | Ri \[mg/min\] rate of infusion intestine talinolol | $0$ | mg/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_DUODENUM\_k}}$ | `GU__TALFLUX_DUODENUM_k` | Transport rate duodenum | $0.0666666666666667$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_JEJUNUM\_1\_k}}$ | `GU__TALFLUX_JEJUNUM_1_k` | Transport rate jejunum\_1 | $0.019047619047619$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_JEJUNUM\_2\_k}}$ | `GU__TALFLUX_JEJUNUM_2_k` | Transport rate jejunum\_2 | $0.019047619047619$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_ILEUM\_1\_k}}$ | `GU__TALFLUX_ILEUM_1_k` | Transport rate ileum\_1 | $0.0121212121212121$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_ILEUM\_2\_k}}$ | `GU__TALFLUX_ILEUM_2_k` | Transport rate ileum\_2 | $0.0121212121212121$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALFLUX\_COLON\_k}}$ | `GU__TALFLUX_COLON_k` | Transport rate colon | $0.000740740740740741$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_duodenum}}$ | `GU__TALUPTAKE_duodenum` | net uptake talinolol duodenum |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_jejunum\_1}}$ | `GU__TALUPTAKE_jejunum_1` | net uptake talinolol jejunum\_1 |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_jejunum\_2}}$ | `GU__TALUPTAKE_jejunum_2` | net uptake talinolol jejunum\_2 |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_ileum\_1}}$ | `GU__TALUPTAKE_ileum_1` | net uptake talinolol ileum\_1 |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_ileum\_2}}$ | `GU__TALUPTAKE_ileum_2` | net uptake talinolol ileum\_2 |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_TALUPTAKE\_colon}}$ | `GU__TALUPTAKE_colon` | net uptake talinolol colon |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Aurine}_{\mathrm{tal}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{tal}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{LI}_{\mathrm{\_tal\_bi}} &= 0 \cdot \mathrm{LI}_{\mathrm{\_Vbi}}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot \mathrm{COBW} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right) \\[1ex]
\mathrm{Vhv} &= \mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{tal}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{tal}}} \cdot 60 \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_tal}} &= \mathrm{Cki}_{\mathrm{plasma\_tal}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_tal}} &= \mathrm{Aki}_{\mathrm{plasma\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_tal}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_tal}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_tal}} &= \mathrm{Cli}_{\mathrm{plasma\_tal}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_tal}} &= \mathrm{Ali}_{\mathrm{plasma\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_tal}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_tal}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_tal}} &= \mathrm{Clu}_{\mathrm{plasma\_tal}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_tal}} &= \mathrm{Alu}_{\mathrm{plasma\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_tal}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_tal}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_tal}} &= \mathrm{Cgu}_{\mathrm{plasma\_tal}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_tal}} &= \mathrm{Agu}_{\mathrm{plasma\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_tal}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_tal}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_tal}} &= \mathrm{Cre}_{\mathrm{plasma\_tal}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_tal}} &= \mathrm{Are}_{\mathrm{plasma\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_tal}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_tal}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Aar}_{\mathrm{tal}} &= \mathrm{Car}_{\mathrm{tal}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{tal}} &= \mathrm{Aar}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mar}_{\mathrm{tal}} &= \frac{\mathrm{Aar}_{\mathrm{tal}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Ave}_{\mathrm{tal}} &= \mathrm{Cve}_{\mathrm{tal}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{tal}} &= \mathrm{Ave}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mve}_{\mathrm{tal}} &= \frac{\mathrm{Ave}_{\mathrm{tal}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Apo}_{\mathrm{tal}} &= \mathrm{Cpo}_{\mathrm{tal}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{tal}} &= \mathrm{Apo}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mpo}_{\mathrm{tal}} &= \frac{\mathrm{Apo}_{\mathrm{tal}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Ahv}_{\mathrm{tal}} &= \mathrm{Chv}_{\mathrm{tal}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{tal}} &= \mathrm{Ahv}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Mhv}_{\mathrm{tal}} &= \frac{\mathrm{Ahv}_{\mathrm{tal}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Xurine}_{\mathrm{tal}} &= \mathrm{Aurine}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{tal}} &= \mathrm{Afeces}_{\mathrm{tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{KI}_{\mathrm{\_GFR\_base}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_duodenum}} &= 0.1 \cdot \mathrm{Vduodenum} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_1}} &= 0.1 \cdot \mathrm{GU}_{\mathrm{\_Vjejunum\_1}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_2}} &= 0.1 \cdot \mathrm{GU}_{\mathrm{\_Vjejunum\_2}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_1}} &= 0.1 \cdot \mathrm{GU}_{\mathrm{\_Vileum\_1}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_2}} &= 0.1 \cdot \mathrm{GU}_{\mathrm{\_Vileum\_2}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Ventero\_colon}} &= 0.1 \cdot \mathrm{GU}_{\mathrm{\_Vcolon}} \\[1ex]
\mathrm{LI}_{\mathrm{\_Cbile\_tal}} &= \frac{v_{\mathrm{LI\_\_TALEX}}}{\mathrm{LI}_{\mathrm{\_bile\_flow}}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_duodenum}} &= v_{\mathrm{GU\_\_TALABS\_DUODENUM}} - v_{\mathrm{GU\_\_TALEFL\_DUODENUM}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_jejunum\_1}} &= v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_1}} - v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_1}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_jejunum\_2}} &= v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_2}} - v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_2}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_ileum\_1}} &= v_{\mathrm{GU\_\_TALABS\_ILEUM\_1}} - v_{\mathrm{GU\_\_TALEFL\_ILEUM\_1}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_ileum\_2}} &= v_{\mathrm{GU\_\_TALABS\_ILEUM\_2}} - v_{\mathrm{GU\_\_TALEFL\_ILEUM\_2}} \\[1ex]
\mathrm{GU}_{\mathrm{\_TALUPTAKE\_colon}} &= v_{\mathrm{GU\_\_TALABS\_COLON}} - v_{\mathrm{GU\_\_TALEFL\_COLON}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{transport\_lu\_tal}}$ | `transport_lu_tal` | transport talinolol | $\mathrm{Clu}_{\mathrm{plasma\_tal}} \rightleftharpoons \mathrm{Clu}_{\mathrm{tal}}$ |
| $v_{\mathrm{transport\_re\_tal}}$ | `transport_re_tal` | transport talinolol | $\mathrm{Cre}_{\mathrm{plasma\_tal}} \rightleftharpoons \mathrm{Cre}_{\mathrm{tal}}$ |
| $v_{\mathrm{iv\_tal}}$ | `iv_tal` | iv talinolol | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_tal}}$ | `Flow_ar_ki_tal` | inflow kidney talinolol | $\mathrm{Car}_{\mathrm{tal}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_tal}}$ | `Flow_ki_ve_tal` | outflow kidney talinolol | $\mathrm{Cki}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Cve}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_arli\_li\_tal}}$ | `Flow_arli_li_tal` | arterial inflow liver talinolol | $\mathrm{Car}_{\mathrm{tal}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_arli\_hv\_tal}}$ | `Flow_arli_hv_tal` | flow arterial shunts | $\mathrm{Car}_{\mathrm{tal}} \longrightarrow \mathrm{Chv}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_po\_li\_tal}}$ | `Flow_po_li_tal` | outflow po talinolol | $\mathrm{Cpo}_{\mathrm{tal}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_po\_hv\_tal}}$ | `Flow_po_hv_tal` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{tal}} \longrightarrow \mathrm{Chv}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_li\_hv\_tal}}$ | `Flow_li_hv_tal` | outflow liver talinolol | $\mathrm{Cli}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Chv}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_tal}}$ | `Flow_hv_ve_tal` | outflow hepatic vein talinolol | $\mathrm{Chv}_{\mathrm{tal}} \longrightarrow \mathrm{Cve}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_tal}}$ | `Flow_ve_lu_tal` | inflow lung talinolol | $\mathrm{Cve}_{\mathrm{tal}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_tal}}$ | `Flow_lu_ar_tal` | outflow lung talinolol | $\mathrm{Clu}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Car}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_tal}}$ | `Flow_ar_gu_tal` | inflow gut talinolol | $\mathrm{Car}_{\mathrm{tal}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_gu\_po\_tal}}$ | `Flow_gu_po_tal` | outflow gut talinolol | $\mathrm{Cgu}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Cpo}_{\mathrm{tal}}$ |
| $v_{\mathrm{Flow\_ar\_re\_tal}}$ | `Flow_ar_re_tal` | inflow rest talinolol | $\mathrm{Car}_{\mathrm{tal}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{Flow\_re\_ve\_tal}}$ | `Flow_re_ve_tal` | outflow rest talinolol | $\mathrm{Cre}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Cve}_{\mathrm{tal}}$ |
| $v_{\mathrm{KI\_\_TALEX}}$ | `KI__TALEX` | excretion talinolol | $\mathrm{Cki}_{\mathrm{plasma\_tal}} \longrightarrow \mathrm{Aurine}_{\mathrm{tal}}$ |
| $v_{\mathrm{LI\_\_TALIM}}$ | `LI__TALIM` | talinolol import | $\mathrm{Cli}_{\mathrm{plasma\_tal}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_tal}}$ |
| $v_{\mathrm{LI\_\_TALEX}}$ | `LI__TALEX` | talinolol bile export | $\mathrm{LI}_{\mathrm{\_tal}} \longrightarrow \mathrm{LI}_{\mathrm{\_tal\_bi}}$ |
| $v_{\mathrm{LI\_\_TALEHC}}$ | `LI__TALEHC` | talinolol enterohepatic circulation | $\mathrm{LI}_{\mathrm{\_tal\_bi}} \longrightarrow \mathrm{Cduodenum}_{\mathrm{tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_DUODENUM}}$ | `GU__TALABS_DUODENUM` | apical uptake talinolol duodenum | $\mathrm{Cduodenum}_{\mathrm{tal}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_DUODENUM}}$ | `GU__TALEFL_DUODENUM` | efflux talinolol P-glycoprotein duodenum | $\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}} \longrightarrow \mathrm{Cduodenum}_{\mathrm{tal}}$ |
| $v_{\mathrm{GU\_\_TALEX\_DUODENUM}}$ | `GU__TALEX_DUODENUM` | talinolol basolateral transport duodenum | $\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_1}}$ | `GU__TALABS_JEJUNUM_1` | apical uptake talinolol jejunum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_1}}$ | `GU__TALEFL_JEJUNUM_1` | efflux talinolol P-glycoprotein jejunum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}}$ |
| $v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_1}}$ | `GU__TALEX_JEJUNUM_1` | talinolol basolateral transport jejunum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_2}}$ | `GU__TALABS_JEJUNUM_2` | apical uptake talinolol jejunum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_2}}$ | `GU__TALEFL_JEJUNUM_2` | efflux talinolol P-glycoprotein jejunum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}}$ |
| $v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_2}}$ | `GU__TALEX_JEJUNUM_2` | talinolol basolateral transport jejunum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_ILEUM\_1}}$ | `GU__TALABS_ILEUM_1` | apical uptake talinolol ileum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_ileum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_ILEUM\_1}}$ | `GU__TALEFL_ILEUM_1` | efflux talinolol P-glycoprotein ileum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_1}}$ |
| $v_{\mathrm{GU\_\_TALEX\_ILEUM\_1}}$ | `GU__TALEX_ILEUM_1` | talinolol basolateral transport ileum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_ILEUM\_2}}$ | `GU__TALABS_ILEUM_2` | apical uptake talinolol ileum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_ileum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_ILEUM\_2}}$ | `GU__TALEFL_ILEUM_2` | efflux talinolol P-glycoprotein ileum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_2}}$ |
| $v_{\mathrm{GU\_\_TALEX\_ILEUM\_2}}$ | `GU__TALEX_ILEUM_2` | talinolol basolateral transport ileum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALABS\_COLON}}$ | `GU__TALABS_COLON` | apical uptake talinolol colon | $\mathrm{GU}_{\mathrm{\_tal\_colon}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_entero\_colon}}$ |
| $v_{\mathrm{GU\_\_TALEFL\_COLON}}$ | `GU__TALEFL_COLON` | efflux talinolol P-glycoprotein colon | $\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_colon}}$ |
| $v_{\mathrm{GU\_\_TALEX\_COLON}}$ | `GU__TALEX_COLON` | talinolol basolateral transport colon | $\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}} \rightleftharpoons \mathrm{Cgu}_{\mathrm{plasma\_tal}}$ |
| $v_{\mathrm{GU\_\_TALFLUX\_DUODENUM\_JEJUNUM\_1}}$ | `GU__TALFLUX_DUODENUM_JEJUNUM_1` | talinolol transport duodenum to jejunum\_1 | $\mathrm{Cduodenum}_{\mathrm{tal}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}}$ |
| $v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}}$ | `GU__TALFLUX_JEJUNUM_1_JEJUNUM_2` | talinolol transport jejunum\_1 to jejunum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}}$ |
| $v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_2\_ILEUM\_1}}$ | `GU__TALFLUX_JEJUNUM_2_ILEUM_1` | talinolol transport jejunum\_2 to ileum\_1 | $\mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_1}}$ |
| $v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_1\_ILEUM\_2}}$ | `GU__TALFLUX_ILEUM_1_ILEUM_2` | talinolol transport ileum\_1 to ileum\_2 | $\mathrm{GU}_{\mathrm{\_tal\_ileum\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_2}}$ |
| $v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_2\_COLON}}$ | `GU__TALFLUX_ILEUM_2_COLON` | talinolol transport ileum\_2 to colon | $\mathrm{GU}_{\mathrm{\_tal\_ileum\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_colon}}$ |
| $v_{\mathrm{GU\_\_TALEXC}}$ | `GU__TALEXC` | excretion talinolol (feces) | $\mathrm{GU}_{\mathrm{\_tal\_colon}} \longrightarrow \mathrm{Afeces}_{\mathrm{tal}}$ |
| $v_{\mathrm{GU\_\_TALINF\_duodenum}}$ | `GU__TALINF_duodenum` | infusion talinolol (duodenum) | $\varnothing \longrightarrow \mathrm{Cduodenum}_{\mathrm{tal}}$ |
| $v_{\mathrm{GU\_\_TALINF\_jejunum\_1}}$ | `GU__TALINF_jejunum_1` | infusion talinolol (jejunum\_1) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}}$ |
| $v_{\mathrm{GU\_\_TALINF\_jejunum\_2}}$ | `GU__TALINF_jejunum_2` | infusion talinolol (jejunum\_2) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}}$ |
| $v_{\mathrm{GU\_\_TALINF\_ileum\_1}}$ | `GU__TALINF_ileum_1` | infusion talinolol (ileum\_1) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_1}}$ |
| $v_{\mathrm{GU\_\_TALINF\_ileum\_2}}$ | `GU__TALINF_ileum_2` | infusion talinolol (ileum\_2) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_ileum\_2}}$ |
| $v_{\mathrm{GU\_\_TALINF\_colon}}$ | `GU__TALINF_colon` | infusion talinolol (colon) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_tal\_colon}}$ |
| $v_{\mathrm{GU\_\_dissolution\_tal}}$ | `GU__dissolution_tal` | dissolution talinolol | $\varnothing \longrightarrow \mathrm{Cduodenum}_{\mathrm{tal}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_lu\_tal}} &= \frac{\mathrm{ftissue}_{\mathrm{tal}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_tal}} \cdot \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Kp}_{\mathrm{tal}} - \mathrm{Clu}_{\mathrm{tal}}\right) \\[1ex]
v_{\mathrm{transport\_re\_tal}} &= \frac{\mathrm{ftissue}_{\mathrm{tal}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_tal}} \cdot \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Kp}_{\mathrm{tal}} - \mathrm{Cre}_{\mathrm{tal}}\right) \\[1ex]
v_{\mathrm{iv\_tal}} &= \frac{\mathrm{Ki}_{\mathrm{tal}} \cdot \mathrm{IVDOSE}_{\mathrm{tal}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_tal}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_tal}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_tal}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_tal}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_tal}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_tal}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_tal}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_tal}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_tal}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_tal}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_tal}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_tal}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_tal}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_tal}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{KI\_\_TALEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{KI}_{\mathrm{\_TALEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_tal}} \\[1ex]
v_{\mathrm{LI\_\_TALIM}} &= \frac{\frac{\mathrm{LI}_{\mathrm{\_f\_oatp1b1}} \cdot \mathrm{LI}_{\mathrm{\_TALIM\_Vmax}}}{\mathrm{LI}_{\mathrm{\_TALIM\_Km\_tal}}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cli}_{\mathrm{plasma\_tal}} - \mathrm{LI}_{\mathrm{\_tal}}\right)}{1 + \frac{\mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cli}_{\mathrm{plasma\_tal}}}{\mathrm{LI}_{\mathrm{\_TALIM\_Km\_tal}}} + \frac{\mathrm{LI}_{\mathrm{\_tal}}}{\mathrm{LI}_{\mathrm{\_TALIM\_Km\_tal}}}} \\[1ex]
v_{\mathrm{LI\_\_TALEX}} &= \mathrm{LI}_{\mathrm{\_f\_pgp}} \cdot \mathrm{LI}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_tal}} \\[1ex]
v_{\mathrm{LI\_\_TALEHC}} &= \mathrm{LI}_{\mathrm{\_f\_EHC}} \cdot v_{\mathrm{LI\_\_TALEX}} \\[1ex]
v_{\mathrm{GU\_\_TALABS\_DUODENUM}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_duodenum}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{Cduodenum}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_DUODENUM}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_duodenum}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_DUODENUM}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_1}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_jejunum\_1}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_1}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_jejunum\_1}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_1}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_2}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_jejunum\_2}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_2}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_jejunum\_2}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_2}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALABS\_ILEUM\_1}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_ileum\_1}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_ileum\_1}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_ILEUM\_1}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_ileum\_1}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_ILEUM\_1}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALABS\_ILEUM\_2}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_ileum\_2}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_ileum\_2}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_ILEUM\_2}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_ileum\_2}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_ILEUM\_2}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALABS\_COLON}} &= \mathrm{GU}_{\mathrm{\_f\_oatp2b1}} \cdot \mathrm{GU}_{\mathrm{\_oatp2b1\_colon}} \cdot \mathrm{GU}_{\mathrm{\_TALABS\_k}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_colon}} \\[1ex]
v_{\mathrm{GU\_\_TALEFL\_COLON}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_pgp}} \cdot \mathrm{GU}_{\mathrm{\_pgp\_colon}} \cdot \mathrm{GU}_{\mathrm{\_TALEFL\_Vmax}} \cdot \mathrm{Vgu} \cdot \mathrm{GU}_{\mathrm{\_tal\_entero\_colon}}}{\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}} + \mathrm{GU}_{\mathrm{\_TALEFL\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_TALEX\_COLON}} &= \mathrm{GU}_{\mathrm{\_TALEX\_k}} \cdot \mathrm{Vgu} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}} - \mathrm{fup}_{\mathrm{tal}} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tal}}\right) \\[1ex]
v_{\mathrm{GU\_\_TALFLUX\_DUODENUM\_JEJUNUM\_1}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_DUODENUM\_k}} \cdot \mathrm{Vduodenum} \cdot \mathrm{Cduodenum}_{\mathrm{tal}} \\[1ex]
v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_JEJUNUM\_1\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vjejunum\_1}} \cdot \mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}} \\[1ex]
v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_JEJUNUM\_2\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vjejunum\_2}} \cdot \mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}} \\[1ex]
v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_1\_ILEUM\_2}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_ILEUM\_1\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vileum\_1}} \cdot \mathrm{GU}_{\mathrm{\_tal\_ileum\_1}} \\[1ex]
v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_2\_COLON}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_ILEUM\_2\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vileum\_2}} \cdot \mathrm{GU}_{\mathrm{\_tal\_ileum\_2}} \\[1ex]
v_{\mathrm{GU\_\_TALEXC}} &= \mathrm{GU}_{\mathrm{\_f\_velocity}} \cdot \mathrm{GU}_{\mathrm{\_TALFLUX\_COLON\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vcolon}} \cdot \mathrm{GU}_{\mathrm{\_tal\_colon}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_duodenum}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_duodenum}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_jejunum\_1}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_jejunum\_1}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_jejunum\_2}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_jejunum\_2}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_ileum\_1}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_ileum\_1}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_ileum\_2}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_ileum\_2}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_TALINF\_colon}} &= \frac{\mathrm{GU}_{\mathrm{\_Ri\_tal\_colon}}}{\mathrm{Mr}_{\mathrm{tal}}} \\[1ex]
v_{\mathrm{GU\_\_dissolution\_tal}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_tal}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{tal}}}{\mathrm{Mr}_{\mathrm{tal}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_tal}} - v_{\mathrm{Flow\_ki\_ve\_tal}} - v_{\mathrm{KI\_\_TALEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_tal}} + v_{\mathrm{Flow\_po\_li\_tal}} - v_{\mathrm{Flow\_li\_hv\_tal}} - v_{\mathrm{LI\_\_TALIM}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_tal}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_tal}} + v_{\mathrm{Flow\_ve\_lu\_tal}} - v_{\mathrm{Flow\_lu\_ar\_tal}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_tal}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vgu}_{\mathrm{plasma}}} \Bigl( v_{\mathrm{Flow\_ar\_gu\_tal}} - v_{\mathrm{Flow\_gu\_po\_tal}} + v_{\mathrm{GU\_\_TALEX\_DUODENUM}} + v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_1}} \\
&\quad {} + v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_2}} + v_{\mathrm{GU\_\_TALEX\_ILEUM\_1}} + v_{\mathrm{GU\_\_TALEX\_ILEUM\_2}} + v_{\mathrm{GU\_\_TALEX\_COLON}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_tal}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_tal}} + v_{\mathrm{Flow\_ar\_re\_tal}} - v_{\mathrm{Flow\_re\_ve\_tal}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_tal}} - v_{\mathrm{Flow\_arli\_li\_tal}} - v_{\mathrm{Flow\_arli\_hv\_tal}} + v_{\mathrm{Flow\_lu\_ar\_tal}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_tal}} - v_{\mathrm{Flow\_ar\_re\_tal}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_tal}} + v_{\mathrm{Flow\_ki\_ve\_tal}} + v_{\mathrm{Flow\_hv\_ve\_tal}} - v_{\mathrm{Flow\_ve\_lu\_tal}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_tal}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_tal}} - v_{\mathrm{Flow\_po\_hv\_tal}} + v_{\mathrm{Flow\_gu\_po\_tal}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_tal}} + v_{\mathrm{Flow\_po\_hv\_tal}} + v_{\mathrm{Flow\_li\_hv\_tal}} - v_{\mathrm{Flow\_hv\_ve\_tal}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_tal}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_tal}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{tal}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_TALEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{tal}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_TALEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cduodenum}_{\mathrm{tal}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vduodenum}} \Bigl( v_{\mathrm{LI\_\_TALEHC}} - v_{\mathrm{GU\_\_TALABS\_DUODENUM}} + v_{\mathrm{GU\_\_TALEFL\_DUODENUM}} - v_{\mathrm{GU\_\_TALFLUX\_DUODENUM\_JEJUNUM\_1}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_duodenum}} + v_{\mathrm{GU\_\_dissolution\_tal}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_tal}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_TALIM}} - v_{\mathrm{LI\_\_TALEX}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_tal\_bi}}}{\mathrm{d} t} &= v_{\mathrm{LI\_\_TALEX}} - v_{\mathrm{LI\_\_TALEHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_duodenum}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_DUODENUM}} - v_{\mathrm{GU\_\_TALEFL\_DUODENUM}} - v_{\mathrm{GU\_\_TALEX\_DUODENUM}}}{\mathrm{GU}_{\mathrm{\_Ventero\_duodenum}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_jejunum\_1}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vjejunum\_1}}} \Bigl( -v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_1}} + v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_1}} + v_{\mathrm{GU\_\_TALFLUX\_DUODENUM\_JEJUNUM\_1}} - v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_jejunum\_1}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_1}} - v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_1}} - v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_1}}}{\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_jejunum\_2}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vjejunum\_2}}} \Bigl( -v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_2}} + v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_2}} + v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_1\_JEJUNUM\_2}} - v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_jejunum\_2}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_jejunum\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_JEJUNUM\_2}} - v_{\mathrm{GU\_\_TALEFL\_JEJUNUM\_2}} - v_{\mathrm{GU\_\_TALEX\_JEJUNUM\_2}}}{\mathrm{GU}_{\mathrm{\_Ventero\_jejunum\_2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_ileum\_1}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vileum\_1}}} \Bigl( -v_{\mathrm{GU\_\_TALABS\_ILEUM\_1}} + v_{\mathrm{GU\_\_TALEFL\_ILEUM\_1}} + v_{\mathrm{GU\_\_TALFLUX\_JEJUNUM\_2\_ILEUM\_1}} - v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_1\_ILEUM\_2}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_ileum\_1}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_ILEUM\_1}} - v_{\mathrm{GU\_\_TALEFL\_ILEUM\_1}} - v_{\mathrm{GU\_\_TALEX\_ILEUM\_1}}}{\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_ileum\_2}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vileum\_2}}} \Bigl( -v_{\mathrm{GU\_\_TALABS\_ILEUM\_2}} + v_{\mathrm{GU\_\_TALEFL\_ILEUM\_2}} + v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_1\_ILEUM\_2}} - v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_2\_COLON}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_ileum\_2}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_ileum\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_ILEUM\_2}} - v_{\mathrm{GU\_\_TALEFL\_ILEUM\_2}} - v_{\mathrm{GU\_\_TALEX\_ILEUM\_2}}}{\mathrm{GU}_{\mathrm{\_Ventero\_ileum\_2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_colon}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vcolon}}} \Bigl( -v_{\mathrm{GU\_\_TALABS\_COLON}} + v_{\mathrm{GU\_\_TALEFL\_COLON}} + v_{\mathrm{GU\_\_TALFLUX\_ILEUM\_2\_COLON}} - v_{\mathrm{GU\_\_TALEXC}} \\
&\quad {} + v_{\mathrm{GU\_\_TALINF\_colon}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tal\_entero\_colon}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_TALABS\_COLON}} - v_{\mathrm{GU\_\_TALEFL\_COLON}} - v_{\mathrm{GU\_\_TALEX\_COLON}}}{\mathrm{GU}_{\mathrm{\_Ventero\_colon}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{tal}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_dissolution\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{tal}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_tal}} \cdot \mathrm{Mr}_{\mathrm{tal}} + \mathrm{Ri}_{\mathrm{tal}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_tal}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{tal}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_Abile\_tal}}}{\mathrm{d} t} &= v_{\mathrm{LI\_\_TALEX}} \qquad \text{(rate rule)}
\end{aligned}
$$
