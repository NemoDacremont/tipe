#!/bin/env python

from simulation import lireFichierVitesse
from matplotlib import pyplot as plt
from constantes import DT
from manipulationDonnees import moyenneGlissante
import sys

def ouvreVitesses(cheminFichier="./vitesses.csv"):
	fichier = open(cheminFichier, "r")
	lignes = fichier.readlines()
	fichier.close()

	vitesses = []
	N = len(lignes)

	for i in range(N):
		if i % 5000 == 0:
			print(f"{i}/{N}")

		ligne = lignes[i]
		vitesse = float(ligne.replace("\n", ""))
		vitesses.append(vitesse)

	return vitesses


def moyenneMinute(vitesse, dureeMoyenne=60):
	out = []

	for i in range(int(len(vitesse) / dureeMoyenne)):
		moy = 0
		for j in range(dureeMoyenne):
			moy += vitesse[i * dureeMoyenne + j]

		moy /= dureeMoyenne
		out.append(moy)

	return out


DUREE_MOYENNE = 3000

FICHIER_VITESSE = "./vitesses.csv"
if len(sys.argv) >  1:
	FICHIER_VITESSE = sys.argv[1]

vitessesSimulees = ouvreVitesses(FICHIER_VITESSE)
indicesVitessesSimulees = [i * DT * DUREE_MOYENNE for i in range(int(len(vitessesSimulees) / DUREE_MOYENNE))]
v2 = moyenneMinute(vitessesSimulees, DUREE_MOYENNE)
v2 = moyenneGlissante(v2, 30)

vitessesReelles = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")
vitessesReelles = moyenneGlissante(vitessesReelles, 5)
indicesVitessesReelles = [i * 60 for i in range(len(vitessesReelles))]

plt.figure()

plt.title("Vitesse en fonction du temps")

plt.plot(indicesVitessesSimulees, v2, "-+", label="vitesse simulée")
plt.plot(indicesVitessesReelles, vitessesReelles, "-+", label="vitesse Réelle")

plt.xlabel("temps (en s)")
plt.ylabel("Vitesse (en m/s)")

plt.legend()

plt.show()


