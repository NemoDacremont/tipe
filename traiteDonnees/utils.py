


def sauvegardeDicoCSV(data: dict, cheminFichier: str, aUneEntete=True):
	"""
	"""
	file = open(cheminFichier, "w")

	entete = list(data[list(data.keys())[0]].keys())
	ligneEntete = ";".join(entete)

	file.write(ligneEntete)
	for cle in data:
		try:
			ligne = f"{data[cle][entete[0]]}"
			for el in entete[1:]:
				ligne += f";{data[cle][el]}"

			ligne += "\n"

			file.write(ligne)
		except Exception:
			print(f"Erreur lors de l'écriture de la ligne {cle}")

	file.close()


def sauvegardeListDictCSV(data: list, cheminFichier: str):
	"""
		sauvegarde une liste de dictionnaires
	"""
	file = open(cheminFichier, "w")

	entete = list(data[0].keys())
	ligneEntete = ";".join(entete) + "\n"
	print(entete)

	file.write(ligneEntete)

	for dico in data:
		els = []
		for col in entete:
			els.append(dico[col])

		ligne = ";".join(els) + "\n"
		print(ligne)
		file.write(ligne)

	file.close()




