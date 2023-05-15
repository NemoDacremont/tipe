#!/bin/env python

import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1, moyenneGlissante
from affichage import affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show
from simulationOptimisation import simulationOptimisation

# pour des conseils:
# https://traffic-simulation.de/info/info_IDM.html
# Caractéristiques voiture / modèle
V0 = 8.33  # 3.33  # =5.4 à 17h17
T = 1.6
A = 2.0  # 2.77  # 0.73
B = 2
DELTA = 4
L = 4
S0 = 2
S1 = 3

PHYSIQUE = {
	"x": 0,
	"vx": V0,
	"ax": 0,
	"s_star": 0
}

# Constantes simulation
DEBUT = 0
FIN = 60
DT = 0.01

DIST_MAX = 245


N = 3

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]


def optimisation(epsilon, alpha=0.1, beta=0.2, gamma=1):
	grad = [-2 for i in range(N)]
	diffA = [-1 for i in range(N)]
	diffV = [-1 for i in range(N)]
	a = [A for _ in range(N)]
	v0 = [V0 for _ in range(N)]
	i = 0
	ecarts = [1 for i in range(N)]

	while i == 0 or max([abs(grad[i]) for i in range(N)]) > epsilon:
		i += 1

		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecarts = [(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)]


		a = [max(a[i] - alpha * diffA[i], 0.5) for i in range(N)]
		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsA = [(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)]


		v0 = [max(v0[i] - beta * diffV[i], 1.0) for i in range(N)]
		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsV = [(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)]

		diffA = [(ecartsA[i] - ecarts[i]) / alpha for i in range(N)]
		diffV = [(ecartsV[i] - ecarts[i]) / beta for i in range(N)]

		grad = [diffA[i] + diffV[i] for i in range(N)]
		print("Fin itération", i, ":")
		print("a:", a)
		print("v0:", v0)
		print("grad:", grad)
		print("ecarts:", ecarts)
		print("ecartsA:", ecartsA)
		print("ecartsV:", ecartsV)
		print("diffA:", diffA)
		print("diffV:", diffV)
		print("max grad:", max([abs(grad[i]) for i in range(N)]))

	return a, v0, grad

print(optimisation(4, 0.01, 0.01))


