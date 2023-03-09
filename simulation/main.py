#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy, copy

Temps = list[float] | list[int]

PHYSIQUE_DEFAUT = {
	"x": 0,
	"vx": 0,
	"ax": 0,
	"s_star": 0
}


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
		physique["s_star"] = s_0 + s_1 * np.sqrt(abs(vx / v_0)) + T * vx + (vx * delta_v) / (2 * np.sqrt(abs(a * b)))

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
		"s_1": s_1
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
			print("feu passe au orange")

	if feu["etat"] == "orange":
		if feu["tempsRestant"] <= 0:
			feu["tempsRestant"] = feu["periode"]
			feu["etat"] = "rouge"
			print("feu passe au rouge")

	if feu["etat"] == "rouge":
		if feu["tempsRestant"] <= 0:
			feu["tempsRestant"] = feu["periode"]
			feu["etat"] = "vert"
			print("feu passe au vert")



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
				if alpha == 0:
					print("voiture 0 rencontre un feu, x=", x, feu["position"])

				# On teste s'il n'y a pas de véhicule entre le feu et la voiture courrante
				if alpha == 0 or voitures[alpha - 1]["physique"]["x"] > feu["position"]:
					delta_v = 0 - vx  # la vitesse du véhicule virtuel est nulle
					s_alpha = feu["position"] - x - voiture["l"]
					break

	# On recalcule s_star dans un premier temps
	physique["s_star"] = s_0 + s_1 * np.sqrt(abs(vx / v_0)) + T * vx + (vx * delta_v) / (2 * np.sqrt(abs(a * b)))

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


def simulationEchelon(valeurEchelon: float, temps: Temps, v_0: float, T: float,
		a: float, b: float, delta: int, l: float, s_0: float, s_1: float,
		physique=PHYSIQUE_DEFAUT, distMax=1000):
	"""
		Simule une ligne droite par un échelon du flux de voiture
		Les voitures se déplacent sur un segment de 0 à distMax, au delà, elles sont
		retirée des voitures à mettre à jour
		parametre:
			- valeurEchelon: nombre de nouvelles voitures par secondes
			- temps: liste des temps
			... caractéristiques des voitures


		Ajout temporaire: il y a un feu ) distMax / 2

	"""
	voitures = []
	donneesVoitures = []
	donneesFeux = []
	timerVoiture = 0

	feux = [
		creeFeu(0, distMax / 4, 10, 5),
		creeFeu(1, distMax / 2, 10, 5),
		creeFeu(2, 3 * distMax / 4, 10, 5),
	]


	dt = temps[1] - temps[0]
	timerVoiture = 0

	ID = 0

	for i in range(len(temps)):
		timerVoiture -= dt

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

				print(f"x0: {x0}")
				print(f"v0: {v0}")

				physiqueVoiture["x"] = x0
				physiqueVoiture["vx"] = v0

			nouvelleVoiture = creeVoiture(ID, v_0, T, a, b, delta, l, s_0, s_1,
				physiqueVoiture, voitureSuivie)
			voitures.append(nouvelleVoiture)
			print("création voiture", ID)
			print("nouvelleVoiture x:", nouvelleVoiture["physique"]["x"])
			print("elle suit la voiture", voitureSuivie)
			ID += 1


		# Deepcopy est nécessaire pour sauvegarder les voitures qui sont des dico
		copieVoiture = deepcopy(voitures)
		copieFeux = deepcopy(feux)

		donneesVoitures.append([])  # On sauvegarde l'instant
		donneesFeux.append([])  # On sauvegarde l'instant
		for voiture in copieVoiture:
			donneesVoitures[i].append((i * dt, voiture))

		for feu in copieFeux:
			donneesFeux[i].append((i * dt, feu))

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
				print("retire voiture ID:", voiture["ID"])
				voitures.pop(alpha)

	return donneesVoitures, donneesFeux


# Valeurs par défaut, valeur conseillées par le papier
# Valeurs https://traffic-simulation.de/info/info_IDM.html
v_0 = 8.33  # 3.33
T = 1.3
a = 0.3  # 0.73
b = 2
delta = 4
l = 2
s_0 = 2
s_1 = 3

# Temps
debut = 0
fin = 100
dt = 0.01  # 0.01 sec


temps = [debut + dt * i for i in range(int((fin - debut) / dt))]

physique = {
	"x": 0,
	"vx": v_0,
	"ax": 0,
	"s_star": 0
}
echelon = 0.5  # Une voiture toutes les 2 sec
distMax = 1000
donneesVoitures, donneesFeux = simulationEchelon(echelon, temps, v_0, T, a, b,
	delta, l, s_0, s_1, physique, distMax)


# print(donneesVoitures)

voitureIDs = []
tempsVoitures = {}
donneesPlotVoitures = {
	"x": {},
	"vx": {},
	"ax": {},
	"s_star": {}
}
for j in range(len(donneesVoitures)):
	# donneesPlotVoitures["x"].append([])
	# donneesPlotVoitures["vx"].append([])
	# donneesPlotVoitures["ax"].append([])
	for i in range(len(donneesVoitures[j])):
		t, voiture = donneesVoitures[j][i]
		voitureID = voiture["ID"]

		if voitureID not in voitureIDs:
			voitureIDs.append(voitureID)

		# tempsVoitures
		if voitureID not in tempsVoitures:
			tempsVoitures[voitureID] = []
		tempsVoitures[voitureID].append(t)

		# x
		if voitureID not in donneesPlotVoitures["x"]:
			donneesPlotVoitures["x"][voitureID] = []
		donneesPlotVoitures["x"][voitureID].append(voiture["physique"]["x"])

		# s_star
		if voitureID not in donneesPlotVoitures["s_star"]:
			donneesPlotVoitures["s_star"][voitureID] = []
		donneesPlotVoitures["s_star"][voitureID].append(voiture["physique"]["s_star"])

		# vx
		if voitureID not in donneesPlotVoitures["vx"]:
			donneesPlotVoitures["vx"][voitureID] = []
		donneesPlotVoitures["vx"][voitureID].append(voiture["physique"]["vx"])

		# ax
		if voitureID not in donneesPlotVoitures["ax"]:
			donneesPlotVoitures["ax"][voitureID] = []
		donneesPlotVoitures["ax"][voitureID].append(voiture["physique"]["ax"])


# Traitement des feux
valeurs = {"vert": 0, "orange": 1, "rouge": 2}
feuIDs = {}  # id: position
tempsFeux = {}
donneesPlotFeux = {
	"etat": {},
}
for j in range(len(donneesFeux)):
	for i in range(len(donneesFeux[j])):
		t, feu = donneesFeux[j][i]
		feuID = feu["ID"]

		if feuID not in feuIDs:
			feuIDs[feuID] = feu["position"]

		# tempsFeux
		if feuID not in tempsFeux:
			tempsFeux[feuID] = []
		tempsFeux[feuID].append(t)

		# etat
		if feuID not in donneesPlotFeux["etat"]:
			donneesPlotFeux["etat"][feuID] = []

		etat = valeurs[feu["etat"]]
		donneesPlotFeux["etat"][feuID].append(etat)


# Affichage
# Affichage pour les n premières voitures
n = 1
for voitureID in voitureIDs[:n]:
	# Affichage position
	plt.figure()
	ID = voitureID

	plt.ylim(top=distMax + 100, bottom=-distMax - 100)
	plt.title(f"position de la voiture {ID} en fonction du tempsVoitures")
	plt.plot(tempsVoitures[ID], donneesPlotVoitures["x"][ID],
		label=f"vitesse de la voiture {ID}")


	# Affichage vitesse
	plt.figure()

	plt.ylim(top=v_0 + 1, bottom=-v_0 - 1)
	plt.title(f"vitesse de la voiture {ID} en fonction du tempsVoitures")
	plt.plot(tempsVoitures[ID], donneesPlotVoitures["vx"][ID],
		label=f"vitesse de la voiture {ID}")

	# Affichage s_star
	plt.figure()

	plt.ylim(top=100, bottom=-100)
	plt.title(f"s_star de la voiture {ID} en fonction du tempsVoitures")
	plt.plot(tempsVoitures[ID], donneesPlotVoitures["s_star"][ID],
		label=f"s_star de la voiture {ID}")


	# Affichage accélération
	plt.figure()

	plt.ylim(top=a + 1, bottom=-a - 1)
	plt.title(f"Accélération de la voiture {ID} en fonction du tempsVoitures")
	plt.plot(tempsVoitures[ID], donneesPlotVoitures["ax"][ID],
		label=f"vitesse de la voiture {ID}")

# Affichage pour les n premiers feux
n = 3
for feuID in list(feuIDs.keys())[:n]:
	# Affichage etat
	plt.figure()
	ID = feuID

	plt.title(f"etat du feu {feuID} en fonction du temps, position: {feuIDs[feuID]}")
	plt.plot(tempsFeux[ID], donneesPlotFeux["etat"][ID],
		label="vitesse de la voiture 0")


# Affichage pour toutes les voitures
# Affichage position
plt.title("Position des voitures en fonction du tempsVoitures")
for voitureID in voitureIDs:
	plt.ylim(top=distMax + 100, bottom=-distMax - 100)
	plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["x"][voitureID],
		label=f"position de la voiture {voitureID}")
# plt.legend()


# Affichage vitesse
plt.figure()

plt.title("Vitesse des voitures en fonction du tempsVoitures")
for voitureID in voitureIDs:
	plt.ylim(top=v_0 + 1, bottom=-v_0 - 1)
	plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["vx"][voitureID],
		label=f"vitesse de la voiture {voitureID}")
plt.legend()


# Affichage accélération
plt.figure()

plt.title("Accélération des voitures en fonction du tempsVoitures")
for voitureID in voitureIDs:
	plt.ylim(top=a + 1, bottom=-a - 1)
	plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["ax"][voitureID],
		label=f"accélération de la voiture {voitureID}")
# plt.legend()


plt.show()




