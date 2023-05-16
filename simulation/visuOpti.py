#!/bin/env python

from matplotlib import pyplot as plt
import sys


def extraitAttribut(donnees, attribut: str):
	out = []
	for i in range(len(donnees)):
		out.append(float(donnees[i][attribut]))

	return out 


def afficheGraphe(donnees, attribut: str):
	colonne = extraitAttribut(donnees, attribut)

	plt.figure()

	plt.plot(colonne, label=f"{attribut}")

	plt.title(f"{attribut} en fonction des itérations")

	plt.ylabel(f"{attribut}")
	plt.xlabel("itérations")
	plt.legend()


def ouvreCSV(cheminFichier: str, ID_entete=None, separateur=',', exclude_col={}):
	"""
		Ouvre un fichier csv

		paramètres:
			Si ID_entete = None -> renvoie un tableau
	"""
	fichier = open(cheminFichier, 'r', encoding='utf-8-sig')  # Cet encodage retire les BOM

	lignes = fichier.readlines()
	entete = lignes[0].replace("\n", "").split(separateur)
	# print(entete)

	fichier.close()

	# Stocke sous la forme d'un dictionnaire pour accélérer l'accès aux données
	if ID_entete == None:
		out = []
		for i in range(1, len(lignes)):
			ligne = lignes[i].replace("\n", "")
			els = ligne.split(separateur)

			l = {}
			for i in range(len(els)):
				if entete[i] not in exclude_col:
					l[entete[i]] = els[i]

			out.append(l)

	else:
		out = {}
		for i in range(1, len(lignes)):
			ligne = lignes[i].replace("\n", "")
			els = ligne.split(separateur)

			l = {}
			for i in range(len(els)):
				if entete[i] not in exclude_col:
					l[entete[i]] = els[i]

			out[l[ID_entete]] = l

	return out




nomFichier = "donneesOptimisations.csv"

if len(sys.argv) > 1:
	nomFichier = sys.argv[1]


graphes = ["ecarts", "diffA", "diffV", "a", "v0"]
donnees = ouvreCSV(nomFichier)

ecarts = extraitAttribut(donnees, "ecarts")
v0 = extraitAttribut(donnees, "v0")
# ecarts = extraitAttribut(donnees, "ecarts")

for attribut in graphes:
	afficheGraphe(donnees, attribut)


# plt.figure()
#
#
# pts = [(v0[i], ecarts[i]) for i in range(len(v0))]
# pts.sort()
# X = [pts[i][0] for i in range(len(pts))]
# Y = [pts[i][1] for i in range(len(pts))]
#
# plt.title("Ecart en fonction de v0")
#
# plt.plot(X, Y, "-+", label="Ecart")
#
# plt.xlabel("v0")
# plt.ylabel("Ecart")
# plt.legend()



plt.show()

