#!/bin/env python
from traiteDonnees import extraitHorodatage, readSauvegarde, extraitDonneesAvecMoyenne, moyenneGlissante, readSegment, tronqueHeure
import matplotlib.pyplot as plt


def afficheDebit(fichier: str):
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


def somme(l):
	s = 0
	for el in l:
		s += el

	return s

N = 1
nomRue = "Strasbourg"
prefixes = ["P"]
exclude = []

for prefixe in prefixes:
	for k in range(N):
		if f"{prefixe}{k + 1}" not in exclude:
			nomSegment = f"{nomRue} {prefixe}{k + 1}"
			nomFichierLecture = f"./sousDonnees/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeVitesse = f"./vitesseVehicule/{nomRue}_{prefixe}{k + 1}"
			nomFichierSauvegardeDebit = f"./debitVehicule/{nomRue}_{prefixe}{k + 1}"

			segments = readSegment(nomSegment)
			vitesses = {}

			N = len(segments)

			for i in range(N):
				segment = segments[i]
				horodatage = extraitHorodatage(segment["Horodatage"])

				jour = horodatage["jour"]
				mois = horodatage["mois"]
				heure = horodatage["h"]

				cle = f"{mois}-{jour}"
				if cle not in vitesses:
					vitesses[cle] = [0 for i in range(24)]

				vitesses[cle][heure] += 1

				print(f"{i} / {N}, {cle}")


			valeurs = []
			for cle in vitesses:
				# print(vitesses[cle])
				# print(len(vitesses))
				# input()

				valeurs.append((cle, somme(vitesses[cle])))

				# plt.figure()
				#
				# plt.title(f"nombre de données par heure le {cle}")
				# plt.plot(vitesses[cle])
				#
				# plt.xlabel("heure (en h)")
				# plt.ylabel("nombre de données")

			valeurs.sort()
			X = [valeurs[i][0] for i in range(len(valeurs))]
			Y = [valeurs[i][1] for i in range(len(valeurs))]


			plt.figure()

			plt.title("Nombre de données par jours")

			for i in range(len(X)):
				plt.bar(X[i], Y[i], color="blue")

			plt.ylabel("Nombre de données")
			plt.xlabel("jour")

			plt.show()


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






