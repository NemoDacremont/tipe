#!/bin/env python

from matplotlib import pyplot as plt
import sys


def extraitAttribut(donnees, attribut: str):
	out = []
	for i in range(len(donnees)):
		out.append(donnees[i][attribut])

	return out 


def afficheGraphe(donnees, attribut: str):
	colonne = extraitAttribut(donnees, attribut)

	plt.figure()

	plt.plot(colonne, label=f"{attribut}")

	plt.title(f"{attribut} en fonction des itérations")

	plt.ylabel("attribut")
	plt.xlabel("itérations")
	plt.legend()



nomFichier = "donneesOptimisations.csv"

if len(sys.argv) > 1:
	nomFichier = sys.argv[1]


fichier = open(nomFichier, "r")

lignes = fichier.readlines()

fichier.close()


graphes = ["ecarts", "grad", "a", "v0"]
donnees = []
for ligne in lignes:
	tmp = ligne.split(",")
	tmp = [float(tmp[i]) for i in range(len(tmp))]
	a, v0, ecarts, ecartsA, ecartsV, grad, diffA, diffV = tmp

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


for attribut in graphes:
	afficheGraphe(donnees, attribut)

plt.show()

