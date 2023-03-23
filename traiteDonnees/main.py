#!/bin/env python
from traiteDonnees import readSauvegarde, extraitDonneesAvecMoyenne, moyenneGlissante
import matplotlib.pyplot as plt


def afficheDebit(fichier: str):
	donnees = readSauvegarde(fichier)
	# longueurVehicule = 3
	# longueurSegment = float(donnees[0]["Longueur"])
	# print("longueurSegment", longueurSegment)

	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Débit")
	# valDebitFiltree = moyenneGlissante(valDebit, 10)

	# Moyenne non filtrée
	plt.figure()

	plt.title("Débit instantané moyen en fonction du temps")
	plt.plot(temps, valDebit)

	plt.xlabel("instant (heure.min)")
	plt.ylabel("débit (voitures/s)")

	plt.show()

	# Moyenne Filtrée
	# plt.figure()
	#
	# plt.title("Débit instantané moyen filtré en fonction du temps")
	# plt.plot(temps, valDebitFiltree)
	#
	# plt.show()


def getDebit(fichier: str, heure: int):
	donnees = readSauvegarde(fichier)
	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Débit")

	out = []
	for i in range(len(temps)):
		if temps[i] < heure + 1 and temps[i] >= heure:
			out.append((temps[i], valDebit[i]))

	return out


def sauvegardeDebit(nomFichier: str, lignes: list[str]):
	# try:
	# 	print("fichier créé")
	# 	fichier = open(nomFichier, "x")
	# 	fichier.close()
	# except:
	# 	pass

	fichier = open(nomFichier, 'w')

	fichier.writelines(lignes)

	fichier.close()


# afficheDebit("./sousDonnees/Doulon_P1")

# N = 7
# nomRue = 'Doulon'
# prefixes = ['I', 'P']
# for prefixe in prefixes:
# 	for k in range(N):
# 		nomFichierLecture = f"./sousDonnees/Doulon_{prefixe}{k + 1}"
# 		nomFichierSauvegarde = f"./debitVehicule/Doulon_{prefixe}{k + 1}"
#
# 		data = getDebit(nomFichierLecture, 17)
#
# 		lignes = []
# 		for i in range(len(data)):
# 			lignes.append(f"{data[i][0]};{data[i][1]}")
#
# 		sauvegardeDebit(nomFichierSauvegarde, lignes)
#
# 		print(nomFichierSauvegarde, "écrit!")




