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
DUREE_FEU = 26


N = 4

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

fichierSauvegardeTemporaire = "tmp.csv"

# Ajoute l'entête du fichier temporaire
entete = ["a", "v0", "dureeFeu", "ecarts", "ecartsA", "ecartsV", "ecartsF",
	"grad", "diffA", "diffV", "diffF"]

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
	K = 10**-9

	while i == 0 or abs(grad) > epsilon:
		i += 1
		feux = [
			creeFeu(0, 40, dureeFeu, 3)
		]

		donneesVoitures, _ = simulationOptimisation(debits, v0, T, a, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, feux=feux)

		vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecarts = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])


		a2 = a + h
		donneesVoituresA, _ = simulationOptimisation(debits, v0, T, a2, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)

		vitessesMoyennes_minutesA = extraitVitesseMoyenne(donneesVoituresA, 60)
		ecartsA = somme([(vitessesMoyennes_minutesA[i] - vitesses[i]) ** 2 for i in range(1, N)])


		# v02 = v0 + h
		# donneesVoitures, _ = simulationOptimisation(debits, v02, T, a, B,
		# 	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)
		#
		#
		# vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
		ecartsV = 0  # somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])

		H = 1 * h
		feux2 = [
			creeFeu(0, 40, (dureeFeu + H), 3)
		]

		print(feux2)

		donneesVoituresFeux, _ = simulationOptimisation(debits, v0, T, a, B,
			DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, feux=feux2)

		vitessesMoyennes_minutesFeux = extraitVitesseMoyenne(donneesVoituresFeux, 60)
		ecartsF = somme([(vitessesMoyennes_minutesFeux[i] - vitesses[i]) ** 2 for i in range(1, N)])


		diffA = (ecartsA - ecarts) / h
		diffV = 0  # (ecartsV - ecarts) / h
		diffF = (ecartsF - ecarts) / H


		grad = max(abs(diffA), abs(diffV), abs(diffF))

		a = a - alpha * diffA
		v0 = v0 - alpha * diffV
		dureeFeu = dureeFeu - alpha * diffF

		donnees.append({
			"a": a,
			"v0": v0,
			"dureeFeu": dureeFeu,
			"ecarts": ecarts,
			"ecartsA": ecartsA,
			"ecartsV": ecartsV,
			"ecartsF": ecartsF,
			"diffA": diffA,
			"diffV": diffV,
			"diffF": diffF,
			"grad": grad
		})

		print("Fin itération", i, ":")
		print("a:", a)
		print("v0:", v0)
		print("dureeFeu:", dureeFeu)
		print("grad:", grad)
		print("ecarts:", ecarts)
		print("ecartsA:", ecartsA)
		print("ecartsV:", ecartsV)
		print("ecartsF:", ecartsF)
		print("diffA:", diffA)
		print("diffV:", diffV)
		print("diffF:", diffF)
		print("max grad:", abs(grad))


		fichier = open(fichierSauvegardeTemporaire, "a")

		ligne = [a, v0, dureeFeu, ecarts, ecartsA, ecartsV, ecartsF, grad, diffA, diffV, diffF]
		ligne = [str(ligne[i]) for i in range(len(ligne))]

		fichier.write(",".join(ligne) + "\n")
		fichier.close()

	return donnees

donnees = optimisation(0.4, 10**-10, 10**-4)

fichier = open("donneesOptimisations.csv", "w")

for i in range(len(donnees)):
	donnee = donnees[i]

	ligne = [donnee["a"], donnee["v0"], donnee["dureeFeu"], donnee["ecarts"], donnee["ecartsA"],
		donnee["ecartsV"], donnee["ecartsF"], donnee["grad"], donnee["diffA"], donnee["diffV"],
		donnee["diffF"]]
	ligne = [str(ligne[i]) for i in range(len(ligne))]

	texteLigne = ",".join(ligne) + "\n"
	fichier.write(texteLigne)

fichier.close()



