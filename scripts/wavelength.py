#%% Libs
import numpy as np
import matplotlib.pyplot as plt

from src.path import *
from scipy.optimize import bisect
from scipy.interpolate import interp1d

#%% Parâmetros
gamma = 1.4
T0    = 298.15
p0    = 101325
R     = 8314.46261815324 / 28.9   # Air
c0    = np.sqrt(gamma * R * T0)
M     = 0.5

omega_num = 20 * np.pi
f         = omega_num / (2 * np.pi)
lamb0     = c0 / f
lambd     = lamb0 * (1 + M)
lambu     = lamb0 * (1 - M)
print(f'lambda0 = {lamb0} m')
print(f'lambda montante = {round(lambu,3)} m')
print(f'lambda jusante  = {round(lambd,3)} m')
print(f'Raio zona útil = {round(30*lambd)} m')
print(f'Raio zona de saída = {round(60*lambd)} m')
print(f't obs = {round(60*lambd/c0 + 2/f, 2)} s')
#%% import solução analítica
x, p = np.loadtxt(
    PATH_DATA.joinpath('monopoleFlow', 'analiticSolution2s.dat'), unpack=True
)
pf = interp1d(x, p, kind='cubic')

plt.plot(x, pf(x))
plt.grid()
plt.show()

#%% raizes
sign = np.sign(p)
roots = []
tol = 1e-5
for i in range(len(sign) - 1):
    if sign[i] * sign[i + 1] < 0:
        root = bisect(pf, x[i], x[i + 1])
        roots.append(root)
        if len(roots) > 1 and abs(roots[-2] - roots[-1]) < tol:
            roots.pop()
roots = np.array(roots)
#%% plot com as raizes e comprimentos de onda
save = True
lamb = np.diff(roots)

ticks = (roots[:-1] + roots[1:]) / 2

plt.plot(x, pf(x), 'k')
plt.plot(roots, pf(roots),
    'm^',
    markersize=5,
    label=r'$\lambda_{min}=$' + f'{round(min(lamb),3)} m',
)
plt.xticks(np.round(ticks, 2), [f'{round(i,1)}' for i in lamb], rotation=45)
for root in roots:
    plt.axvline(root, color = 'gray', linestyle = '--', linewidth = 0.5)

plt.title('Análise do comprimento de onda')
plt.xlabel(r'$\lambda \ [m]$')
plt.ylabel(r'$P \ [Pa]$')
plt.legend()
# plt.grid(axis='y')
if save:
    plt.savefig(PATH_IMAGES.joinpath('wave_length_analysis.png'), format ='png', dpi = 720)
plt.show()