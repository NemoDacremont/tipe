

import matplotlib.pyplot as plt
from constantes import V0, A, DIST_MAX, DT
from manipulationDonnees import extraitVitesseMoyenne1, extraitVitesseMoyenne, moyenneGlissante


def afficheVoituresIndividuellement(voitureIDs, tempsVoitures,
	donneesPlotVoitures, n, distMax=DIST_MAX, v_0=V0, a=A):
	"""
	affiche les voitures 0 à n - 1
	"""
	for voitureID in voitureIDs[:n]:
		# Affichage position
		plt.figure()
		ID = voitureID

		plt.ylim(top=distMax + 100, bottom= -100)
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


def afficheFeuxIndividuellement(feuIDs, tempsFeux,
	donneesPlotFeux, n):
	for feuID in list(feuIDs.keys())[:n]:
		# Affichage etat
		plt.figure()
		ID = feuID

		plt.title(f"etat du feu {feuID} en fonction du temps, position: {feuIDs[feuID]}")
		plt.plot(tempsFeux[ID], donneesPlotFeux["etat"][ID],
			label="vitesse de la voiture 0")


def affichePositionVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures,
		distMax=DIST_MAX, legend=False):
	"""
		Superpose la position de toutes les voitures en fonction du temps dans un
		même graphe
	"""
	plt.title("Position des voitures en fonction du tempsVoitures")
	for voitureID in voitureIDs:
		plt.ylim(top=distMax + 100, bottom=-100)
		plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["x"][voitureID],
			label=f"position de la voiture {voitureID}")

	if legend:
		plt.legend()


def afficheVitesseVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures,
		v_0=V0, legend=False):
	plt.figure()

	plt.title("Vitesse des voitures en fonction du tempsVoitures")
	for voitureID in voitureIDs:
		plt.ylim(top=v_0 + 1, bottom=-v_0 - 1)
		plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["vx"][voitureID],
			label=f"vitesse de la voiture {voitureID}")

	if legend:
		plt.legend()


def afficheAccelerationVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures,
		a=A, legend=False):
	plt.figure()

	plt.title("Accélération des voitures en fonction du tempsVoitures")
	for voitureID in voitureIDs:
		plt.ylim(top=a + 1, bottom=-a - 1)
		plt.plot(tempsVoitures[voitureID], donneesPlotVoitures["ax"][voitureID],
			label=f"accélération de la voiture {voitureID}")

	if legend:
		plt.legend()


def afficheVitessesMoyennes(donneesVoitures, vitessesReelles, dt=DT):
	nombreParties = int(len(donneesVoitures) * dt / 60)
	taillePartie = int(len(donneesVoitures) / nombreParties)

	vitessesMoyennes_instants = extraitVitesseMoyenne1(donneesVoitures)
	# vitessesMoyennes_instants = moyenneGlissante(vitessesMoyennes_instants, 1500)

	indicesVitesse = [i * dt for i in range(len(vitessesMoyennes_instants))]

	plt.figure()
	plt.title("Vitesse moyenne")
	plt.plot(indicesVitesse, vitessesMoyennes_instants, "+-", label="Vitesse simulation")

	# / 100 car centisecondes vers secondes
	indicesVitesse = [(i * taillePartie) / 100 for i in range(len(vitessesReelles))]
	# vitReelles = moyenneGlissante(vitessesReelles, 15)
	plt.plot(indicesVitesse, vitessesReelles, "+-", label="Vitesse réelle")

	plt.xlabel("temps (en s)")
	plt.ylabel("vitesse (en m/s)")
	plt.legend()


def afficheVitessesMoyennesMinutes(donneesVoitures, vitessesReelles, dt=DT):
	dureeMoyenne = 60

	nombreParties = int(len(donneesVoitures) * dt / dureeMoyenne)
	taillePartie = int(len(donneesVoitures) / nombreParties)

	vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, dureeMoyenne)

	# / 100 car centisecondes vers secondes
	temps = [(i * taillePartie) / 100 for i in range(nombreParties)]

	vitessesMoyennes_minutes = moyenneGlissante(vitessesMoyennes_minutes, 4)

	plt.figure()
	plt.title("Vitesse moyenne minutes")
	plt.plot(temps, vitessesMoyennes_minutes, "+-", label="Vitesse simulation")


	dureeMoyenne = 60
	nombreParties = int(len(donneesVoitures) * dt / dureeMoyenne)
	taillePartie = int(len(donneesVoitures) / nombreParties)

	indicesVitesse = [(i * taillePartie) / 100 for i in range(nombreParties)]
	# On affiche à partir de 1 pour faire joli
	vitessesReelles = moyenneGlissante(vitessesReelles, 4)
	plt.plot(indicesVitesse, vitessesReelles[1:], "+-", label="Vitesse réelle")

	plt.xlabel("temps (en s)")
	plt.ylabel("vitesses moyennes (en m/s)")
	plt.legend()


def afficheEcartAuReel(donneesVoitures, vitessesReelles, dt=DT):
	"""
		Affiche l'écart au réel de la simulation
	"""
	nombreParties = int(len(donneesVoitures) * DT / 60)
	taillePartie = int(len(donneesVoitures) / nombreParties)

	vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)

	eps = [vitessesMoyennes_minutes[i] - vitessesReelles[i] for i in range(len(vitessesReelles) - 1)]
	indicesVitesse = [(i * taillePartie) / 100 for i in range(len(vitessesReelles) - 1)]

	plt.figure()
	plt.title("Écart Vitesse moyenne minutes")
	plt.plot(indicesVitesse, eps, label="ecart vitesse")

	plt.xlabel("temps (en sec)")
	plt.ylabel("Ecart (en m/s)")
	plt.legend()



def show():
	plt.show()



