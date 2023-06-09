#%% Libs
from src.utils import probes
import numpy as np

#%% Global params
gamma = 1.4
T0    = 298.15
p0    = 101325
R     = 8314.46261815324 / 28.9   # Air
c0    = np.sqrt(gamma * R * T0)
M     = 0.5

omega_num = 20 * np.pi
f         = omega_num / (2 * np.pi)
lamb0     = c0 / f
lambd     = round(lamb0 * (1 + M))
lambu     = round(lamb0 * (1 - M))

freqSample = lambu/3
nPoints    = round(60*lambd *32/freqSample)   

#%% Spacial probes and Time probes
probes(number_of_probes=nPoints, lim = (-30*lambd,30*lambd), name_of_archive='probesSpacial')
probes(number_of_probes = 22, lim = (-30*lambd, 30*lambd), name_of_archive = 'probesTime')

x = np.linspace(-30*lambd, 30*lambd, 22)/lambd
print(np.round(x))

# %%
