#!/bin/env python

from matplotlib import pyplot as plt


def extraitAttribut(donnees, attribut: str):
	out = []
	for i in range(len(donnees)):
		out.append(donnees[i][attribut])

	return out 





nomFichier = "donneesOptimisations.csv"
fichier = open(nomFichier, "r")

lignes = fichier.readlines()

fichier.close()


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


ecarts = extraitAttribut(donnees, "ecarts")

plt.figure()

plt.plot(ecarts)

plt.show()


