#!/bin/env python

import os


def ouvreCSV(cheminFichier: str, ID_entete="Identifiant", separateur=',', exclude_col={}):
	"""
		Renvoie sous la forme d'un dictionnaire de dictionnaire le contenu du fichier
		cheminFichier au format CSV

		
		ex:
		id_entete_i correspond à un exemple de valeur correspondant à ID_entete

		return {
			id_entete_1: { donnees_1 },
			id_entete_2: { donnees_2 },
			id_entete_3: { donnees_3 },
		}
	"""
	# Extrait entête et lignes
	fichier = open(cheminFichier, 'r', encoding='utf-8-sig')  # Cet encodage retire les BOM

	lignes = fichier.readlines()
	entete = lignes[0].replace("\n", "").split(separateur)

	fichier.close()

	# Stocke sous la forme d'un dictionnaire pour accélérer l'accès aux données et aux recherches
	out = {}

	for i in range(1, len(lignes)):  # On exclue l'entête
		ligne = lignes[i].replace("\n", "")
		els = ligne.split(separateur)

		l = {}
		for i in range(len(els)):
			if entete[i] not in exclude_col:
				l[entete[i]] = els[i]

		out[l[ID_entete]] = l

	return out


def readSegment(nomSegment: str, dossierDonnees="donnees"):
	"""
		Retourne les données d'un segment sous la forme d'une liste de dictionnaires

		ex: [
			{ "Nom du tronçon": nomSegment, "Horodatage": h1, ... },
			{ "Nom du tronçon": nomSegment, "Horodatage": h2, ... },
			{ "Nom du tronçon": nomSegment, "Horodatage": h3, ... },
			{ "Nom du tronçon": nomSegment, "Horodatage": h4, ... },
			{ "Nom du tronçon": nomSegment, "Horodatage": h5, ... },
		]

	"""
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


def extraitHorodatage(heure: str):
	"""
		converti une heure au format 2023-01-26T12:39:00+01:00
		en une heure au 
	"""
	date, p1 = heure.split("T")

	annee, mois, jour = date.split("-")
	h, m, _, _ = p1.split(":")

	horodatage = {
		"annee": int(annee),
		"mois": int(mois),
		"jour": int(jour),
		"m": int(m),
		"h": int(h),
	}
	return horodatage


def tronqueHeure(heure: str):
	"""
		converti une heure au format 2023-01-26T12:39:00+01:00
		retourne (heure, minute) au format d'un tuple d'entiers
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
	"""
		Moyenne glissante sur n valeurs
	"""
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


def readSauvegarde(cheminFichier: str, separateur=";") -> list:
	"""
		Lit un fichier 
	"""
	donnees = []

	# extrait les lignes et l'entête
	fichier = open(cheminFichier, "r")

	lignesFichier = fichier.readlines()

	fichier.close()

	# Entête
	entete = lignesFichier[0].replace("\n", "").split(separateur)

	# donnees en excluant l'entête
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
	jsp.sort()  # tri rapide lexicographique

	temps, vals = [], []
	for i in range(len(jsp)):
		temps.append(jsp[i][0])
		vals.append(jsp[i][1])

	return temps, vals

