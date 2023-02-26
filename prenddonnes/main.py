#!/bin/env python

import requests
import time
import datetime


def filename(dossier: str) -> str:
	currentTime = datetime.datetime.now()
	nom = f"{dossier}/{currentTime.month}_{currentTime.day}-{currentTime.hour}_{currentTime.minute}_{currentTime.second}.csv"

	return nom


def parseCSV(data: str, ID_entete="Identifiant", separateur=',',
		exclude_col={}):

	data = data.replace("\ufeff", "")
	lignes = data.split("\n")[:-1]

	entete = lignes[0].replace("\n", "").split(separateur)

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


def sauvegardeCSV(data: dict, cheminFichier: str, aUneEntete=True):
	"""
	"""
	file = open(cheminFichier, "w")

	entete = list(data[list(data.keys())[0]].keys())
	ligneEntete = str(entete).replace("[", "").replace("]", "") + "\n"

	file.write(ligneEntete)
	for cle in data:
		try:
			ligne = f"{data[cle][entete[0]]}"
			for el in entete[1:]:
				ligne += f";{data[cle][el]}"

			ligne += "\n"

			file.write(ligne)
		except:
			print(f"Erreur lors de l'écriture de la lignke {cle}")

	file.close()


dossier = "./donnees"
DT = 59  # en sec

while True:
	res = requests.get("https://data.loire-atlantique.fr/api/explore/v2.1/shared/datasets/244400404_fluidite-axes-routiers-nantes-metropole@nantesmetropole/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&csv_separator=%3B")

	nom_fichier = filename(dossier)


	csv = parseCSV(res.text, separateur=';', exclude_col={"Geométrie", "geo_point_2d\r"})

	sauvegardeCSV(csv, nom_fichier)

	print(f"{nom_fichier} written")
	time.sleep(DT)



