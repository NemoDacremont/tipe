#!/bin/env python

from simulation import lireFichierVitesse
from matplotlib import pyplot as plt
from constantes import DT
from manipulationDonnees import moyenneGlissante


from numpy import round
import sys
import os

def ouvreVitesses(cheminFichier="./vitesses.csv"):
	fichier = open(cheminFichier, "r")
	lignes = fichier.readlines()
	fichier.close()

	vitesses = []
	N = len(lignes)

	for i in range(N):
		# if i % 5000 == 0:
		# 	print(f"{i}/{N}")

		ligne = lignes[i]
		vitesse = float(ligne.replace("\n", ""))
		vitesses.append(vitesse)

	return vitesses


def moyenneMinute(vitesse, dureeMoyenne=60):
	out = [0.0 for _ in range(int(len(vitesse) / dureeMoyenne))]

	for i in range(int(len(vitesse) / dureeMoyenne)):
		moy = 0
		for j in range(dureeMoyenne):
			moy += vitesse[i * dureeMoyenne + j]

		moy /= dureeMoyenne
		out[i] = moy

	return out



DUREE_MOYENNE = 60

FICHIER_VITESSE_REELLES = "./vitesseVehicule/1-28/Strasbourg_P1"
FICHIER_VITESSE = "./vitesses.csv"
if len(sys.argv) >  1:
	FICHIER_VITESSE = sys.argv[1]


def afficheVitesse(cheminVitesseSimulee, dt=DT, dureeMoyenne=DUREE_MOYENNE, fichierVitesseReelles=FICHIER_VITESSE_REELLES):
	# VitessesSimulees
	vitessesSimulees = ouvreVitesses(cheminVitesseSimulee)

	# moyenne: centisecondes -> secondes
	vitessesSimulees = moyenneMinute(vitessesSimulees, 100)

	indicesVitessesSimulees = [i * dt * dureeMoyenne for i in range(int(len(vitessesSimulees) / dureeMoyenne))]
	v2 = moyenneMinute(vitessesSimulees, dureeMoyenne)
	v2 = moyenneGlissante(v2, 4)

	# Vitesess réelles
	vitessesReelles = lireFichierVitesse(fichierVitesseReelles)

	vitessesReelles = [vitessesReelles[i] / 3.6 for i in range(len(vitessesReelles))]
	vitessesReelles = moyenneGlissante(vitessesReelles, 4)
	indicesVitessesReelles = [i * 60 for i in range(len(vitessesReelles) - 1)]

	plt.figure()

	plt.title("Vitesse en fonction du temps")

	plt.plot(indicesVitessesSimulees, v2, "-+", label="vitesse simulée")
	plt.plot(indicesVitessesReelles, vitessesReelles[1:], "-+", label="vitesse Réelle")

	plt.xlabel("temps (en s)")
	plt.ylabel("Vitesse (en m/s)")

	plt.legend()

	plt.show()


def calculEcart(vitessesSimulee, vitesseReelle, dt=DT):
	"""
		vitesseSimulee à un intervalle dt, permet de s'adapter pour dt = 1s
		 -> dt en secondes
	"""

	vitessesSimuleeMoyenne = moyenneMinute(vitessesSimulee, int(60 / dt))
	ecart = 0
	N = len(vitessesSimuleeMoyenne)

	for i in range(N):
		ecart += (vitesseReelle[i] - vitessesSimuleeMoyenne[i]) ** 2

	return ecart / N





def affichePlan(cheminDossier: str, miniA, miniV, maxiA, maxiV, NA, NF, pasA, pasV):
	fichiers = os.listdir(cheminDossier)
	vitessesReelles = lireFichierVitesse("./vitesseVehicule/1-28/Strasbourg_P1")
	vitessesReelles = [vitessesReelles[i] / 3.6 for i in range(len(vitessesReelles))]

	# donnees: matrice de dimension NA * NF, contenant les vitesses :)
	donnees = [[0 for j in range(NA)] for i in range(NF)]

	# Rempli donnees
	for fichier in fichiers:
		cheminFichier = cheminDossier + "/" + fichier
		caracteristiques = fichier.replace("vitesses", "").replace(".csv", "")
		print(f"fichier: {cheminFichier}")
		print(f"a={caracteristiques[:3]}, v0={caracteristiques[3:]}")
		v0 = float(caracteristiques[3:])
		a = float(caracteristiques[:3])


		vitesses = ouvreVitesses(cheminFichier)
		vitesses = [vitesses[i] / 3.6 for i in range(len(vitesses))]

		j = int(round((a - miniA) / pasA))
		i = int(round((v0 - miniV) / pasV))
		ecart = calculEcart(vitesses, vitessesReelles, 1)

		print("i,j =", i, j, ecart)

		donnees[i][j] = ecart



	
	plt.figure()

	plt.title("Écart au réel en fonction de a et de v0")
	plt.imshow(donnees, cmap="hot", interpolation="none", extent=(miniA, maxiA, miniV, maxiV), aspect="auto")
	plt.colorbar()

	plt.ylabel("vitesse maximale (en m/s)")
	plt.xlabel("a (en m/s²)")

	plt.show()
	
affichePlan(FICHIER_VITESSE, 2.2, 7.5, 3.2, 9.5, 11, 11, 0.1, 0.2)
# afficheVitesse(FICHIER_VITESSE, 1, dureeMoyenne=60)


