#!/bin/env python

from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
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


def sauvegardeVitesseCSV(cheminFichier: str, vitesses: list):
	fichier = open(cheminFichier, "w")

	for vitesse in vitesses:
		fichier.write(vitesse)

	fichier.close()






nomFichier = "donneesOptimisations.csv"

if len(sys.argv) > 1:
	nomFichier = sys.argv[1]


graphes = []
donnees = ouvreCSV(nomFichier)

ecarts = extraitAttribut(donnees, "ecarts")
a = extraitAttribut(donnees, "a")
dureeFeu = extraitAttribut(donnees, "dureeFeu")

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


NA = 100 # int((maxiA - miniA) / pasA)
NF = 100 # int((maxiF - miniF) / pasF)

miniA = 1.5  # min(a)
maxiA = 4  # max(a)
miniF = 20  # min(dureeFeu)
maxiF = 40  # max(dureeFeu)

pasA = (maxiA - miniA) / 100
pasF = (maxiF - miniF) / 100

Z = [[-np.inf for _ in range(NA)] for _ in range(NF)]

print(miniA, maxiA, pasA)
print(miniF, maxiF, pasF)


for k in range(len(a)):
	print("fait:", k, "/", len(a))
	i = int(np.round((dureeFeu[k] - miniF) / pasF))
	j = int(np.round((a[k] - miniA) / pasA))

	print(a[k], dureeFeu[k], np.log(ecarts[k]))
	print((a[k] - miniA) / pasA, (dureeFeu[k] - miniF) / pasF)
	print(i, j)
	print(len(Z), len(Z[0]))

	Z[i][j] = np.log(ecarts[k])

print("Début affichage")

# plt.imshow(Z, cmap="turbo", interpolation='none', extent=(np.amin(a), np.amax(a), np.amin(dureeFeu), np.amax(dureeFeu)), aspect = 'auto')

plt.figure()

plt.title("grad en fonction de a, dureeFeu")

plt.imshow(Z, cmap="hot", interpolation='none', extent=(miniA, maxiA, miniF, maxiF), aspect = 'auto')
plt.colorbar()
# plt.quiver(a, dureeFeu, diffA, diffF, color="r")

# plt.imshow(pts, interpolation='none', aspect=0.01, origin="lower")  # , extent=[1, 2, 25, 30])
# ax = plt.gca()

plt.xlabel("a")
plt.ylabel("dureeFeu")


plt.show()

