
import numpy as np
from copy import deepcopy, copy
from constantes import DEBUT, FIN, DT, DIST_MAX

Temps = list[float] | list[int]

PHYSIQUE_DEFAUT = {
	"x": 0,
	"vx": 0,
	"ax": 0,
	"s_star": 0
}


def lireFichierDebit(nomFichier: str, separateur=';') -> list[float]:
	"""
		Lit un fichier CSV au format temps;debit
	"""
	debits = []
	fichier = open(nomFichier, 'r')

	lignes = fichier.readlines()

	fichier.close()


	for ligne in lignes:
		valeurs = ligne.replace("\n", "").split(";")
		_, debit = valeurs

		debits.append(float(debit) / 3600)

	return debits


def lireFichierVitesse(nomFichier: str, separateur=';') -> list[float]:
	"""
		Lit un fichier CSV au format temps;vitesse
	"""
	vitesses = []
	fichier = open(nomFichier, 'r')

	lignes = fichier.readlines()

	fichier.close()


	for ligne in lignes:
		valeurs = ligne.replace("\n", "").split(";")
		_, vitesse = valeurs

		vitesses.append(float(vitesse))

	return vitesses


def creeVoiture(ID: int, v_0: float, T: float, a: float, b: float, delta: int, l: float,
		s_0: float, s_1: float, physique=PHYSIQUE_DEFAUT, voiture_suivie=None):
	"""
		Cree un dictionnaire codant une voiture
		paramètres:
			- v_0: float, vitesse désirée en m/s
			- T: float, en s
			- a: float, accélération maximale, en m/s^2
			- b: float, accélération "confortable", préférera freiner selon b, en m/s^2
			- delta: int, puissance pour l'accélération, sans unité
			- l: float, longueur de la voiture, en m
			- s_0: float
			- s_1: float
	"""
	physique = copy(physique)
	if voiture_suivie:
		vx = physique["vx"]
		delta_v = voiture_suivie["physique"]["vx"] - vx
		physique["s_star"] = s_0 + s_1 * np.sqrt(vx / v_0) + T * vx + (vx * delta_v) / (2 * np.sqrt(a * b))

	return {
		"ID": ID,
		"physique": physique,
		"v_0": v_0,
		"T": T,
		"a": a,
		"b": b,
		"delta": delta,
		"l": l,
		"s_0": s_0,
		"s_1": s_1,
		"etat": {}
	}


def creeFeu(id: int, position: float, periode: float, dureeOrange: float) -> dict:
	feu = {
		"ID": id,
		"position": position,
		"periode": periode,
		"dureeOrange": dureeOrange,
		"tempsRestant": periode,
		"etat": "vert"
	}

	return feu


def metAJourFeu(feu: dict, dt: float) -> None:
	feu["tempsRestant"] -= dt
	if feu["etat"] == "vert":
		if feu["tempsRestant"] <= 0:
			feu["tempsRestant"] = feu["dureeOrange"]
			feu["etat"] = "orange"
			# print("feu passe au orange")

	if feu["etat"] == "orange":
		if feu["tempsRestant"] <= 0:
			feu["tempsRestant"] = feu["periode"]
			feu["etat"] = "rouge"
			# print("feu passe au rouge")

	if feu["etat"] == "rouge":
		if feu["tempsRestant"] <= 0:
			feu["tempsRestant"] = feu["periode"]
			feu["etat"] = "vert"
			# print("feu passe au vert")



def metAJourAcceleration(voitures: list, feux: list, alpha: int) -> None:
	"""
		Calcule l'accélération à l'instant t+1 de la voiture d'indice alpha
		Paramètres:
			- voitures: list[Voiture], liste des voitures du système
			- feux: list[Feu], liste des voitures du système
			- alpha: int, voiture considérée
	"""
	voiture = voitures[alpha]
	physique = voiture["physique"]

	# On récupère les données pour plus de lisibilité
	a, v_0, delta = voiture["a"], voiture["v_0"], voiture["delta"]
	s_0, s_1, T, b = voiture["s_0"], voiture["s_1"], voiture["T"], voiture["b"]
	x, vx, ax, s_star = physique["x"], physique["vx"], physique["ax"], physique["s_star"]


	# Si la voiture en suit une autre
	if alpha > 0:
		voiture_suivie = voitures[alpha - 1]

		delta_v = voiture_suivie["physique"]["vx"] - vx
		s_alpha = voiture_suivie["physique"]["x"] - x - voiture["l"]

	# Si la voiture correspond à la voiture de tête
	else:
		# On considère alors s_alpha infini et delta_v = 0
		delta_v = 0
		s_alpha = +np.infty

		# # On recalcule s_star dans un premier temps
		# physique["s_star"] = s_0 + s_1 * np.sqrt(abs(vx / v_0)) + T * vx
		#
		# # On peut alors calculer l'accélération
		# voiture["physique"]["ax"] = a * (1 - (vx / v_0)**delta)

	for feu in feux:
		if feu["etat"] == "rouge" or feu["etat"] == "orange":
			# si les conditions sont respectées,
			# on simule un véhicule virtuel arrêté au niveau du feu
			if x < feu["position"]:
				# On teste s'il n'y a pas de véhicule entre le feu et la voiture courrante
				if alpha == 0 or voitures[alpha - 1]["physique"]["x"] > feu["position"]:
					delta_v = 0 - vx  # la vitesse du véhicule virtuel est nulle
					s_alpha = feu["position"] - x - voiture["l"]


	# if voiture["ID"] == 5:
	# 	# print("deltav, s_alpha:", delta_v, voitures[alpha - 1]["physique"]["vx"] - vx, s_alpha)
	# On recalcule s_star dans un premier temps
	if s_alpha < 10**-6:
		s_alpha = 10**-6
	

	physique["s_star"] = s_0 + s_1 * np.sqrt(vx / v_0) + T * vx + (vx * delta_v) / (2 * np.sqrt(a * b))

	# On peut alors calculer l'accélération
	voiture["physique"]["ax"] = a * (1 - (vx / v_0)**delta - (physique["s_star"] / s_alpha)**2)


def metAJourVoiture(voitures, feux: list, alpha: int, dt: float) -> None:
	"""
		Met complêtement à jour la voiture d'indice alpha
	"""
	voiture = voitures[alpha]
	physique = voiture["physique"]

	# Schéma d'intégration
	# Euler
	metAJourAcceleration(voitures, feux, alpha)
	dv = physique["ax"] * dt
	physique["vx"] = max(0, physique["vx"] + dv)
	# if voiture["ID"] == 5:
	# 	# print("a, v, s_star:", physique["ax"], physique["vx"], physique["s_star"])

	dx = physique["vx"] * dt
	physique["x"] += dx

	# Runge-Kutta ordre 2
	# dt /= 2
	# ax = physique["ax"]
	# vx = physique["vx"]
	#
	# metAJourAcceleration(voitures, feux, alpha)
	# dv1 = physique["ax"] * dt
	# dx1 = (physique["vx"] + dv1) * dt
	# physique["vx"] += dv1
	# physique["x"] += dx1
	#
	# metAJourAcceleration(voitures, feux, alpha)
	# dv2 = physique["ax"] * dt
	# dx2 = (physique["vx"] + dv2) * dt
	#
	#
	# physique["vx"] += (dv1 + dv2) * dt / 2
	# physique["x"] += dx2


def simulation(voitures: list, temps: Temps):
	donnees = [voitures]
	dt = temps[1] - temps[0]
	feux = []

	for i in range(1, len(temps)):
		v = deepcopy(donnees[-1])  # etat des voitures à t+1
		for alpha in range(len(v)):
			metAJourVoiture(v, feux, alpha, dt)

		# On ajoute les états des voitures à t+1
		donnees.append(v)

	return donnees


FEUX_DEFAUT = [
	creeFeu(0, 40, 26, 3),
	# creeFeu(1, DIST_MAX / 2, 20, 2),
	# creeFeu(2, 3 * DIST_MAX / 4, 20, 2),
]


def simulationEchelon(valeurEchelon: float, temps: Temps, v_0: float, T: float,
		a: float, b: float, delta: int, l: float, s_0: float, s_1: float,
		physique=PHYSIQUE_DEFAUT, distMax=1000, voituresDebut=[], feux=FEUX_DEFAUT):
	"""
		Simule une ligne droite par un échelon du flux de voiture
		Les voitures se déplacent sur un segment de 0 à distMax, au delà, elles sont
		retirée des voitures à mettre à jour
		parametre:
			- valeurEchelon: nombre de nouvelles voitures par secondes
			- temps: liste des temps
			... caractéristiques des voitures

		Ajout temporaire: il y a un feu à distMax / 2
	"""
	voitures = voituresDebut
	donneesVoitures = []
	donneesFeux = []
	timerVoiture = 0

	dt = temps[1] - temps[0]
	timerVoiture = 0

	ID = 0
	if len(voitures) > 0:
		ID = voitures[-1]["ID"] + 1

	for i in range(len(temps)):
		timerVoiture -= dt
		t = temps[i]

		# Teste s'il faut créer une nouvelle voiture
		if timerVoiture < 0:
			voitureSuivie = None
			if len(voitures) > 0:
				voitureSuivie = voitures[-1]

			timerVoiture = 1 / valeurEchelon

			physiqueVoiture = copy(physique)
			if len(voitures) > 0:
				x0 = min(voitures[-1]["physique"]["x"] - 2 * s_0, 0)
				# v0 = voitures[-1]["physique"]["vx"] / 2
				v0 = 0

				# print(f"x0: {x0}")
				# print(f"v0: {v0}")

				physiqueVoiture["x"] = x0
				physiqueVoiture["vx"] = v0

			nouvelleVoiture = creeVoiture(ID, v_0, T, a, b, delta, l, s_0, s_1,
				physiqueVoiture, voitureSuivie)
			voitures.append(nouvelleVoiture)
			# # print("création voiture", ID)
			# # print("nouvelleVoiture x:", nouvelleVoiture["physique"]["x"])
			# # print("elle suit la voiture", voitureSuivie)
			ID += 1


		# Deepcopy est nécessaire pour sauvegarder les voitures qui sont des dico
		copieVoiture = deepcopy(voitures)
		copieFeux = deepcopy(feux)

		donneesVoitures.append([])  # On sauvegarde l'instant
		donneesFeux.append([])  # On sauvegarde l'instant
		for voiture in copieVoiture:
			donneesVoitures[i].append((t, voiture))

		for feu in copieFeux:
			donneesFeux[i].append((t, feu))

		# Met à jour les feux:
		for feu in feux:
			metAJourFeu(feu, dt)

		# Met à jour les voitures
		for alpha in range(len(voitures)):
			metAJourVoiture(voitures, feux, alpha, dt)  # Met à jour la voiture alpha

		# Retire les voitures étant à plus de distMax
		for alpha in range(len(voitures) - 1, -1, -1):
			voiture = voitures[alpha]
			if voiture["physique"]["x"] >= distMax:
				# print("retire voiture ID:", voiture["ID"])
				voitures.pop(alpha)


	return donneesVoitures, donneesFeux, voitures, feux


def simulationRue(debitRue: list[float], v_0: float, T: float, a: float,
		b: float, delta: int, l: float, s_0: float, s_1: float,
		physique=PHYSIQUE_DEFAUT, distMax=1000, debut=DEBUT, fin=FIN, dt=DT):
	"""
		Fait une suite de simulation en échelon durant chacune 1 minute où avec
		debitRue est une liste des débits de voitures par minute de la rue
		correspondante.

		donneesVoitures: [
			i -> dict[id: int -> voiture]
		]
	"""
	donneesVoitures = []
	donneesFeux = []
	voitures = []
	feux = FEUX_DEFAUT

	for i in range(len(debitRue) - 1):
		debit = debitRue[i + 1]  # la moyenne des temps à simulée est en i+1
		temps = [fin * i + debut + k * dt for k in range(int((fin - debut) / dt))]

		donneesVoits, donneesF, voitures, feux = simulationEchelon(debit, temps, v_0, T, a, b, delta,
			l, s_0, s_1, physique, distMax, voitures, feux)


		donneesVoitures += donneesVoits
		donneesFeux += donneesF

	return donneesVoitures, donneesFeux




