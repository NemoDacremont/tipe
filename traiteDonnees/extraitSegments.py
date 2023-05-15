#!/bin/env python
from traiteDonnees import readSegment
from utils import sauvegardeListDictCSV


SEGMENT = "Strasbourg"
PREFIXES = ["I", "P"]
N = 3

EXCLUDE = []

for prefixe in PREFIXES:
	for i in range(N):
		if f"{prefixe}{i + 1}" not in EXCLUDE:
			nomSegment = f"{SEGMENT} {prefixe}{i + 1}"
			nomFichier = f"{SEGMENT}_{prefixe}{i + 1}"
			donnees = readSegment(nomSegment)
			sauvegardeListDictCSV(donnees, f"./sousDonnees/{nomFichier}")

			print(nomFichier, "fini")

