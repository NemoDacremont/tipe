#!/bin/env python

import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse, creeFeu
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
DUREE_FEU = 20


N = 1

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]


def somme(L):
	s = 0
	for el in L:
		s += el

	return s


def optimisation(epsilon, h: float, alpha=0.1, beta=0.2, gamma=1):

	donnees = []

	grad = 10
	diffA = 10
	diffV = 10
	a = A
	v0 = V0
	dureeFeu = DUREE_FEU
	i = 0
	ecarts = [1 for i in range(N)]

	while i == 0 or abs(grad) > epsilon:
		i += 1

		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecarts = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)])


		a2 = a + h
		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a2, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsA = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)])


		# v02 = v0 + h
		# donneesVoitures, _ = simulationOptimisation(debits, v02, T, a, B,
		# 	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)
		#
		#
		# vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		# ecartsV = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(N)])


		diffA = (ecartsA - ecarts) / h
		# diffV = (ecartsV - ecarts) / h


		grad = diffA  # + diffV

		a = a - alpha * diffA
		# v0 = v0 - alpha * diffV

		donnees.append({
			"a": a,
			# "v0": v0,
			"ecarts": ecarts,
			"ecartsA": ecartsA,
			# "ecartsV": ecartsV,
			"diffA": diffA,
			# "diffV": diffV,
			"grad": grad
		})

		print("Fin itération", i, ":")
		print("a:", a)
		# print("v0:", v0)
		print("grad:", grad)
		print("ecarts:", ecarts)
		print("ecartsA:", ecartsA)
		# print("ecartsV:", ecartsV)
		print("diffA:", diffA)
		# print("diffV:", diffV)
		print("max grad:", abs(grad))

	return donnees

donnees = optimisation(1, 0.00001, 0.00001)

fichier = open("donneesOptimisations.csv", "w")

for i in range(len(donnees)):
	donnee = donnees[i]

	ligne = [donnee["a"], donnee["v0"], donnee["ecarts"], donnee["ecartsA"],
		donnee["ecartsV"], donnee["grad"], donnee["diffA"], donnee["diffV"]]
	ligne = [str(ligne[i]) for i in range(len(ligne))]

	texteLigne = ",".join(ligne) + "\n"
	fichier.write(texteLigne)

fichier.close()



