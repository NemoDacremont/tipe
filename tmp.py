
def transforme(donnees):
	chemin, poids = donnees

	chemin = [str(chemin[i]) for i in range(len(chemin))]
	texteChemin = ";".join(chemin)
	ligne = texteChemin + ',' + str(poids) + "\n"
	return ligne



donnees = [[1, 4, 32], 1]

texte = transforme(donnees)

print(texte)

