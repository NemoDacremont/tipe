#!/bin/env python

import os
import sys

def ouvreVitesses(cheminFichier="./vitesses.csv"):
	"""
		fichier au format:

		v1
		v2
		.
		.
		.
		vn

		Retourne les vitesses :)
	"""
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


def moyenne(vitesse, dureeMoyenne=60):
	out = []

	for i in range(int(len(vitesse) / dureeMoyenne)):
		moy = 0
		for j in range(dureeMoyenne):
			moy += vitesse[i * dureeMoyenne + j]

		moy /= dureeMoyenne
		out.append(moy)

	return out



def reduitVitesse(chemin: str):
	print("traite", chemin)
	if os.path.isdir(chemin):
		files = os.listdir(chemin)
		for file in files:
			reduitVitesse(chemin + "/" + file)

	
	else:
		vitesses = ouvreVitesses(chemin)
		vitesses = moyenne(vitesses, 100)

		fichier = open(chemin, "w")
		for vitesse in vitesses:
			fichier.write(str(vitesse) + "\n")


argv = sys.argv

if len(argv) == 1:
	print("Entrez un fichier/dossier !")
	sys.exit()

chemin = argv[1]

reduitVitesse(chemin)





