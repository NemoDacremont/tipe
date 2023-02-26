#!/bin/env python

import os



chemins = os.listdir("./donnees/")
print(chemins)

for chemin in chemins:
	fichier = open(chemin, "r")

	fichier.close()



