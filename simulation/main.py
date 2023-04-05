#!/usr/bin/env python

import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse
from constantes import V0, T, A, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, DEBUT, FIN, DT
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1, moyenneGlissante
from affichage import affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show



# Temps

temps = [DEBUT + DT * i for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

# donneesVoitures, donneesFeux = simulationEchelon(echelon, temps, V0, T, A, B,
# 	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)
N = 60
debits = lireFichierDebit("./debitVehicule/Allende_I2")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Allende_I2")[:N]
donneesVoitures, donneesFeux = simulationRue(debits, V0, T, A, B,
	DELTA, L, S0, S1, PHYSIQUE, DIST_MAX)


# Vitesses moyenne pour chaque instants
vitessesMoyennes_instants = extraitVitesseMoyenne1(donneesVoitures)

# Vitesses moyenne pour chaque minutes
vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)



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

# Affiche la vitesse moyenne des segments

nombreParties = int(len(donneesVoitures) * DT / 60)
taillePartie = int(len(donneesVoitures) / nombreParties)

plt.figure()
plt.title("Vitesse moyenne")
plt.plot(vitessesMoyennes_instants, label="Vitesse simulation")

indicesVitesse = [i * taillePartie for i in range(len(vitesses))]
plt.plot(indicesVitesse, vitesses, label="Vitesse réelle")

plt.legend()

plt.xlabel("temps (en sec)")

###

plt.figure()
plt.title("Vitesse moyenne minutes")
plt.plot(indicesVitesse, vitessesMoyennes_minutes, label="Vitesse simulation")

indicesVitesse = [i * taillePartie for i in range(len(vitesses))]
plt.plot(indicesVitesse, vitesses, label="Vitesse réelle")

plt.xlabel("temps (en sec)")
plt.legend()


# Affichage écart
eps = [vitessesMoyennes_minutes[i] - vitesses[i] for i in range(len(vitesses))]
eps2 = [(vitessesMoyennes_minutes[i] - vitesses[i])**2 for i in range(len(vitesses))]

plt.figure()
plt.title("Écart Vitesse moyenne minutes")
plt.plot(indicesVitesse, eps, label="ecart vitesse")
plt.plot(indicesVitesse, eps2, label="ecart type")

plt.xlabel("temps (en sec)")
plt.legend()

print(eps2)


# plt.plot(debits)

# Affichage position
show()
