#!/bin/env python

import os


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


	# print(f"nb donnees: {len(donnees)}")
	return donnees


def tronqueHeure(heure: str):
	"""
		converti une heure au format 2023-01-26T12:39:00+01:00
		en une heure au format HH:mm
	"""
	_, p1 = heure.split("T")
	h, m, _, _ = p1.split(":")

	# return f"{h}:{m}:00+01:00"
	return int(h), int(m)


def convertionHeure(heure: str):
	"""
		converti une heure au format 2023-01-26T12:39:00+01:00
		en une heure au format HH:mm
	"""
	_, p1 = heure.split("T")
	h, m, _, _ = p1.split(":")

	return int(h) + int(m) / 60  # f"{h}:{m}"


def moyenneGlissante(data: list[int | float], n: int):
	out: list[float] = [0 for _ in data]
	out[0] = data[0]

	for i in range(1, len(data)):
		if i < n:
			for j in range(i):
				out[i] += data[j]
			out[i] /= i

		elif i >= n:
			for j in range(n):
				out[i] += data[i - j]
			out[i] /= n

	return out


def readSauvegarde(cheminFichier: str, separateur=";"):
	donnees = []
	fichier = open(cheminFichier, "r")

	lignesFichier = fichier.readlines()

	entete = lignesFichier[0].replace("\n", "").split(separateur)

	for i in range(1, len(lignesFichier)):
		ligneFichier = lignesFichier[i].replace("\n", "")
		ligne = {}

		cellules = ligneFichier.split(separateur)
		for i in range(len(entete)):
			ligne[entete[i]] = cellules[i]

		donnees.append(ligne)

	return donnees


def extraitDonneesAvecMoyenne(donneesSegment, colonne: str) -> tuple[list[float], list[float]]:
	"""
	"""
	def triInstants(liste):
		"""
		Tri bulle
		"""
		for i in range(len(liste)):
			for j in range(len(liste) - 1 - i):
				if liste[j][0] > liste[j + 1][0]:
					c = liste[j + 1]
					liste[j + 1] = liste[j]
					liste[j] = c


	tmpVals = {}  # moyenne des donnéees pour chaque instants de la journée
	tmpCompte = {}  # Compte du nombre de données par instants

	# Permet de faire la moyenne à chaque instant de la journée,
	# Prend des données de plusieurs jours
	for el in donneesSegment:
		temps = convertionHeure(el['Horodatage'])  # Instant de la journée
		# temps = tronqueHeure(el['Horodatage'])
		if temps not in tmpVals:
			tmpVals[temps] = 0
		tmpVals[temps] += float(el[colonne])

		if temps not in tmpCompte:
			tmpCompte[temps] = 0
		tmpCompte[temps] += 1

	# On divise par le compte, ie fait la moyenne
	for i in tmpVals:
		tmpVals[i] /= tmpCompte[i]

	temps = []
	vals = []
	for i in tmpVals:
		temps.append(i)
		vals.append(tmpVals[i])


	jsp = [(temps[i], vals[i]) for i in range(len(temps))]
	# triInstants(jsp)
	jsp.sort()

	temps, vals = [], []
	for i in range(len(jsp)):
		temps.append(jsp[i][0])
		vals.append(jsp[i][1])

	return temps, vals

