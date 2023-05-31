
from constantes import DT


def moyenneGlissante(data: list[int | float], n: int) -> list[int | float]:
	out: list[float] = [0 for _ in data]
	out[0] = data[0]

	for i in range(1, len(data)):
		if i < n:
			for j in range(i):
				out[i] += data[j]
			out[i] /= i

		elif i >= n:
			for j in range(n):
				out[i] += data[i - j]
			out[i] /= n

	return out


def convertiDonneesPlotVoitures(donneesVoitures):
	"""
		Retourne un dictionnaire au format:
		voitureIDs: [ID: int],
		tempsVoiture: {
			ID_voiture: [temps t]
		},
		donneesPlotVoitures: {
			"x": {
				ID_voiture: [x à l'instant t]
			},
			"vx": {
				ID_voiture: [vx à l'instant t]
			},
			"ax": {
				ID_voiture: [ax à l'instant t]
			},
			"s_star": {
				ID_voiture: [s_star à l'instant t]
			}
		}
	"""
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

	return voitureIDs, tempsVoitures, donneesPlotVoitures


def convertiDonneesPlotFeux(donneesFeux):
	"""
		Retourne un dictionnaire au format:
		feuIDs: {
			ID: (position: int)
		},
		tempsFeux: {
			ID_voiture: [temps t]
		},
		donneesPlotFeux: {
			"etat": {
				IDFeu: [etat à l'instant t]
			}
		}

		etat \\in {0, 1, 2}
		valeurs = {"vert": 0, "orange": 1, "rouge": 2}
	"""
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

	return feuIDs, tempsFeux, donneesPlotFeux


def extraitVitesseMoyenne1(donneesVoitures):
	"""
		Retourne la vitesse moyenne pour les temps i * deltaT, i un entier
	"""
	vitessesMoyennes = [0.0 for _ in range(len(donneesVoitures))]

	for i in range(len(donneesVoitures)):
		N = 0
		voituresEls = donneesVoitures[i]
		for voitureEl in voituresEls:
			_, voiture = voitureEl
			vx = voiture["physique"]["vx"]
			vitessesMoyennes[i] += vx 
			N += 1

		if N != 0:
			vitessesMoyennes[i] /= N

	return vitessesMoyennes


def extraitVitesseMoyenne(donneesVoitures, deltaT: float, dt=DT):
	"""
		Retourne la vitesse moyenne pour les temps i * deltaT, i un entier
	"""
	nombreParties = int(len(donneesVoitures) * dt / deltaT)
	taillePartie = int(len(donneesVoitures) / nombreParties)
	vitessesMoyennes = [0.0 for _ in range(nombreParties)]
	# print(taillePartie, nombreParties)

	for i in range(nombreParties):
		N = 0
		for j in range(taillePartie):
			voituresEls = donneesVoitures[i * taillePartie + j]
			for voitureEl in voituresEls:
				_, voiture = voitureEl
				vx = voiture["physique"]["vx"]
				vitessesMoyennes[i] += vx 
				N += 1

		vitessesMoyennes[i] = vitessesMoyennes[i] / N

	return vitessesMoyennes


