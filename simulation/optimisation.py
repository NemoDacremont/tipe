#!/bin/env python

import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1, moyenneGlissante
from affichage import affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show

# pour des conseils:
# https://traffic-simulation.de/info/info_IDM.html
# Caractéristiques voiture / modèle
V0 = 8.33  # 3.33  # =5.4 à 17h17
T = 1.6
A = 2  # 2.77  # 0.73
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


N = 10
temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec


def optimisation(epsilon):
	debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
	vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]
	donneesVoitures, donneesFeux = simulationRue(debits, V0, T, A, B,
		DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)


	pass




