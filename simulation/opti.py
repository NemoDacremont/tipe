#!/bin/env python

from simulation import lireFichierDebit, lireFichierVitesse, creeFeu
from manipulationDonnees import extraitVitesseMoyenne
from simulationOptimisation import simulationOptimisation


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

def somme(L: list):
	"""
		Retourne la somme des éléments d'une liste de int ou de float
	"""
	s = 0
	for el in L:
		s += el

	return s


def calculeEcart(a, dureeFeu):
	feux = [
		creeFeu(0, 40, dureeFeu, 3)
	]

	donneesVoitures, _ = simulationOptimisation(debits, V0, T, a, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, feux=feux)

	vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
	ecarts = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])

	return ecarts


debutA = 1.5
finA = 2.5
NA = 20  # nombre de points
pasA = (finA - debutA) / NA

debutF = 25
finF = 30
NF = 20  # nombre de points
pasF = (finF - debutF) / NF


accelerations = [debutA + i * pasA for i in range(NA)]
dureesFeux = [debutF + i * pasF for i in range(NF)]


debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]


fichierSauvegardeTemporaire = "tmp.csv"

# Ajoute l'entête du fichier temporaire
entete = ["a", "v0", "dureeFeu", "ecarts", "ecartsA", "ecartsV", "ecartsF",
	"grad", "diffA", "diffV", "diffF"]

entete = ",".join(entete) + "\n"

fichier = open(fichierSauvegardeTemporaire, "w")
fichier.write(entete)
fichier.close()


totalPoints = NA * NF
k = 0
print(f"Points faits: {k}/{totalPoints}")


for a in accelerations:
	for duree in dureesFeux:
		ecart = calculeEcart(a, duree)

		# ligne à sauvegarder dans le fichier temporaire
		ligne = [a, duree, ecart]
		ligne = [str(ligne[i]) for i in range(len(ligne))]
		texteLigne = ",".join(ligne) + "\n"

		# sauvegarde
		fichier = open(fichierSauvegardeTemporaire, "a")

		fichier.write(texteLigne)

		fichier.close
		k += 1
		print(f"Points faits: {k}/{totalPoints}")



