
from simulation import simulationEchelon, creeFeu
from copy import deepcopy
from constantes import DEBUT, FIN, DT


PHYSIQUE_DEFAUT = {
	"x": 0,
	"vx": 0,
	"ax": 0,
	"s_star": 0
}


FEUX_DEFAUT = [
	creeFeu(0, 40, 20, 3),
]


def simulationOptimisation(debitRue: list[float], v_0: float, T: float,
		a: float, b: float, delta: int, l: float, s_0: float, s_1: float,
		physique=PHYSIQUE_DEFAUT, distMax=1000, debut=DEBUT, fin=FIN, dt=DT,
		feux=FEUX_DEFAUT):
	"""
		Fait une suite de simulation en échelon durant chacune 1 minute où avec
		debitRue est une liste des débits de voitures par minute de la rue
		correspondante.

		donneesVoitures: [
			i -> dict[id: int -> voiture]
		]
	"""
	donneesVoitures = []
	donneesFeux = []
	voitures = []
	feux = deepcopy(feux)

	for i in range(len(debitRue)):
		debit = debitRue[i]
		temps = [fin * i + debut + k * dt for k in range(int((fin - debut) / dt))]

		donneesVoits, donneesF, voitures, feux = simulationEchelon(debit, temps, v_0,
			T, a, b, delta, l, s_0, s_1, physique, distMax, voitures, feux)


		donneesVoitures += donneesVoits
		donneesFeux += donneesF

	return donneesVoitures, donneesFeux



