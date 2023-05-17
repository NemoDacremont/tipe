
import matplotlib.pyplot as plt
from simulation import simulationRue, lireFichierDebit, lireFichierVitesse, creeFeu

from manipulationDonnees import convertiDonneesPlotVoitures, convertiDonneesPlotFeux, \
	extraitVitesseMoyenne, extraitVitesseMoyenne1, moyenneGlissante
from simulationOptimisation import simulationOptimisation



V0 = 8.33  # 3.33  # =5.4 à 17h17
T = 1.6
A = 2  # 2.77  # 0.73
B = 2
DELTA = 4
L = 4
S0 = 2
S1 = 3

PHYSIQUE = {
	"x": 0,
	"vx": V0,
	"ax": 0,
	"s_star": 0
}

# Constantes simulation
DEBUT = 0
FIN = 60
DT = 0.01

DIST_MAX = 245
DUREE_FEU = 20


N = 10



debits = lireFichierDebit("./debitVehicule/Strasbourg_P1")[:N]
vitesses = lireFichierVitesse("./vitesseVehicule/Strasbourg_P1")[:N]

pas = 1
debut = 20
fin = 30

durees = [debut + i * pas for i in range(int((fin - debut) / pas))]

Y = [0 for _ in range(int((fin - debut) / pas))]


def somme(L: list):
	"""
		Retourne la somme des éléments d'une liste de int ou de float
	"""
	s = 0
	for el in L:
		s += el

	return s


for i in range(int((fin - debut) / pas)):
	duree = durees[i]
	feux = [
		creeFeu(0, 40, duree, 3)
	]

	donneesVoitures, _ = simulationOptimisation(debits, V0, T, A, B, DELTA, L, S0, S1, PHYSIQUE, DIST_MAX, feux=feux)

	vitessesMoyennes_minutes = extraitVitesseMoyenne(donneesVoitures, 60)
	ecarts = somme([(vitessesMoyennes_minutes[i] - vitesses[i]) ** 2 for i in range(1, N)])
	Y[i] = ecarts



plt.figure()

plt.title(f"ecart en fonction de dureeFeu, {debut} à {fin}, pas={pas}, N={N}")

plt.plot(durees, Y)
plt.ylabel("Ecart")
plt.xlabel("dureeFeu")

plt.show()


