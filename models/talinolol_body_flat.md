# model: talinolol_body
Autogenerated ODE System from SBML file with sbmlutils.
```
time: [min]
substance: [mmol]
extent: [mmol]
volume: [l]
area: [m^2]
length: [m]
```

## Parameters `p`
```
BW = 75.0  # [kg] 
COBW = 1.548  # [ml/s/kg] 
COHRI = 150.0  # [ml] 
FQfo = 0.0146153846153846  # [-] 
FQgu = 0.18  # [-] 
FQh = 0.215  # [-] 
FQki = 0.19  # [-] 
FQlu = 1.0  # [-] 
FVar = 0.0257  # [l/kg] 
FVfo = 0.00482857142857143  # [l/kg] 
FVfov = 0.001  # [l/kg] 
FVgu = 0.0171  # [l/kg] 
FVhv = 0.001  # [l/kg] 
FVki = 0.0044  # [l/kg] 
FVli = 0.021  # [l/kg] 
FVlu = 0.0076  # [l/kg] 
FVpo = 0.001  # [l/kg] 
FVve = 0.0514  # [l/kg] 
Fblood = 0.02  # [-] 
GU__F_tal_abs = 0.454817449608062  # [-] 
GU__Ka_application_tal = 1000.0  # [1/hr] 
GU__Ri_tal_colon = 0.0  # [mg/min] 
GU__Ri_tal_duodenum = 0.0  # [mg/min] 
GU__Ri_tal_ileum_1 = 0.0  # [mg/min] 
GU__Ri_tal_ileum_2 = 0.0  # [mg/min] 
GU__Ri_tal_jejunum_1 = 0.0  # [mg/min] 
GU__Ri_tal_jejunum_2 = 0.0  # [mg/min] 
GU__TALABS_Km = 0.459  # [mmol/l] 
GU__TALABS_Vmax = 2.05772035007332  # [mmol/min/l] 
GU__TALEFL_Vmax = 0.328585050412362  # [1/min] 
GU__TALEX_Vmax = 0.000695176819174214  # [1/min] 
GU__TALFLUX_DUODENUM_k = 0.0666666666666667  # [1/min] 
GU__TALFLUX_ILEUM_1_k = 0.0121212121212121  # [1/min] 
GU__TALFLUX_ILEUM_2_k = 0.0121212121212121  # [1/min] 
GU__TALFLUX_JEJUNUM_1_k = 0.019047619047619  # [1/min] 
GU__TALFLUX_JEJUNUM_2_k = 0.019047619047619  # [1/min] 
GU__Vcolon = 3.8170350741116  # [l] 
GU__Vileum_1 = 0.944716180842621  # [l] 
GU__Vileum_2 = 0.944716180842621  # [l] 
GU__Vjejunum_1 = 0.601183024172577  # [l] 
GU__Vjejunum_2 = 0.601183024172577  # [l] 
GU__f_OATP2B1 = 1.0  # [-] 
GU__f_PG = 1.0  # [-] 
GU__f_velocity = 1.0  # [-] 
GU__oatp2b1_colon = 0.5  # [-] 
GU__oatp2b1_duodenum = 0.45  # [-] 
GU__oatp2b1_ileum_1 = 0.45  # [-] 
GU__oatp2b1_ileum_2 = 0.45  # [-] 
GU__oatp2b1_jejunum_1 = 0.5  # [-] 
GU__oatp2b1_jejunum_2 = 0.45  # [-] 
GU__pgp_colon = 0.25  # [-] 
GU__pgp_duodenum = 0.3  # [-] 
GU__pgp_ileum_1 = 0.7  # [-] 
GU__pgp_ileum_2 = 1.1  # [-] 
GU__pgp_jejunum_1 = 0.4  # [-] 
GU__pgp_jejunum_2 = 0.5  # [-] 
HCT = 0.51  # [-] 
HEIGHT = 170.0  # [cm] 
HR = 70.0  # [1/min] 
HRrest = 70.0  # [1/min] 
KI__TALEX_k = 0.959200672225413  # [1/min] 
KI__f_renal_function = 1.0  # [-] 
Ka_dis_tal = 0.681894676931315  # [1/hr] 
Kp_tal = 6.62140199045977  # [-] 
LI__TALEX_k = 0.150085430091066  # [1/min] 
LI__TALIM_Km_tal = 0.301  # [mmol/l] 
LI__TALIM_Vmax = 0.00998467038314402  # [mmol/min/l] 
LI__Vapical = nan  # [m^2] 
LI__Vbaso = nan  # [m^2] 
LI__Vbi = 1.0  # [l] 
LI__bile_flow = 0.000766666666666667  # [l/min] 
LI__f_EHC = 1.0  # [-] 
LI__f_OATP1B1 = 1.0  # [-] 
LI__f_PG = 1.0  # [-] 
Mr_tal = 363.495  # [g/mol] 
Ri_tal = 0.0  # [mg/min] 
Vduodenum = 0.322563025707332  # [l] 
Vfeces = 1.0  # [l] 
Vfo = 1.0  # [l] 
Vfov = 1.0  # [l] 
Vstomach = 1.0  # [l] 
Vurine = 1.0  # [l] 
conversion_min_per_day = 1440.0  # [min/day] 
cum_dose_intestine_tal = 0.0  # [mg] 
f_cirrhosis = 0.0  # [-] 
f_shunting_forearm = 0.28  # [-] 
ftissue_tal = 0.641324628334905  # [l/min] 
fup_tal = 0.4  # [-] 
ti_tal = 10.0  # [s] 
```

## Initial conditions `x0`
```
Afeces_tal = 0.0  # [mmol] Vfeces
Aurine_tal = 0.0  # [mmol] Vurine
Car_tal = 0.0  # [mmol/l] Var
Cduodenum_tal = 0.0  # [mmol/l] Vduodenum
Cfo_plasma_tal = 0.0  # [mmol/l] Vfo_plasma
Cfov_tal = 0.0  # [mmol/l] Vfov
Cgu_plasma_tal = 0.0  # [mmol/l] Vgu_plasma
Chv_tal = 0.0  # [mmol/l] Vhv
Cki_plasma_tal = 0.0  # [mmol/l] Vki_plasma
Cli_plasma_tal = 0.0  # [mmol/l] Vli_plasma
Clu_plasma_tal = 0.0  # [mmol/l] Vlu_plasma
Clu_tal = 0.0  # [mmol/l] Vlu_tissue
Cpo_tal = 0.0  # [mmol/l] Vpo
Cre_plasma_tal = 0.0  # [mmol/l] Vre_plasma
Cre_tal = 0.0  # [mmol/l] Vre_tissue
Cve_tal = 0.0  # [mmol/l] Vve
GU__POSTOMACH_tal = 0.0  # [mg] 
GU__tal_colon = 0.0  # [mmol/l] GU__Vcolon
GU__tal_entero_colon = 0.0  # [mmol/l] GU__Ventero_colon
GU__tal_entero_duodenum = 0.0  # [mmol/l] GU__Ventero_duodenum
GU__tal_entero_ileum_1 = 0.0  # [mmol/l] GU__Ventero_ileum_1
GU__tal_entero_ileum_2 = 0.0  # [mmol/l] GU__Ventero_ileum_2
GU__tal_entero_jejunum_1 = 0.0  # [mmol/l] GU__Ventero_jejunum_1
GU__tal_entero_jejunum_2 = 0.0  # [mmol/l] GU__Ventero_jejunum_2
GU__tal_ileum_1 = 0.0  # [mmol/l] GU__Vileum_1
GU__tal_ileum_2 = 0.0  # [mmol/l] GU__Vileum_2
GU__tal_jejunum_1 = 0.0  # [mmol/l] GU__Vjejunum_1
GU__tal_jejunum_2 = 0.0  # [mmol/l] GU__Vjejunum_2
GU__tal_stomach = 0.0  # [mmol] Vstomach
IVDOSE_tal = 0.0  # [mg] 
LI__Abile_tal = 0.0  # [mmol] 
LI__tal = 0.0  # [mmol/l] Vli_tissue
LI__tal_bi = 0.0  # [mmol] LI__Vbi
PODOSE_tal = 0.0  # [mg] 
cum_dose_tal = 0.0  # [mg] 
```

## ODE system
```
# y
Afov_tal = Cfov_tal * Vfov  # [mmol]
BSA = 0.024265 * (BW / 1)**0.5378 * (HEIGHT / 1)**0.3964  # [m^2]
CO = BW * COBW + (HR - HRrest) * COHRI / 60  # [ml/s]
FQre = 1 - (FQki + FQh + FQfo)  # [-]
FVre = 1 - (FVgu + FVki + FVli + FVlu + FVve + FVar + FVfo)  # [l/kg]
GU__TALINF_colon = GU__Ri_tal_colon / Mr_tal  # [mmol/min]
GU__TALINF_duodenum = GU__Ri_tal_duodenum / Mr_tal  # [mmol/min]
GU__TALINF_ileum_1 = GU__Ri_tal_ileum_1 / Mr_tal  # [mmol/min]
GU__TALINF_ileum_2 = GU__Ri_tal_ileum_2 / Mr_tal  # [mmol/min]
GU__TALINF_jejunum_1 = GU__Ri_tal_jejunum_1 / Mr_tal  # [mmol/min]
GU__TALINF_jejunum_2 = GU__Ri_tal_jejunum_2 / Mr_tal  # [mmol/min]
GU__Ventero_colon = 0.1 * GU__Vcolon  # [l]
GU__Ventero_duodenum = 0.1 * Vduodenum  # [l]
GU__Ventero_ileum_1 = 0.1 * GU__Vileum_1  # [l]
GU__Ventero_ileum_2 = 0.1 * GU__Vileum_2  # [l]
GU__Ventero_jejunum_1 = 0.1 * GU__Vjejunum_1  # [l]
GU__Ventero_jejunum_2 = 0.1 * GU__Vjejunum_2  # [l]
GU__application_tal = (GU__Ka_application_tal / 60) * PODOSE_tal / Mr_tal  # [mmol/min]
GU__dissolution_tal = (Ka_dis_tal / 60) * GU__POSTOMACH_tal / Mr_tal  # [mmol/min]
Ki_tal = (0.693 / ti_tal) * 60  # [1/min]
Var = BW * FVar - (FVar / (FVar + FVve)) * BW * Fblood * (1 - FVve - FVar)  # [l]
Vfo_plasma = Vfo * Fblood * (1 - HCT)  # [l]
Vfo_tissue = Vfo * (1 - Fblood)  # [l]
Vgu = BW * FVgu  # [l]
Vhv = (1 - HCT) * (BW * FVhv - (FVhv / (FVar + FVve + FVpo + FVhv + FVfo)) * BW * Fblood * (1 - (FVar + FVve + FVpo + FVhv + FVfo)))  # [l]
Vki = BW * FVki  # [l]
Vli = BW * FVli  # [l]
Vlu = BW * FVlu  # [l]
Vpo = (1 - HCT) * (BW * FVpo - (FVpo / (FVar + FVve + FVpo + FVhv + FVfo)) * BW * Fblood * (1 - (FVar + FVve + FVpo + FVhv + FVfo)))  # [l]
Vve = BW * FVve - (FVve / (FVar + FVve)) * BW * Fblood * (1 - FVve - FVar)  # [l]
Xfeces_tal = Afeces_tal * Mr_tal  # [mg]
Xurine_tal = Aurine_tal * Mr_tal  # [mg]
f_shunts = f_cirrhosis  # [-]
f_tissue_loss = f_cirrhosis  # [-]
transport_lu_tal = ftissue_tal * (Clu_plasma_tal * fup_tal * Kp_tal - Clu_tal)  # [mmol/min]
transport_re_tal = ftissue_tal * (Cre_plasma_tal * fup_tal * Kp_tal - Cre_tal)  # [mmol/min]
Aar_tal = Car_tal * Var  # [mmol]
Afo_plasma_tal = Cfo_plasma_tal * Vfo_plasma  # [mmol]
Ahv_tal = Chv_tal * Vhv  # [mmol]
Apo_tal = Cpo_tal * Vpo  # [mmol]
Ave_tal = Cve_tal * Vve  # [mmol]
GU__TALEFL_COLON = GU__f_PG * GU__pgp_colon * GU__TALEFL_Vmax * Vgu * GU__tal_entero_colon  # [mmol/min]
GU__TALEFL_DUODENUM = GU__f_PG * GU__pgp_duodenum * GU__TALEFL_Vmax * Vgu * GU__tal_entero_duodenum  # [mmol/min]
GU__TALEFL_ILEUM_1 = GU__f_PG * GU__pgp_ileum_1 * GU__TALEFL_Vmax * Vgu * GU__tal_entero_ileum_1  # [mmol/min]
GU__TALEFL_ILEUM_2 = GU__f_PG * GU__pgp_ileum_2 * GU__TALEFL_Vmax * Vgu * GU__tal_entero_ileum_2  # [mmol/min]
GU__TALEFL_JEJUNUM_1 = GU__f_PG * GU__pgp_jejunum_1 * GU__TALEFL_Vmax * Vgu * GU__tal_entero_jejunum_1  # [mmol/min]
GU__TALEFL_JEJUNUM_2 = GU__f_PG * GU__pgp_jejunum_2 * GU__TALEFL_Vmax * Vgu * GU__tal_entero_jejunum_2  # [mmol/min]
GU__TALEX_COLON = GU__TALEX_Vmax * Vgu * GU__tal_entero_colon  # [mmol/min]
GU__TALEX_DUODENUM = GU__TALEX_Vmax * Vgu * GU__tal_entero_duodenum  # [mmol/min]
GU__TALEX_ILEUM_1 = GU__TALEX_Vmax * Vgu * GU__tal_entero_ileum_1  # [mmol/min]
GU__TALEX_ILEUM_2 = GU__TALEX_Vmax * Vgu * GU__tal_entero_ileum_2  # [mmol/min]
GU__TALEX_JEJUNUM_1 = GU__TALEX_Vmax * Vgu * GU__tal_entero_jejunum_1  # [mmol/min]
GU__TALEX_JEJUNUM_2 = GU__TALEX_Vmax * Vgu * GU__tal_entero_jejunum_2  # [mmol/min]
GU__TALFLUX_DUODENUM_JEJUNUM_1 = GU__f_velocity * GU__TALFLUX_DUODENUM_k * Cduodenum_tal * Vgu  # [mmol/min]
GU__TALFLUX_ILEUM_1_ILEUM_2 = GU__f_velocity * GU__TALFLUX_ILEUM_1_k * GU__tal_ileum_1 * Vgu  # [mmol/min]
GU__TALFLUX_ILEUM_2_COLON = GU__f_velocity * GU__TALFLUX_ILEUM_2_k * GU__tal_ileum_2 * Vgu  # [mmol/min]
GU__TALFLUX_JEJUNUM_1_JEJUNUM_2 = GU__f_velocity * GU__TALFLUX_JEJUNUM_1_k * GU__tal_jejunum_1 * Vgu  # [mmol/min]
GU__TALFLUX_JEJUNUM_2_ILEUM_1 = GU__f_velocity * GU__TALFLUX_JEJUNUM_2_k * GU__tal_jejunum_2 * Vgu  # [mmol/min]
GU__absorption_colon = GU__oatp2b1_colon * GU__TALABS_Vmax * Vgu * GU__tal_colon / (GU__tal_colon + GU__TALABS_Km)  # [mmol/min]
GU__absorption_duodenum = GU__oatp2b1_duodenum * GU__TALABS_Vmax * Vgu * Cduodenum_tal / (Cduodenum_tal + GU__TALABS_Km)  # [mmol/min]
GU__absorption_ileum_1 = GU__oatp2b1_ileum_1 * GU__TALABS_Vmax * Vgu * GU__tal_ileum_1 / (GU__tal_ileum_1 + GU__TALABS_Km)  # [mmol/min]
GU__absorption_ileum_2 = GU__oatp2b1_ileum_2 * GU__TALABS_Vmax * Vgu * GU__tal_ileum_2 / (GU__tal_ileum_2 + GU__TALABS_Km)  # [mmol/min]
GU__absorption_jejunum_1 = GU__oatp2b1_jejunum_1 * GU__TALABS_Vmax * Vgu * GU__tal_jejunum_1 / (GU__tal_jejunum_1 + GU__TALABS_Km)  # [mmol/min]
GU__absorption_jejunum_2 = GU__oatp2b1_jejunum_2 * GU__TALABS_Vmax * Vgu * GU__tal_jejunum_2 / (GU__tal_jejunum_2 + GU__TALABS_Km)  # [mmol/min]
Mfov_tal = (Afov_tal / Vfov) * Mr_tal  # [mg/l]
QC = (CO / 1000) * 60  # [l/min]
Vgu_plasma = Vgu * Fblood * (1 - HCT)  # [l]
Vgu_tissue = Vgu * (1 - Fblood)  # [l]
Vki_plasma = Vki * Fblood * (1 - HCT)  # [l]
Vki_tissue = Vki * (1 - Fblood)  # [l]
Vli_plasma = Vli * Fblood * (1 - HCT)  # [l]
Vli_tissue = Vli * (1 - f_tissue_loss) * (1 - Fblood)  # [l]
Vlu_plasma = Vlu * Fblood * (1 - HCT)  # [l]
Vlu_tissue = Vlu * (1 - Fblood)  # [l]
Vre = BW * FVre  # [l]
Xfov_tal = Afov_tal * Mr_tal  # [mg]
iv_tal = Ki_tal * IVDOSE_tal / Mr_tal  # [mmol/min]
Agu_plasma_tal = Cgu_plasma_tal * Vgu_plasma  # [mmol]
Aki_plasma_tal = Cki_plasma_tal * Vki_plasma  # [mmol]
Ali_plasma_tal = Cli_plasma_tal * Vli_plasma  # [mmol]
Alu_plasma_tal = Clu_plasma_tal * Vlu_plasma  # [mmol]
GU__TALABS_COLON = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_colon  # [mmol/min]
GU__TALABS_DUODENUM = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_duodenum  # [mmol/min]
GU__TALABS_ILEUM_1 = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_ileum_1  # [mmol/min]
GU__TALABS_ILEUM_2 = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_ileum_2  # [mmol/min]
GU__TALABS_JEJUNUM_1 = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_jejunum_1  # [mmol/min]
GU__TALABS_JEJUNUM_2 = GU__f_OATP2B1 * GU__F_tal_abs * GU__absorption_jejunum_2  # [mmol/min]
GU__TALEXC = (1 - GU__F_tal_abs) * GU__absorption_colon  # [mmol/min]
KI__TALEX = KI__f_renal_function * KI__TALEX_k * Vki_tissue * Cki_plasma_tal * fup_tal  # [mmol/min]
LI__TALEX = LI__f_PG * LI__TALEX_k * Vli_tissue * LI__tal  # [mmol/min]
LI__TALIM = (LI__f_OATP1B1 * LI__TALIM_Vmax / LI__TALIM_Km_tal) * Vli_tissue * (Cli_plasma_tal * fup_tal - LI__tal) / (1 + Cli_plasma_tal / LI__TALIM_Km_tal + LI__tal / LI__TALIM_Km_tal)  # [mmol/min]
Mar_tal = (Aar_tal / Var) * Mr_tal  # [mg/l]
Mfo_plasma_tal = (Afo_plasma_tal / Vfo_plasma) * Mr_tal  # [mg/l]
Mhv_tal = (Ahv_tal / Vhv) * Mr_tal  # [mg/l]
Mpo_tal = (Apo_tal / Vpo) * Mr_tal  # [mg/l]
Mve_tal = (Ave_tal / Vve) * Mr_tal  # [mg/l]
Qfo = QC * FQfo  # [l/min]
Qgu = QC * FQgu  # [l/min]
Qh = QC * FQh  # [l/min]
Qki = QC * FQki  # [l/min]
Qlu = QC * FQlu  # [l/min]
Qre = QC * FQre  # [l/min]
Vre_plasma = Vre * Fblood * (1 - HCT)  # [l]
Vre_tissue = Vre * (1 - Fblood)  # [l]
Xar_tal = Aar_tal * Mr_tal  # [mg]
Xfo_plasma_tal = Afo_plasma_tal * Mr_tal  # [mg]
Xhv_tal = Ahv_tal * Mr_tal  # [mg]
Xpo_tal = Apo_tal * Mr_tal  # [mg]
Xve_tal = Ave_tal * Mr_tal  # [mg]
Are_plasma_tal = Cre_plasma_tal * Vre_plasma  # [mmol]
Flow_ar_fo_tal = Qfo * (1 - f_shunting_forearm) * Car_tal  # [mmol/min]
Flow_ar_gu_tal = Qgu * Car_tal  # [mmol/min]
Flow_ar_ki_tal = Qki * Car_tal  # [mmol/min]
Flow_ar_re_tal = Qre * Car_tal  # [mmol/min]
Flow_fo_fov_tal = Qfo * (1 - f_shunting_forearm) * Cfo_plasma_tal + Qfo * f_shunting_forearm * Car_tal  # [mmol/min]
Flow_fo_ve_tal = Qfo * Cfov_tal  # [mmol/min]
Flow_gu_po_tal = Qgu * Cgu_plasma_tal  # [mmol/min]
Flow_hv_ve_tal = Qh * Chv_tal  # [mmol/min]
Flow_ki_ve_tal = Qki * Cki_plasma_tal  # [mmol/min]
Flow_lu_ar_tal = Qlu * Clu_plasma_tal  # [mmol/min]
Flow_re_ve_tal = Qre * Cre_plasma_tal  # [mmol/min]
Flow_ve_lu_tal = Qlu * Cve_tal  # [mmol/min]
GU__TALUPTAKE_colon = GU__TALABS_COLON - GU__TALEFL_COLON  # [mmol/min]
GU__TALUPTAKE_duodenum = GU__TALABS_DUODENUM - GU__TALEFL_DUODENUM  # [mmol/min]
GU__TALUPTAKE_ileum_1 = GU__TALABS_ILEUM_1 - GU__TALEFL_ILEUM_1  # [mmol/min]
GU__TALUPTAKE_ileum_2 = GU__TALABS_ILEUM_2 - GU__TALEFL_ILEUM_2  # [mmol/min]
GU__TALUPTAKE_jejunum_1 = GU__TALABS_JEJUNUM_1 - GU__TALEFL_JEJUNUM_1  # [mmol/min]
GU__TALUPTAKE_jejunum_2 = GU__TALABS_JEJUNUM_2 - GU__TALEFL_JEJUNUM_2  # [mmol/min]
LI__Cbile_tal = LI__TALEX / LI__bile_flow  # [mmol/l]
LI__TALEHC = LI__f_EHC * LI__TALEX  # [mmol/min]
Mgu_plasma_tal = (Agu_plasma_tal / Vgu_plasma) * Mr_tal  # [mg/l]
Mki_plasma_tal = (Aki_plasma_tal / Vki_plasma) * Mr_tal  # [mg/l]
Mli_plasma_tal = (Ali_plasma_tal / Vli_plasma) * Mr_tal  # [mg/l]
Mlu_plasma_tal = (Alu_plasma_tal / Vlu_plasma) * Mr_tal  # [mg/l]
Qha = Qh - Qgu  # [l/min]
Qpo = Qgu  # [l/min]
Xgu_plasma_tal = Agu_plasma_tal * Mr_tal  # [mg]
Xki_plasma_tal = Aki_plasma_tal * Mr_tal  # [mg]
Xli_plasma_tal = Ali_plasma_tal * Mr_tal  # [mg]
Xlu_plasma_tal = Alu_plasma_tal * Mr_tal  # [mg]
Flow_arli_hv_tal = f_shunts * Qha * Car_tal  # [mmol/min]
Flow_arli_li_tal = (1 - f_shunts) * Qha * Car_tal  # [mmol/min]
Flow_li_hv_tal = (1 - f_shunts) * (Qpo + Qha) * Cli_plasma_tal  # [mmol/min]
Flow_po_hv_tal = f_shunts * Qpo * Cpo_tal  # [mmol/min]
Flow_po_li_tal = (1 - f_shunts) * Qpo * Cpo_tal  # [mmol/min]
Mre_plasma_tal = (Are_plasma_tal / Vre_plasma) * Mr_tal  # [mg/l]
Xre_plasma_tal = Are_plasma_tal * Mr_tal  # [mg]

# odes
d Afeces_tal/dt = GU__TALEXC  # [mmol/min]
d Aurine_tal/dt = KI__TALEX  # [mmol/min]
d Car_tal/dt = (-Flow_ar_ki_tal / Var - Flow_arli_li_tal / Var - Flow_arli_hv_tal / Var) + Flow_lu_ar_tal / Var - Flow_ar_gu_tal / Var - Flow_ar_re_tal / Var - Flow_ar_fo_tal / Var - Flow_fo_fov_tal / Var  # [mmol/l/min]
d Cduodenum_tal/dt = ((LI__TALEHC / Vduodenum - GU__TALABS_DUODENUM / Vduodenum) + GU__TALEFL_DUODENUM / Vduodenum - GU__TALFLUX_DUODENUM_JEJUNUM_1 / Vduodenum) + GU__TALINF_duodenum / Vduodenum + GU__dissolution_tal / Vduodenum  # [mmol/l/min]
d Cfo_plasma_tal/dt = Flow_ar_fo_tal / Vfo_plasma - Flow_fo_fov_tal / Vfo_plasma  # [mmol/l/min]
d Cfov_tal/dt = Flow_fo_fov_tal / Vfov - Flow_fo_ve_tal / Vfov  # [mmol/l/min]
d Cgu_plasma_tal/dt = (Flow_ar_gu_tal / Vgu_plasma - Flow_gu_po_tal / Vgu_plasma) + GU__TALEX_DUODENUM / Vgu_plasma + GU__TALEX_JEJUNUM_1 / Vgu_plasma + GU__TALEX_JEJUNUM_2 / Vgu_plasma + GU__TALEX_ILEUM_1 / Vgu_plasma + GU__TALEX_ILEUM_2 / Vgu_plasma + GU__TALEX_COLON / Vgu_plasma  # [mmol/l/min]
d Chv_tal/dt = Flow_arli_hv_tal / Vhv + Flow_po_hv_tal / Vhv + Flow_li_hv_tal / Vhv - Flow_hv_ve_tal / Vhv  # [mmol/l/min]
d Cki_plasma_tal/dt = Flow_ar_ki_tal / Vki_plasma - Flow_ki_ve_tal / Vki_plasma - KI__TALEX / Vki_plasma  # [mmol/l/min]
d Cli_plasma_tal/dt = Flow_arli_li_tal / Vli_plasma + Flow_po_li_tal / Vli_plasma - Flow_li_hv_tal / Vli_plasma - LI__TALIM / Vli_plasma  # [mmol/l/min]
d Clu_plasma_tal/dt = -transport_lu_tal / Vlu_plasma + Flow_ve_lu_tal / Vlu_plasma - Flow_lu_ar_tal / Vlu_plasma  # [mmol/l/min]
d Clu_tal/dt = transport_lu_tal / Vlu_tissue  # [mmol/l/min]
d Cpo_tal/dt = (-Flow_po_li_tal / Vpo - Flow_po_hv_tal / Vpo) + Flow_gu_po_tal / Vpo  # [mmol/l/min]
d Cre_plasma_tal/dt = -transport_re_tal / Vre_plasma + Flow_ar_re_tal / Vre_plasma - Flow_re_ve_tal / Vre_plasma  # [mmol/l/min]
d Cre_tal/dt = transport_re_tal / Vre_tissue  # [mmol/l/min]
d Cve_tal/dt = (iv_tal / Vve + Flow_ki_ve_tal / Vve + Flow_hv_ve_tal / Vve - Flow_ve_lu_tal / Vve) + Flow_re_ve_tal / Vve + Flow_fo_ve_tal / Vve  # [mmol/l/min]
d GU__POSTOMACH_tal/dt = (GU__application_tal - GU__dissolution_tal) * Mr_tal  # [mg/min]
d GU__tal_colon/dt = (-GU__TALABS_COLON / GU__Vcolon + GU__TALEFL_COLON / GU__Vcolon + GU__TALFLUX_ILEUM_2_COLON / GU__Vcolon - GU__TALEXC / GU__Vcolon) + GU__TALINF_colon / GU__Vcolon  # [mmol/l/min]
d GU__tal_entero_colon/dt = GU__TALABS_COLON / GU__Ventero_colon - GU__TALEFL_COLON / GU__Ventero_colon - GU__TALEX_COLON / GU__Ventero_colon  # [mmol/l/min]
d GU__tal_entero_duodenum/dt = GU__TALABS_DUODENUM / GU__Ventero_duodenum - GU__TALEFL_DUODENUM / GU__Ventero_duodenum - GU__TALEX_DUODENUM / GU__Ventero_duodenum  # [mmol/l/min]
d GU__tal_entero_ileum_1/dt = GU__TALABS_ILEUM_1 / GU__Ventero_ileum_1 - GU__TALEFL_ILEUM_1 / GU__Ventero_ileum_1 - GU__TALEX_ILEUM_1 / GU__Ventero_ileum_1  # [mmol/l/min]
d GU__tal_entero_ileum_2/dt = GU__TALABS_ILEUM_2 / GU__Ventero_ileum_2 - GU__TALEFL_ILEUM_2 / GU__Ventero_ileum_2 - GU__TALEX_ILEUM_2 / GU__Ventero_ileum_2  # [mmol/l/min]
d GU__tal_entero_jejunum_1/dt = GU__TALABS_JEJUNUM_1 / GU__Ventero_jejunum_1 - GU__TALEFL_JEJUNUM_1 / GU__Ventero_jejunum_1 - GU__TALEX_JEJUNUM_1 / GU__Ventero_jejunum_1  # [mmol/l/min]
d GU__tal_entero_jejunum_2/dt = GU__TALABS_JEJUNUM_2 / GU__Ventero_jejunum_2 - GU__TALEFL_JEJUNUM_2 / GU__Ventero_jejunum_2 - GU__TALEX_JEJUNUM_2 / GU__Ventero_jejunum_2  # [mmol/l/min]
d GU__tal_ileum_1/dt = (-GU__TALABS_ILEUM_1 / GU__Vileum_1 + GU__TALEFL_ILEUM_1 / GU__Vileum_1 + GU__TALFLUX_JEJUNUM_2_ILEUM_1 / GU__Vileum_1 - GU__TALFLUX_ILEUM_1_ILEUM_2 / GU__Vileum_1) + GU__TALINF_ileum_1 / GU__Vileum_1  # [mmol/l/min]
d GU__tal_ileum_2/dt = (-GU__TALABS_ILEUM_2 / GU__Vileum_2 + GU__TALEFL_ILEUM_2 / GU__Vileum_2 + GU__TALFLUX_ILEUM_1_ILEUM_2 / GU__Vileum_2 - GU__TALFLUX_ILEUM_2_COLON / GU__Vileum_2) + GU__TALINF_ileum_2 / GU__Vileum_2  # [mmol/l/min]
d GU__tal_jejunum_1/dt = (-GU__TALABS_JEJUNUM_1 / GU__Vjejunum_1 + GU__TALEFL_JEJUNUM_1 / GU__Vjejunum_1 + GU__TALFLUX_DUODENUM_JEJUNUM_1 / GU__Vjejunum_1 - GU__TALFLUX_JEJUNUM_1_JEJUNUM_2 / GU__Vjejunum_1) + GU__TALINF_jejunum_1 / GU__Vjejunum_1  # [mmol/l/min]
d GU__tal_jejunum_2/dt = (-GU__TALABS_JEJUNUM_2 / GU__Vjejunum_2 + GU__TALEFL_JEJUNUM_2 / GU__Vjejunum_2 + GU__TALFLUX_JEJUNUM_1_JEJUNUM_2 / GU__Vjejunum_2 - GU__TALFLUX_JEJUNUM_2_ILEUM_1 / GU__Vjejunum_2) + GU__TALINF_jejunum_2 / GU__Vjejunum_2  # [mmol/l/min]
d GU__tal_stomach/dt = 0  # [mmol/min]
d IVDOSE_tal/dt = -iv_tal * Mr_tal + Ri_tal  # [mg/min]
d LI__Abile_tal/dt = LI__TALEX  # [mmol/min]
d LI__tal/dt = LI__TALIM / Vli_tissue - LI__TALEX / Vli_tissue  # [mmol/l/min]
d LI__tal_bi/dt = LI__TALEX - LI__TALEHC  # [mmol/min]
d PODOSE_tal/dt = -GU__application_tal * Mr_tal  # [mg/min]
d cum_dose_tal/dt = Ri_tal  # [mg/min]
```