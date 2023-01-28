#!/bin/env python

import requests
import time
import datetime


def filename(dossier: str) -> str:
	currentTime = datetime.datetime.now()
	nom = f"{dossier}/{currentTime.month}_{currentTime.day}-{currentTime.hour}_{currentTime.minute}_{currentTime.second}.csv"

	return nom


dossier = "./donnees"
DT = 59  # en sec

while True:
	res = requests.get("https://data.loire-atlantique.fr/api/explore/v2.1/shared/datasets/244400404_fluidite-axes-routiers-nantes-metropole@nantesmetropole/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&csv_separator=%3B")

	nom_fichier = filename(dossier)
	file = open(filename(dossier), "w")

	file.write(res.text)

	file.close()
	print(f"{nom_fichier} written")
	time.sleep(DT)



