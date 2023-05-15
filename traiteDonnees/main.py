#!/bin/env python
from traiteDonnees import readSauvegarde, extraitDonneesAvecMoyenne, moyenneGlissante
import matplotlib.pyplot as plt


def afficheDebit(fichier: str):
	donnees = readSauvegarde(fichier)
	# longueurVehicule = 3
	# longueurSegment = float(donnees[0]["Longueur"])
	# print("longueurSegment", longueurSegment)

	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Vitesse")
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


def getVitesse(fichier: str, heure: int):
	donnees = readSauvegarde(fichier)
	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Vitesse")

	out = []
	for i in range(len(temps)):
		if temps[i] < heure + 1 and temps[i] >= heure:
			out.append((temps[i], valDebit[i]))

	return out


def getDebit(fichier: str, heure: int):
	donnees = readSauvegarde(fichier)
	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Débit")

	out = []
	for i in range(len(temps)):
		if temps[i] < heure + 1 and temps[i] >= heure:
			out.append((temps[i], valDebit[i]))

	return out


def sauvegarde(nomFichier: str, lignes: list[str]):
	# try:
	# 	print("fichier créé")
	# 	fichier = open(nomFichier, "x")
	# 	fichier.close()
	# except:
	# 	pass
	print("sauvegarde", nomFichier)

	fichier = open(nomFichier, 'w')

	fichier.writelines(lignes)

	fichier.close()


def extrait(segment):
	nomFichierLecture = f"./sousDonnees/{segment.replace(' ', '_')}"
	nomFichierSauvegarde = f"./vitesseVehicule/{segment.replace(' ', '_')}"

	data = getVitesse(nomFichierLecture, 17)

	lignes = []
	for i in range(len(data)):
		lignes.append(f"{data[i][0]};{data[i][1]}\n")

	sauvegarde(nomFichierSauvegarde, lignes)

	print(nomFichierSauvegarde, "écrit!")


afficheDebit("./sousDonnees/Allende_I2")


N = 3
nomRue = "Strasbourg"
prefixes = ["I", "P"]
exclude = []

for prefixe in prefixes:
	for k in range(N):
		if f"{prefixe}{k + 1}" not in exclude:
			nomFichierLecture = f"./sousDonnees/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeVitesse = f"./vitesseVehicule/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeDebit = f"./debitVehicule/{nomRue}_{prefixe}{k + 1}"

			vitesses = getVitesse(nomFichierLecture, 17)
			debits = getDebit(nomFichierLecture, 17)

			lignesVitesses = []
			for i in range(len(vitesses)):
				lignesVitesses.append(f"{vitesses[i][0]};{vitesses[i][1]}\n")

			lignesDebit = []
			for i in range(len(debits)):
				lignesDebit.append(f"{debits[i][0]};{debits[i][1]}\n")

			sauvegarde(nomFichierSauvegardeVitesse, lignesVitesses)
			sauvegarde(nomFichierSauvegardeDebit, lignesDebit)

			print(f"{nomRue}_{prefixe}{k + 1}", "écrit!")




