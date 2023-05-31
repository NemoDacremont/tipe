#!/usr/bin/env python

# import matplotlib.pyplot as plt
from simulation import PHYSIQUE_DEFAUT, simulationRue, lireFichierDebit, lireFichierVitesse
from constantes import V0, T, A, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, DEBUT, FIN, DT
from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1
from affichage import afficheEcartAuReel, affichePositionVoitures, afficheVitesseVoitures, \
	afficheAccelerationVoitures, show, afficheVitessesMoyennes, afficheVitessesMoyennesMinutes

import socket as so
import sys

def sauvegardeVitesseCSV(cheminFichier: str, vitesses: list):
	fichier = open(cheminFichier, "a")

	for vitesse in vitesses:
		fichier.write(str(vitesse) + "\n")

	fichier.close()


def sauvegardeVoitures(cheminFichier: str, voitures, exclude={"etat": True}):
	fichier = open(cheminFichier, "w")

	if len(voitures) == 0:
		return


	entete = []
	for cle in voitures[0][1]:
		if cle not in exclude:
			entete.append(cle)

	fichier.write(",".join(entete) + "\n")


	for _, voiture in voitures:
		ligne = []
		for cle in entete:
			if cle == "physique":
				donnee = []
				physique = voiture[cle]
				for clePhysique in physique:
					donnee.append(f"{clePhysique}:{physique[clePhysique]}")

				ligne.append(";".join(donnee))

			else:
				ligne.append(voiture[cle])

		ligne = [str(ligne[i]) for i in range(len(ligne))]
		texte = ",".join(ligne) + "\n"

		fichier.write(texte)

	fichier.close()


def lireVoitures(cheminFichier: str):
	fichier = open(cheminFichier, "r", encoding='utf-8-sig')

	lignes = fichier.readlines()
	fichier.close()

	if len(lignes) == 0:
		return []

	voitures = []
	cles = lignes[0].replace("\n", "").split(",")
	
	for i in range(1, len(lignes)):
		ligne = lignes[i].replace("\n", "")
		donneesLigne = ligne.split(",")

		voiture = {}
		for j in range(len(cles)):
			cle = cles[j]

			if cle == "ID":
				voiture[cle] = int(donneesLigne[j])

			elif cle == "physique":
				physique = {}
				valeurs = donneesLigne[j]
				paquets = valeurs.split(";")

				for paquet in paquets:
					clePhysique, valeur = paquet.split(":")
					physique[clePhysique] = float(valeur)

				voiture[cle] = physique

			else:
				voiture[cle] = float(donneesLigne[j])

		voitures.append(voiture)

	return voitures


def sauvegardeFeux(cheminFichier: str, feux):
	fichier = open(cheminFichier, "w")

	entete = []
	for cle in feux[0][1]:
		entete.append(cle)

	fichier.write(",".join(entete) + "\n")


	for _, feu in feux:
		ligne = []
		for cle in entete:
			ligne.append(feu[cle])

		ligne = [str(ligne[i]) for i in range(len(ligne))]
		texte = ",".join(ligne) + "\n"

		fichier.write(texte)

	fichier.close()


def lireFeux(cheminFichier: str):
	fichier = open(cheminFichier, "r", encoding='utf-8-sig')

	lignes = fichier.readlines()
	fichier.close()

	if len(lignes) == 0:
		return []

	feux = []
	cles = lignes[0].replace("\n", "").split(",")
	
	for i in range(1, len(lignes)):
		ligne = lignes[i].replace("\n", "")
		donneesLigne = ligne.split(",")

		feu = {}
		for j in range(len(cles)):
			cle = cles[j]

			if cle == "etat":
				feu[cle] = str(donneesLigne[j])

			elif cle == "ID":
				feu[cle] = int(donneesLigne[j])

			else:
				feu[cle] = float(donneesLigne[j])

		feux.append(feu)

	return feux





# Temps
temps = [(DEBUT + DT * i) / 100 for i in range(int((FIN - DEBUT) / DT))]
echelon = 0.5  # Une voiture toutes les 2 sec

hostname = so.gethostname()


argv = sys.argv
N_OFFSET = 0
N = 1
a = A
v0 = V0
if len(argv) >= 2:
	N = int(argv[1])

if len(argv) >= 3:
	N_OFFSET = int(argv[2])

if len(argv) >= 4:
	a = float(argv[3])

if len(argv) >= 5:
	v0 = float(argv[4])

if N_OFFSET < 0:
	N_OFFSET = 0



print(a)
nomFichierSauvegardeTemporaireVoitures = f"./sim_tmp/{hostname}/voitures{a}_{v0}.csv"
nomFichierSauvegardeTemporaireFeux = f"./sim_tmp/{hostname}/feux{a}_{v0}.csv"
nomFichierSauvegardeVitesses = f"./vitessesSimulees/{hostname}/vitesses{a}_{v0}.csv"


# Véhicules / h
debits = lireFichierDebit("./debitVehicule/1-28/Strasbourg_P1")

# en km/h
vitesses = lireFichierVitesse("./vitesseVehicule/1-28/Strasbourg_P1")
# converti en m/s
vitesses = [vitesses[i] / 3.6 for i in range(len(vitesses))]


voituresInit = []  # lireVoitures(nomFichierSauvegardeTemporaireVoitures)
feuxInit = []  # lireFeux(nomFichierSauvegardeTemporaireFeux)


# print(voituresInit)
# input()

debits = [debits[N_OFFSET + i] for i in range(N + 1)]
vitesses = [vitesses[N_OFFSET + i] for i in range(N + 1)]

# Simulation
donneesVoitures, donneesFeux = simulationRue(debits, V0, T, a, B,
	DELTA, L, S0, S1, physique=PHYSIQUE, distMax=DIST_MAX, voituresInit=voituresInit
	, feuxInit=feuxInit)


# Vitesses moyenne pour chaque instants
vitessesMoyennes_instants = extraitVitesseMoyenne1(donneesVoitures)

# Vitesses moyenne pour chaque minutes
# vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)

voitureIDs, tempsVoitures, donneesPlotVoitures = convertiDonneesPlotVoitures(donneesVoitures)
feuIDs, tempsFeux, donneesPlotFeux = convertiDonneesPlotFeux(donneesFeux)

sauvegardeVitesseCSV(nomFichierSauvegardeVitesses, vitessesMoyennes_instants)
sauvegardeVoitures(nomFichierSauvegardeTemporaireVoitures, donneesVoitures[-1])
sauvegardeFeux(nomFichierSauvegardeTemporaireFeux, donneesFeux[-1])



"""
###
### Affichage
###
# Affichage position des voitures dans le temps
affichePositionVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)


# Affichage vitesse
afficheVitesseVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)


# Affichage accélération
afficheAccelerationVoitures(voitureIDs, tempsVoitures, donneesPlotVoitures)


# Vitesse moyenne des voitures à chaque instant et la vitesse réelle
afficheVitessesMoyennes(donneesVoitures, vitesses)


# Vitesse moyenne à chaque minute des voitures et la vitesse réelle
afficheVitessesMoyennesMinutes(donneesVoitures, vitesses)

# Ecart à chaque minute au réel
afficheEcartAuReel(donneesVoitures, vitesses, DT)


show()
"""


