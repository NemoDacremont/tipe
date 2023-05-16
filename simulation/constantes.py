
# pour des conseils:
# https://traffic-simulation.de/info/info_IDM.html
# Caractéristiques voiture / modèle
V0 = 8.16  # 3.33  # =5.4 à 17h17
T = 1.6
A = 1.88  # 2.77  # 0.73
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

# Constantes simulation échelon
DEBUT = 0  # en secones, début de l'échelon
FIN = 60  # en secondes, fin de l'échelon
DT = 0.01  # dt de l'échelon

# Relatif à la rue
DIST_MAX = 245
