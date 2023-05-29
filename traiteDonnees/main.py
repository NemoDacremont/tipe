#!/bin/env python
from traiteDonnees import extraitHorodatage, readSauvegarde, extraitDonneesAvecMoyenne, moyenneGlissante, readSegment, tronqueHeure
import matplotlib.pyplot as plt


import os


def afficheDebit(fichier: str):
	"""
	"""
	donnees = readSauvegarde(fichier)
	# longueurVehicule = 3
	# longueurSegment = float(donnees[0]["Longueur"])
	# print("longueurSegment", longueurSegment)

	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Vitesse")
	valDebitFiltree = moyenneGlissante(valDebit, 15)

	# Moyenne non filtrée
	plt.figure()

	plt.title("Débit instantané moyen en fonction du temps")
	plt.plot(temps, valDebit)

	plt.xlabel("instant (heure.min)")
	plt.ylabel("débit (voitures/s)")

	# Moyenne Filtrée
	plt.figure()

	plt.title("Débit instantané moyen filtré en fonction du temps")
	plt.plot(temps, valDebitFiltree)

	plt.show()


def getVitesse(fichier: str, heureDebut: float, heureFin: float):
	donnees = readSauvegarde(fichier)
	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Vitesse")

	out = []
	for i in range(len(temps)):
		if temps[i] < heureFin and temps[i] >= heureDebut:
			out.append((temps[i], valDebit[i]))

	return out


def getDebit(fichier: str, heureDebut: float, heureFin: float):
	donnees = readSauvegarde(fichier)
	temps, valDebit = extraitDonneesAvecMoyenne(donnees, "Débit")

	out = []
	for i in range(len(temps)):
		if temps[i] < heureFin and temps[i] >= heureDebut:
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

	data = getVitesse(nomFichierLecture, 17, 18)

	lignes = []
	for i in range(len(data)):
		lignes.append(f"{data[i][0]};{data[i][1]}\n")

	sauvegarde(nomFichierSauvegarde, lignes)

	print(nomFichierSauvegarde, "écrit!")


# afficheDebit("./sousDonnees/Strasbourg_P1")

nomFichier = "./debitVehicule/1-28/Strasbourg_P1"

fichier = open(nomFichier, "r")

lignes = fichier.readlines()
data = []

for ligne in lignes:
	temps, debit = ligne.replace("\n", "").split(",")
	data.append([float(temps), float(debit)])

data.sort()
X = [data[i][0] for i in range(len(data))]
Y = [data[i][1] for i in range(len(data))]

plt.figure()

plt.plot(X, Y)
plt.show()



input()



# Extrait les débits et les vitesses réelles
# N = 3
# nomRue = "Strasbourg"
# prefixes = ["I", "P"]
# exclude = []
#
# for prefixe in prefixes:
# 	for k in range(N):
# 		if f"{prefixe}{k + 1}" not in exclude:
# 			nomFichierLecture = f"./sousDonnees/{nomRue}_{prefixe}{k + 1}"
# 			nomFichierSauvegardeVitesse = f"./vitesseVehicule/{nomRue}_{prefixe}{k + 1}"
# 			nomFichierSauvegardeDebit = f"./debitVehicule/{nomRue}_{prefixe}{k + 1}"
#
# 			vitesses = getVitesse(nomFichierLecture, 15.5, 21)
# 			debits = getDebit(nomFichierLecture, 15.5, 21)
#
# 			lignesVitesses = []
# 			for i in range(len(vitesses)):
# 				lignesVitesses.append(f"{vitesses[i][0]};{vitesses[i][1]}\n")
#
# 			lignesDebit = []
# 			for i in range(len(debits)):
# 				lignesDebit.append(f"{debits[i][0]};{debits[i][1]}\n")
#
# 			sauvegarde(nomFichierSauvegardeVitesse, lignesVitesses)
# 			sauvegarde(nomFichierSauvegardeDebit, lignesDebit)
#
# 			print(f"{nomRue}_{prefixe}{k + 1}", "écrit!")


N = 1
nomRue = "Strasbourg"
prefixes = ["P"]
exclude = []

donnees = {}

for prefixe in prefixes:
	for k in range(N):
		if f"{prefixe}{k + 1}" not in exclude:
			nomSegment = f"{nomRue} {prefixe}{k + 1}"
			nomFichierLecture = f"./sousDonnees/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeVitesse = f"./vitesseVehicule/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeDebit = f"./debitVehicule/{nomRue}_{prefixe}{k + 1}"

			segments = readSegment(nomSegment)

			N = len(segments)

			for i in range(N):
				segment = segments[i]
				horodatage = extraitHorodatage(segment["Horodatage"])

				jour = horodatage["jour"]
				mois = horodatage["mois"]
				heure = horodatage["h"]
				minute = horodatage["m"]

				cle = f"{mois}-{jour}"
				if cle not in donnees:
					donnees[cle] = {}

				if heure not in donnees[cle]:
					donnees[cle][heure] = {}

				if minute not in donnees[cle]:
					donnees[cle][heure][minute] = {}

				donnees[cle][heure][minute] = segment

				print(f"{i} / {N}, {cle}")


			# for cle in vitesses:
			# 	print(vitesses[cle])
			# 	print(len(vitesses))
			# 	plt.figure()
			#
			# 	plt.title(f"nombre de données par heure le {cle}")
			# 	plt.plot(vitesses[cle])
			#
			# 	plt.xlabel("heure (en h)")
			# 	plt.ylabel("nombre de données")
			#
			# plt.show()


			# vitesses = getVitesse(nomFichierLecture, 15.5, 21)
			# debits = getDebit(nomFichierLecture, 15.5, 21)

			# lignesVitesses = []
			# for i in range(len(vitesses)):
			# 	lignesVitesses.append(f"{vitesses[i][0]};{vitesses[i][1]}\n")
			#
			# lignesDebit = []
			# for i in range(len(debits)):
			# 	lignesDebit.append(f"{debits[i][0]};{debits[i][1]}\n")
			#
			# sauvegarde(nomFichierSauvegardeVitesse, lignesVitesses)
			# sauvegarde(nomFichierSauvegardeDebit, lignesDebit)
			#
			# print(f"{nomRue}_{prefixe}{k + 1}", "écrit!")

# Les données intéressantes sont le 28 janvier
donnees = donnees["1-28"]

# liste des informations à écrire dans les fichiers
ligneDebits = []
ligneVitesses = []

a = {}

for heure in donnees:
	minutes = donnees[heure]
	for minute in minutes:
		segment = minutes[minute]
		# heure, minute = tronqueHeure(segment["Horodatage"])
		debit = segment["Débit"]
		vitesse = segment["Vitesse"]

		temps = heure + minute / 60
		# if cle not in a:
		# 	a[cle] = 0
		#
		# a[cle] += 1

		ligneDebits.append([temps, debit])
		ligneVitesses.append([temps, vitesse])


# tmp = [(temps, a[temps]) for temps in a]
# tmp.sort()

# X = [tmp[i][0] for i in range(len(tmp))]
# Y = [tmp[i][1] for i in range(len(tmp))]
#
# plt.figure()
#
# plt.plot(X, Y)
#
# plt.show()


ligneDebits.sort()
ligneVitesses.sort()

prefixe = "P"
k = 0

os.makedirs(f"./vitesseVehicule/1-28/", exist_ok=True)
os.makedirs(f"./debitVehicule/1-28/", exist_ok=True)

nomFichierSauvegardeVitesse = f"./vitesseVehicule/1-28/{nomRue}_{prefixe}{k + 1}"
nomFichierSauvegardeDebit = f"./debitVehicule/1-28/{nomRue}_{prefixe}{k + 1}"

fichierDebit = open(nomFichierSauvegardeDebit, "w")
for ligneRaw in ligneDebits:
	temp = [str(ligneRaw[i]) for i in range(len(ligneRaw))]
	ligne = ",".join(temp) + "\n"
	fichierDebit.write(ligne)

fichierDebit.close()


fichierVitesse = open(nomFichierSauvegardeVitesse, "w")
for ligneRaw in ligneVitesses:
	temp = [str(ligneRaw[i]) for i in range(len(ligneRaw))]
	ligne = ",".join(temp) + "\n"
	fichierVitesse.write(ligne)

fichierVitesse.close()






