# !/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
from cmath import phase


# # Fonctions utiles
def lecture(nom_fichier):
	"""Lit un fichier de données

	Parameters
	----------
	nom_fichier: str
		nom du fichier à ouvrir. Chaque ligne du fichier doit être au format "x;y" avec x le temps et y la valeur du signal acquis.

	Returns
	-------
	array
		tableau des temps
	array
		tableau des valeurs du signal
	"""

	# Ouverture du fichier
	fichier = open(nom_fichier, "r")

	# Lecture du fichier
	texte = fichier.readlines()
	n = len(texte)  # Nombre de données
	temps = np.zeros(n)
	signal = np.zeros(n)
	for i in range(n):
		temps[i], signal[i] = texte[i].rstrip('\n').split(';')

	fichier.close()

	return temps, signal


def FFT(signal, Te):
	"""Calcule la transformée de Fourier discrète d'un signal échantillonné

	Parameters
	----------
	signal : array
		tableau des valeurs du signal
	Te : float
		période d'échantillonnage

	Returns
	-------
	array
		tableau des fréquences
	array
		tableau des amplitudes
	array
		tableau des phases
	"""


	N = signal.shape[0]

	amp_c = scipy.fft.fft(signal)
	# Amplitudes
	amp = np.abs(amp_c)     # On prend le module des différentes composantes complexes de la FFT
	amp =scipy.fftpack.fftshift(amp)  # On trie les composantes par fréquence croissante
	amp = amp[N // 2:]  # On ne garde que les fréquences positives

	# Phases
	phi = np.angle(amp_c)
	phi = scipy.fftpack.fftshift(phi)
	phi = phi[N // 2:]

	# Fréquences
	freqs = scipy.fftpack.fftfreq(N, Te)
	freqs = scipy.fftpack.fftshift(freqs)
	freqs = freqs[N // 2:]

	# Normalisation
	amp[1:] = amp[1:] * 2 / N
	amp[0] = amp[0] / N

	return freqs, amp, phi


# # Fonctions à compléter



def FFT_inverse(freq, amp, phi, Te, N):
	"""Calcule la transformée de Fourier discrète inverse

	Parameters
	----------

	freq : array
		tableau des fréquences
	amp : array
		tableau des amplitudes
	phi : array
		tableau des phases
	Te : float
		période d'échantillonnage
	N : int
		nombre de point du signal temporel

	Returns
	-------
	array
		tableau des valeurs du signal temporel
	"""

	temps = np.array([k * Te for k in range(N)])

	signal = np.zeros(N)

	for i in range(len(amp)):
		signal += amp[i] * np.cos(2 * np.pi * freq[i] * temps + phi[i])


	return signal




def passe_bas(w, params):
	"""Fonction de transfert d'un filtre passe-bas du 1er ordre

	Parameters
	----------

	w : float
		pulsation
	params : list
		[H0, wc] : le gain statique et la pulsation de coupure

	Returns
	-------
	complex
		la valeur de la fonction de transfert à la pulsation w
	"""
	HO, wc = params

	H = HO / (1 + (w / wc) * 1j)

	return H




def filtrage(entree, Te, H, params):
	"""Renvoie la valeur de la fonction de transfert à la pulsation w

	Parameters
	----------

	entree : array
		tableau des valeurs du signal à filtrer
	Te : float
		période d'échantillonnage
	H : func
		fonction de transfert
	params : list
		arguments de la fonction de transfert

	Returns
	-------
	entree : array
		tableau des valeurs du signal filtré
	"""
	N = len(entree)

	freq, amp, phi = FFT(entree, Te)

	# on applique le filtre sur chaque harmonique
	for k in range(len(freq)):
		f = freq[k]

		w = 2 * np.pi * f
		transfert = H(w, params)
		gain, dephasage = abs(transfert), phase(transfert)

		amp[k] = amp[k] * gain
		phi[k] = phi[k] + dephasage

	sortie = FFT_inverse(freq, amp, phi, Te, N)
	return sortie


def passe_bande(w, params):
	"""Fonction de transfert d'un filtre passe-bande du 2eme ordre

	Parameters
	----------

	w : float
		pulsation
	params : list
		[H0, Q, wc] : le gain statique, le facteur de qualité et la pulsation de coupure

	Returns
	-------
	complex
		la valeur de la fonction de transfert à la pulsation w
	"""

	H0, Q, wc = params
	# passe bande, formule développée
	H = H0 * (w * 1j / (Q * wc)) / (1 + w * 1j / (Q * wc) - (w / wc)**2)

	return H
