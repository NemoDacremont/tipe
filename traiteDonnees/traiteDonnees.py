#!/bin/env python

import os
import matplotlib.pyplot as plt
import numpy as np
import filtrage


def ouvreCSV(cheminFichier: str, ID_entete="Identifiant", separateur=',', exclude_col={}):
	fichier = open(cheminFichier, 'r', encoding='utf-8-sig')  # Cet encodage retire les BOM

	lignes = fichier.readlines()
	entete = lignes[0].replace("\n", "").split(separateur)
	# print(entete)

	fichier.close()

	# Stocke sous la forme d'un dictionnaire pour accélérer l'accès aux données
	out = {}

	for i in range(1, len(lignes)):
		ligne = lignes[i].replace("\n", "")
		els = ligne.split(separateur)

		l = {}
		for i in range(len(els)):
			if entete[i] not in exclude_col:
				l[entete[i]] = els[i]

		out[l[ID_entete]] = l

	print(out)
	input()
	return out


def readSegment(nomSegment: str, dossierDonnees="donnees"):
	nomFichiers = os.listdir(dossierDonnees)

	donnees = []

	for nomFichier in nomFichiers:
		chemin = f"{dossierDonnees}/{nomFichier}"

		try:
			donneesFichier = ouvreCSV(chemin, ID_entete="Nom du tronçon",
				separateur=';', exclude_col={"Geométrie", "geo_point_2d"})

			donnees.append(donneesFichier[nomSegment])
		except Exception as e:
			print(f"n'a pas pu lire le fichier {chemin}: {e}")


	return donnees


def convertionHeure(heure: str):
	"""
		converti une heure au format 2023-01-26T12:39:00+01:00
		en une heure au format HH:mm
	"""
	_, p1 = heure.split("T")
	h, m, _, _ = p1.split(":")

	print(f"{h}, {m}, {10 * int(h) / 24 + int(m) / 60}")

	return 10 * int(h) / 24 + int(m) / 60  # f"{h}:{m}"


donnees = readSegment("Doulon P1")

tmpVals = {}
tmpCompte = {}

for el in donnees:
	temps = convertionHeure(el['Horodatage'])
	if temps not in tmpVals:
		tmpVals[temps] = 0
	tmpVals[temps] += int(el["Débit"])

	if temps not in tmpCompte:
		tmpCompte[temps] = 0
	tmpCompte[temps] += 1

for i in tmpVals:
	tmpVals[i] /= tmpCompte[i]


timeStamp = [convertionHeure(el['Horodatage']) for el in donnees]
vitesse = [el['Vitesse'] for el in donnees]
debit = [int(el['Débit']) for el in donnees]

temps = []
vals = []
for i in tmpVals:
	temps.append(i)
	vals.append(tmpVals[i])


Te = 1 / 60
H0, wc = 1, 6.28 / (24 * 3600)
params = [H0, wc]

tmp1 = [(temps[i], vals[i]) for i in range(len(temps))]

for i in range(len(tmp1)):
	for j in range(len(tmp1) - 1 - i):
		if tmp1[j][0] > tmp1[j + 1][0]:
			c = tmp1[j + 1]
			tmp1[j + 1] = tmp1[j]
			tmp1[j] = c


print(tmp1)
temps = [tmp1[i][0] for i in range(len(tmp1))]
val = [tmp1[i][1] for i in range(len(tmp1))]

val2 = filtrage.filtrage(np.array(val, dtype=np.float64), Te, filtrage.passe_bas, params)

# pas moyenne
# plt.figure()
#
# plt.title("Débit instantané en fonction du temps")
# plt.plot(timeStamp, debit)
# plt.xlabel("instant (date)")
# plt.ylabel("débit (voitures/s)")


# moyenne
plt.figure()

plt.title("Débit instantané moyen en fonction du temps")
plt.plot(temps, val)

plt.xlim(-1, 11)
plt.xlabel("instant (heure.min)")
plt.ylabel("débit (voitures/s)")


plt.figure()

plt.title("Débit instantané moyen filtré en fonction du temps")
plt.plot(temps, val2)

plt.xlim(-1, 11)
plt.xlabel("instant (heure.min)")
plt.ylabel("débit (voitures/s)")



plt.show()
