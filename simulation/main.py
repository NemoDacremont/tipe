#!/usr/bin/env python

from simulation import simulationRue, lireFichierDebit
from constantes import V0, T, A, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, DEBUT, FIN, DT
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux
from affichage import affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show


# Valeurs par défaut, valeur conseillées par le papier
# Valeurs https://traffic-simulation.de/info/info_IDM.html

# Temps

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

# donneesVoitures, donneesFeux = simulationEchelon(echelon, temps, V0, T, A, B,
# 	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)
debits = lireFichierDebit("./DoulonP1")[:5]
donneesVoitures, donneesFeux = simulationRue(debits, V0, T, A, B,
	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)


voitureIDs, tempsVoitures, donneesPlotVoitures = convertiDonneesPlotVoitures(donneesVoitures)
feuIDs, tempsFeux, donneesPlotFeux = convertiDonneesPlotFeux(donneesFeux)

# print(donneesPlotVoitures.keys())

# Affichage
# Affichage pour les n premières voitures
# Affichage pour les n premiers feux

# Affichage pour toutes les voitures
# Affichage position
affichePositionVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)

# Affichage vitesse
afficheVitesseVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)

# Affichage accélération
afficheAccelerationVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)


# plt.plot(debits)

# Affichage position
show()
