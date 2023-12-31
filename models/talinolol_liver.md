# model: talinolol_liver
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
TALEX_k = 0.150085430091066  # [1/min] 
TALIM_Km_tal = 0.301  # [mmol/l] 
TALIM_Vmax = 0.00998467038314402  # [mmol/min/l] 
Vapical = nan  # [m^2] 
Vbaso = nan  # [m^2] 
Vbi = 1.0  # [l] 
Vduodenum = 0.1  # [l] 
Vext = 4.0  # [l] 
Vli = 1.5  # [l] 
bile_flow = 0.000766666666666667  # [l/min] 
f_EHC = 1.0  # [-] 
f_OATP1B1 = 1.0  # [-] 
f_PG = 1.0  # [-] 
fup_tal = 0.4  # [-] 
```

## Initial conditions `x0`
```
Abile_tal = 0.0  # [mmol] 
tal = 0.0  # [mmol/l] Vli
tal_bi = 0.0  # [mmol] Vbi
tal_duodenum = 0.0  # [mmol/l] Vduodenum
tal_ext = 0.0  # [mmol/l] Vext
```

## ODE system
```
# y
TALEX = f_PG * TALEX_k * Vli * tal  # [mmol/min]
TALIM = (f_OATP1B1 * TALIM_Vmax / TALIM_Km_tal) * Vli * (tal_ext * fup_tal - tal) / (1 + tal_ext / TALIM_Km_tal + tal / TALIM_Km_tal)  # [mmol/min]
Cbile_tal = TALEX / bile_flow  # [mmol/l]
TALEHC = f_EHC * TALEX  # [mmol/min]

# odes
d Abile_tal/dt = TALEX  # [mmol/min]
d tal/dt = TALIM / Vli - TALEX / Vli  # [mmol/l/min]
d tal_bi/dt = TALEX - TALEHC  # [mmol/min]
d tal_duodenum/dt = TALEHC / Vduodenum  # [mmol/l/min]
d tal_ext/dt = -TALIM / Vext  # [mmol/l/min]
```