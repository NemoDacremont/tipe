
import os


def rename(filepath: str):
	fichier = open(filepath, "r")


	lignes = fichier.readlines()

	fichier.close()

	fichier = open(filepath, "w")

	entete = lignes[0]
	print(entete)
	entete = entete.replace("aux d'occ", "aux d@occ")
	entete = entete.replace("\"", "")
	entete = entete.replace(",", ";")
	entete = entete.replace("; ", ";")
	entete = entete.replace("'", "")
	entete = entete.replace("@", "'")

	entete = entete.replace("Nomdutronçon", "Nom du tronçon")
	entete = entete.replace("Tauxdoccupation", "Taux d'occupation")
	entete = entete.replace("Tempsdeparcours", "Temps de parcours")
	entete = entete.replace("Codecouleur", "Code couleur")

	entete = entete.replace("Etat du traficG", "Etat du trafi#")
	entete = entete.replace("Etat du trafic;", "Etat du trafi%")
	entete = entete.replace("Etat du trafic\n", "Etat du trafijsp")

	entete = entete.replace("Etat du trafic", "Etat du trafic\n")

	entete = entete.replace("Etat du trafi%", "Etat du trafic;")
	entete = entete.replace("Etat du trafi#", "Etat du trafic;G")
	entete = entete.replace("Etat du trafijsp", "Etat du trafic\n")

	entete = entete.replace("Etatdutrafic", "Etat du trafic\n")

	# print(entete)
	lignes[0] = entete

	for i in range(len(lignes) - 1, -1, -1):
		ligne = lignes[i]
		if ligne == "\n":
			lignes.pop(i)
			print("pop ligne", i)


	fichier.writelines(lignes)

	fichier.close()


i = 0
dossier = "donnees"
for file in os.listdir(dossier):
	print(f"renomme {file}")
	rename(f"{dossier}/{file}")
	i += 1






