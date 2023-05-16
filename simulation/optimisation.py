#!/bin/env python

import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse, creeFeu
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1, moyenneGlissante
from affichage import affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show
from simulationOptimisation import simulationOptimisation

from numpy import sqrt

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
DUREE_FEU = 20


N = 4

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

fichierSauvegardeTemporaire = "tmp.csv"

# Ajoute l'entête du fichier temporaire
entete = ["a", "v0", "ecarts", "ecartsA", "ecartsV", "grad", "diffA", "diffV"]
entete = ",".join(entete) + "\n"

fichier = open(fichierSauvegardeTemporaire, "w")
fichier.write(entete)
fichier.close()

# Lecture des fichiers de données réelles
debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]


def somme(L: list):
	"""
		Retourne la somme des éléments d'une liste de int ou de float
	"""
	s = 0
	for el in L:
		s += el

	return s


def optimisation(epsilon, h, alpha=0.1):

	donnees = []

	grad = 10
	diffA = 10
	diffV = 10
	a = A
	v0 = V0
	dureeFeu = DUREE_FEU
	i = 0

	while i == 0 or abs(grad) > epsilon:
		i += 1

		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecarts = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])


		a2 = a + h
		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a2, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsA = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])


		v02 = v0 + h
		donneesVoitures, _ = simulationOptimisation(debits, v02, T, a, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)


		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsV = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])


		diffA = (ecartsA - ecarts) / h
		diffV = (ecartsV - ecarts) / h


		grad = max(abs(diffA), abs(diffV))

		a = a - alpha * diffA  * ecartsA
		v0 = v0 - alpha * diffV * ecartsV

		donnees.append({
			"a": a,
			"v0": v0,
			"ecarts": ecarts,
			"ecartsA": ecartsA,
			"ecartsV": ecartsV,
			"diffA": diffA,
			"diffV": diffV,
			"grad": grad
		})

		print("Fin itération", i, ":")
		print("a:", a)
		print("v0:", v0)
		print("grad:", grad)
		print("ecarts:", ecarts)
		print("ecartsA:", ecartsA)
		print("ecartsV:", ecartsV)
		print("diffA:", diffA)
		print("diffV:", diffV)
		print("max grad:", abs(grad))


		fichier = open(fichierSauvegardeTemporaire, "a")

		ligne = [a, v0, ecarts, ecartsA, ecartsV, grad, diffA, diffV]
		ligne = [str(ligne[i]) for i in range(len(ligne))]

		fichier.write(",".join(ligne) + "\n")
		fichier.close()

	return donnees

donnees = optimisation(0.4, 10**-13, 10**-8)

fichier = open("donneesOptimisations.csv", "w")

for i in range(len(donnees)):
	donnee = donnees[i]

	ligne = [donnee["a"], donnee["v0"], donnee["ecarts"], donnee["ecartsA"],
		donnee["ecartsV"], donnee["grad"], donnee["diffA"], donnee["diffV"]]
	ligne = [str(ligne[i]) for i in range(len(ligne))]

	texteLigne = ",".join(ligne) + "\n"
	fichier.write(texteLigne)

fichier.close()



