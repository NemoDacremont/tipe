
import matplotlib.pyplot as plt
from constantes import V0, A, DIST_MAX


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




def show():
	plt.show()



