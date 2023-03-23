#!/bin/env python
from traiteDonnees import readSegment
from utils import sauvegardeListDictCSV


for i in range(1, 8):
	nomSegment = f"Doulon P{i}"
	nomFichier = f"Doulon_P{i}"
	donnees = readSegment(nomSegment)
	sauvegardeListDictCSV(donnees, f"./sousDonnees/{nomFichier}")
	print(nomFichier, "fini")


for i in range(1, 8):
	nomSegment = f"Doulon I{i}"
	nomFichier = f"Doulon_I{i}"
	donnees = readSegment(nomSegment)
	sauvegardeListDictCSV(donnees, f"./sousDonnees/{nomFichier}")
	print(nomFichier, "fini")
