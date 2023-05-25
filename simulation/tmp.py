# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:18:29 2023

@author: oscar
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt

Nb = 4  # Nombre de barres
longueur_barres = 10
diamètre_barre = 5  # en cm


def structure(Nb, longueur_barres):
	barres = []
	cord_barres = {}

	noeuds = 0
	noeuds_coordonnées = []
	noeuds_indices = {}

	# Définition des noeuds
	a = 0
	for x in range(0, Nb + 1, 1):
		for y in range(0, Nb - x + a + 1, 1):
			a = 1

			noeuds_coordonnées.append(
				[int(x * longueur_barres), int(y * longueur_barres)]
			)
			noeuds_indices[
				(int(x * longueur_barres), int(y * longueur_barres))
			] = noeuds
			noeuds = noeuds + 1

			# Définition des barres verticales
	a = 0
	n = 0
	for x in range(0, Nb + 1, 1):
		for y in range(1, Nb - x + a + 1, 1):
			a = 1
			ind1 = noeuds_indices[
				(int(x * longueur_barres), int((y - 1) * longueur_barres))
			]
			ind2 = noeuds_indices[(int(x * longueur_barres), int(y * longueur_barres))]

			barres.append([ind1, ind2])
			cord_barres[(ind1, ind2)] = n
			cord_barres[(ind2, ind1)] = n
			n = n + 1

			# Définition des barres horizontales

	for x in range(0, Nb, 2):
		# for y in range(0, Nb-b, 1):
		for y in range(0, Nb - x, 1):
			ind1 = noeuds_indices[
				(int(x * longueur_barres), int((y) * longueur_barres))
			]
			ind2 = noeuds_indices[
				(int((x + 1) * longueur_barres), int((y + 1) * longueur_barres))
			]

			barres.append([ind1, ind2])
			cord_barres[(ind1, ind2)] = n
			cord_barres[(ind2, ind1)] = n

			n = n + 1

			# Définition des barres obliques
	for x in range(1, Nb, 2):
		for y in range(1, Nb - (x - 1), 1):
			# for y in range(1, Nb-c, 1):

			ind1 = noeuds_indices[
				(int(x * longueur_barres), int((y) * longueur_barres))
			]
			ind2 = noeuds_indices[
				(int((x + 1) * longueur_barres), int((y - 1) * longueur_barres))
			]

			barres.append([ind1, ind2])
			cord_barres[(ind1, ind2)] = n
			cord_barres[(ind2, ind1)] = n

			n = n + 1

	d = 0
	for y in range(0, Nb + 1, 1):
		for x in range(0, Nb - y + d, 1):
			d = 1

			ind1 = noeuds_indices[
				(int(x * longueur_barres), int((y) * longueur_barres))
			]
			ind2 = noeuds_indices[
				(int((x + 1) * longueur_barres), int((y) * longueur_barres))
			]

			barres.append([ind1, ind2])
			cord_barres[(ind1, ind2)] = n
			cord_barres[(ind2, ind1)] = n

			n = n + 1
	return noeuds_coordonnées, noeuds_indices, barres, cord_barres


def longueur_b(barres, noeuds_coordonnées):
	longueur_barres = np.zeros((len(barres)))
	for l in range(len(barres)):
		n1_x = noeuds_coordonnées[barres[l][0]][0]
		n2_x = noeuds_coordonnées[barres[l][1]][0]
		n1_y = noeuds_coordonnées[barres[l][0]][1]
		n2_y = noeuds_coordonnées[barres[l][1]][1]

		longueur_barres[l] = sqrt((n2_x - n1_x) ** 2 + (n2_y - n1_y) ** 2)
	return longueur_barres


def masse__voisins(noeuds_coordonnées, diamètre_barre):
	longueur_barres = longueur_b(barres, noeuds_coordonnées)
	# densité en g.cm**-3
	densite_acier = 7.83
	g = 9.81
	u = [0, -1]

	# masse de chaque barre
	masse_barres = np.zeros((len(longueur_barres)))
	for l in range(len(longueur_barres)):
		masse_barres[l] = (
			densite_acier * pi * (diamètre_barre) ** 2 * longueur_barres[l]
		)

	# masse assicié aux noeuds

	masse_noeuds = np.zeros((len(noeuds_coordonnées)))

	# voisin de chaque noeuds
	voisins = {}
	for n in range(len(noeuds_coordonnées)):
		voisins[n] = []
		for m in range(len(barres)):
			if barres[m][0] == n:
				voisins[n].append(barres[m][1])

				masse_noeuds[n] = masse_noeuds[n] + masse_barres[m] / 2
			if barres[m][1] == n:
				voisins[n].append(barres[m][0])

				masse_noeuds[n] = masse_noeuds[n] + masse_barres[m] / 2

	# definition du poids
	P = np.zeros((len(noeuds_coordonnées), 2))
	for i in range(len(masse_noeuds)):
		P[i] = np.dot(masse_noeuds[i] * g, u)

	return masse_noeuds, voisins, P


def vecteur_unitaire(noeuds_coordonnées, longueur_barres):
	U = []
	for j in range(len(barres)):
		print(u)
		norme = longueur_barres[j]
		u = np.zeros(2)

		# vecteur unitaire pour chaque barre
		u[0] = (
			noeuds_coordonnées[barres[j][1]][0] - noeuds_coordonnées[barres[j][0]][0]
		) / norme
		u[1] = (
			noeuds_coordonnées[barres[j][1]][1] - noeuds_coordonnées[barres[j][0]][1]
		) / norme
		U.append(u)

	return U


def hooke(barres, noeuds_coordonnées, diamètre_barre, l0, voisins, cord_barres):
	E = 220  # en GPa
	S = pi * diamètre_barre**2

	# longueur des barres
	l_b = longueur_b(barres, noeuds_coordonnées)

	# definition vecteur unitaire
	u_barres = vecteur_unitaire(noeuds_coordonnées, l_b)
	F_h = np.zeros((len(barres) * 2, 2))

	# nombre de force elastique associé  chaque noeud
	Nb_h = []

	b = 0
	for i in range(len(noeuds_coordonnées)):
		Nb = 0
		for j in range(len(voisins[i])):
			Nb = Nb + 1

			ib = cord_barres[(i, voisins[i][j])]

			l = l_b[ib]
			u = u_barres[ib]

			# sens de la force
			if i == barres[ib][0]:
				sens = 1
			else:
				sens = -1

			F_h[b, 0] = sens * (1 / l0[ib]) * E * S * (l - l0[ib]) * u[0]
			F_h[b, 1] = sens * (1 / l0[ib]) * E * S * (l - l0[ib]) * u[1]
			b = b + 1
		Nb_h.append(Nb)

	return F_h, Nb_h


def f_spec():
	pass


# resultante des forces


def resultante(Nb_h, noeuds_coordonnées, voisins, l0, cord_barres, barres):
	f_hooke, Nb_h = hooke(
		barres, noeuds_coordonnées, diamètre_barre, l0, voisins, cord_barres
	)
	a, b, P = masse__voisins(noeuds_coordonnées, diamètre_barre)
	resultante = np.zeros((len(noeuds_coordonnées), 2))
	for i in range(len(noeuds_coordonnées)):
		for j in range(Nb_h[i]):
			resultante[i] = P[i] + f_hooke[j]
	return resultante


# méthode d'Euler implicite


def derivée(position, vitesse, Nb_h, l0, cord_barres, barres, indice):
	m, voisins, Nb_h = masse__voisins(position, diamètre_barre)
	m = m[indice]
	# calcule la dérive de la position et la dérive de la vitesse
	return (
		vitesse,
		(1 / m) * resultante(Nb_h, position, voisins, l0, cord_barres, barres)[indice],
	)


def Euler(position_0, v_0, h, t_m):
	t = np.arange(0, t_m, h)
	n = int(t_m / h)
	position = np.zeros((n, 2))
	position[0, 1] = position_0[0]
	position[0, 1] = position_0[1]
	v = np.zeros((n, 2))
	for i in range(n - 1):
		dposition, dv = derivée(position, v[i], Nb_h, l0, cord_barres, barres, 1)

		position[i + 1, 0] = position[i, 0] + h * dposition[0]
		position[i + 1, 1] = position[i, 1] + h * dposition[1]
		v[i + 1, 0] = v[i, 0] + h * dv[0]
		v[i + 1, 1] = v[i, 1] + h * dv[1]
	return position, v, t


#
# def euler( Te, t_m, Nb_h,coordonnée):
# 	t = np.arange(0, t_m, Te)
# 	a=[]
# 	masse_n, voisins, P = masse__voisins(noeuds_coordonnées, diamètre_barre)
# 	position=np.zeros((np.size(t),2))
# 	n1=noeuds_coordonnées[1]
# 	for i in range(np.size(t)):
# 		for j in range(len(noeuds_coordonnées)):
# 			position[0,j]=
# 			position[1,j]=
# 			resultante
# 	print(position)
#


# Programme principal
noeuds_coordonnées, noeuds_indices, barres, cord_barres = structure(Nb, longueur_barres)


# figure a l'instant t=0
plt.figure("figure barres")
for i in range(0, len(barres), 1):
	ind1, ind2 = barres[i]

	n1_x, n1_y = noeuds_coordonnées[ind1]
	n2_x, n2_y = noeuds_coordonnées[ind2]

	plt.plot([n1_x, n2_x], [n1_y, n2_y], "b", "-")
plt.show()


# longueur à vide

l0 = longueur_b(barres, noeuds_coordonnées)

# masse associée à chaque noeuds et voisins des noeuds

masse_n, voisins, P = masse__voisins(noeuds_coordonnées, diamètre_barre)
f_hooke, Nb_h = hooke(
	barres, noeuds_coordonnées, diamètre_barre, l0, voisins, cord_barres
)
h = 0.2
t_m = 50

position, vitesse, t = Euler(noeuds_coordonnées[1], 0, h, t_m)
# print(position)

# plt.figure("figure ")
# for i in range(np.size(t)):
# 	print(position[i][0], position[i][1])
# 	plt.plot(position[i][0], position[i][1], "b", "-")
# plt.show()
