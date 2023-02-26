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


def metAJourAcceleration(voitures, alpha: int) -> None:
	"""
		Calcule l'accélération à l'instant t+1 de la voiture d'indice alpha
		Paramètres:
			- voitures: list[Voiture], liste des voitures du système
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

		# On recalcule s_star dans un premier temps
		physique["s_star"] = s_0 + s_1 * np.sqrt(abs(vx / v_0)) + T * vx + (vx * delta_v) / (2 * np.sqrt(abs(a * b)))

		# On peut alors calculer l'accélération
		voiture["physique"]["ax"] = a * (1 - (vx / v_0)**delta - (physique["s_star"] / s_alpha)**2)

	# Si la voiture correspond à la voiture de tête
	else:
		# On considère alors s_alpha infini et delta_v = 0

		# On recalcule s_star dans un premier temps
		physique["s_star"] = s_0 + s_1 * np.sqrt(abs(vx / v_0)) + T * vx

		# On peut alors calculer l'accélération
		voiture["physique"]["ax"] = a * (1 - (vx / v_0)**delta)


def metAJourVoiture(voitures, alpha: int, dt: float) -> None:
	"""
		Met complêtement à jour la voiture d'indice alpha
	"""
	metAJourAcceleration(voitures, alpha)
	voiture = voitures[alpha]
	physique = voiture["physique"]

	physique["vx"] += physique["ax"] * dt
	physique["x"] += physique["vx"] * dt


def simulation(voitures: list, temps: Temps):
	donnees = [voitures]
	dt = temps[1] - temps[0]

	for i in range(1, len(temps)):
		v = deepcopy(donnees[-1])  # etat des voitures à t+1
		for alpha in range(len(v)):
			metAJourVoiture(v, alpha, dt)

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

	"""
	voitures = []
	donnees = []
	timerVoiture = 0

	dt = temps[1] - temps[0]
	timerVoiture = 0

	ID = 0

	for i in range(len(temps)):
		timerVoiture -= dt
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
		donnees.append([])  # On sauvegarde l'instant
		for voiture in copieVoiture:
			donnees[i].append((i * dt, voiture))

		# Met à jour les voitures
		for alpha in range(len(voitures)):
			metAJourVoiture(voitures, alpha, dt)  # Met à jour la voiture alpha

		# Retire les voitures étant à plus de distMax
		for alpha in range(len(voitures) - 1, -1, -1):
			voiture = voitures[alpha]
			if voiture["physique"]["x"] >= distMax:
				print("retire voiture ID:", voiture["ID"])
				voitures.pop(alpha)

	return donnees


# Valeurs par défaut, valeur conseillées par le papier
v_0 = 8.33  # 3.33
T = 1.6
a = 1  # 0.73
b = 1.67
delta = 4
l = 2
s_0 = 2
s_1 = 3

# Temps
debut = 0
fin = 60
dt = 0.01  # 0.1 sec


temps = [debut + dt * i for i in range(int((fin - debut) / dt))]

physique = {
	"x": 0,
	"vx": v_0,
	"ax": 0,
	"s_star": 0
}
echelon = 0.3  # Une voiture toutes les 2 sec
distMax = 1000
donnees = simulationEchelon(echelon, temps, v_0, T, a, b, delta, l, s_0, s_1,
	physique, distMax)


# print(donnees)

# Isole la première voiture
voitureIDs = []
temps = {}
tmp = {
	"x": {},
	"vx": {},
	"ax": {}
}
for j in range(len(donnees)):
	# tmp["x"].append([])
	# tmp["vx"].append([])
	# tmp["ax"].append([])
	for i in range(len(donnees[j])):
		t, voiture = donnees[j][i]
		voitureID = voiture["ID"]

		if voitureID not in voitureIDs:
			voitureIDs.append(voitureID)

		# temps
		if voitureID not in temps:
			temps[voitureID] = []
		temps[voitureID].append(t)

		# x
		if voitureID not in tmp["x"]:
			tmp["x"][voitureID] = []
		tmp["x"][voitureID].append(voiture["physique"]["x"])

		# vx
		if voitureID not in tmp["vx"]:
			tmp["vx"][voitureID] = []
		tmp["vx"][voitureID].append(voiture["physique"]["vx"])

		# ax
		if voitureID not in tmp["ax"]:
			tmp["ax"][voitureID] = []
		tmp["ax"][voitureID].append(voiture["physique"]["ax"])



# Affichage
# Affichage pour les n premières voitures
n = 3
for voitureID in voitureIDs[:n]:
	# Affichage position
	plt.figure()
	ID = voitureID

	plt.title(f"position de la voiture {ID} en fonction du temps")
	plt.plot(temps[ID], tmp["x"][ID], label="vitesse de la voiture 0")


	# Affichage vitesse
	plt.figure()

	plt.title(f"vitesse de la voiture {ID} en fonction du temps")
	plt.plot(temps[ID], tmp["vx"][ID], label="vitesse de la voiture 0")


	# Affichage accélération
	plt.figure()

	plt.title(f"Accélération de la voiture {ID} en fonction du temps")
	plt.plot(temps[ID], tmp["ax"][ID], label="vitesse de la voiture 0")


# Affichage pour toutes les voitures
# Affichage position
plt.title("Position des voitures en fonction du temps")
for voitureID in voitureIDs:
	plt.ylim(top=distMax + 100, bottom=-distMax - 100)
	plt.plot(temps[voitureID], tmp["x"][voitureID], label=f"position de la voiture {voitureID}")
# plt.legend()


# Affichage vitesse
plt.figure()

plt.title("Vitesse des voitures en fonction du temps")
for voitureID in voitureIDs:
	plt.ylim(top=v_0 + 1, bottom=-v_0 - 1)
	plt.plot(temps[voitureID], tmp["vx"][voitureID], label=f"vitesse de la voiture {voitureID}")
plt.legend()


# Affichage accélération
plt.figure()

plt.title("Accélération des voitures en fonction du temps")
for voitureID in voitureIDs:
	plt.ylim(top=a + 1, bottom=-a - 1)
	plt.plot(temps[voitureID], tmp["ax"][voitureID], label=f"accélération de la voiture {voitureID}")
# plt.legend()


plt.show()




