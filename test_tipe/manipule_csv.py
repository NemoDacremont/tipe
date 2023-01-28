
import os
import requests
import zipfile

#Module écrit par Nemo et relu par Anaël

def ouvre_fichier(chemin, encodage="utf8"):
	"""
		Entrée: - chemin: string, chemin vers le fichier à ouvrir
		Retourne: objet File, fichier ouvert

		Envoie une erreur si le fichier n'éxiste pas
	"""

	if os.path.isfile(chemin):
		return open(chemin, "r", encoding=encodage)

	raise ValueError("file doesn't exists")

def parse_CSV(chemin, encodage="utf8", separator=",", remove_header=False):
	"""
		Entrée: - chemin: string, chemin vers un fichier ou un dossier,
							Si fichier: le fichier doit être au format CSV
								Si dossier: les fichiers qu'il contient doivent être au format CSV
						- encodate: string, caractérise l'encodage du fichier
						- separator: séparateur utilisé dans le fichier CSV

		Retourne: Liste de listes au format [[str, timecode],..., [str, timecode]]
							où str caractérise un caractère et timecode est un flottant
        
        Remarque : si la commande renvoie Error : list index out of range, essayez de mettre en argument separator = ';'.
        Il arrive que les csv se fassent en utilisant , ou ; comme séparateur
	"""

	## Récupère les fichiers CSV pour les lires
	fichiers = []

	if os.path.isfile(chemin):
		fichiers.append(ouvre_fichier(chemin, encodage))

	elif os.path.isdir(chemin):
		# liste_fichier: ['nom_fichier1', 'nom_dossier1', 'nom_fichier2']
		liste_fichier = os.listdir(chemin)
		for nom_fichier in liste_fichier:
			chemin_fichier = f"{chemin}/{nom_fichier}"
			if os.path.isfile(chemin_fichier):
				fichiers.append(ouvre_fichier(chemin_fichier, encodage))

	## parse les fichiers ouverts
	data = []

	for fichier in fichiers:
		lines = fichier.readlines()

		start = 0
		if remove_header:
			start = 1

		for i in range(start, len(lines)):
			line = lines[i]
			# permet de parser une ligne: ["valeur1","valeur2"]
			raw = line.split(separator)

			# on retire le caractère newline
			raw[-1] = raw[-1].replace("\n", "")

			data.append(raw)

		fichier.close()

	return data

def parse_data(chemin, encodage="utf8", separator=",", has_header=False):
	"""
		Entrée: - chemin: string, chemin vers le fichier à ouvrir qui doit être
							un fichier CSV au format: 'valeur,timecode' avec timecode un flottant
						- encodate: string, caractérise l'encodage du fichier
						- separator: séparateur utilisé dans le fichier CSV
						- has_header: booléen caractérisant la présence de header dans le fichier à ouvrir

		Retourne: Liste de listes au format [str, timecode] où str caractérise un caractère et 
							timecode est un flottant, à noter que le header est retiré de la liste
	"""
	data = parse_CSV(chemin, encodage, separator)

	# Retire le header du fichier si le fichier en a un
	if has_header:
		data.pop(0)

	# convertit les timecode en float
	for i in range(len(data)):
		data[i][1] = float(data[i][1])
	
	return data

def download_from_server(ip, destination="data"):
	## Récupère le fichier zip du serveur et le stocke dans le fichier tmp.zip
	chemin_fichier_zip = f"{os.path.dirname(__file__)}/tmp.zip"
	chemin_final = f"{os.path.dirname(__file__)}/" + destination
	fichier_zip = open(chemin_fichier_zip, "wb+")

	requete_zip = requests.get(f"http://{ip}/telecharge")

	#fichier_zip.write(requete_zip.text.encode())

	for chunk in requete_zip.iter_content(chunk_size=512):
			if chunk:  # filter out keep-alive new chunks
					fichier_zip.write(chunk)

	## on le décompresse dans le dossier data
	extracteur = zipfile.ZipFile(fichier_zip)

	extracteur.extractall(chemin_final)

	extracteur.close()



	return chemin_final



if __name__ == "__main__":
	download_from_server("127.0.0.1:8080")






